# -*- coding: utf-8 -*-
# Copyright (C) 2018  Nexedi SA
#     Lukasz Nowak <luke@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.

from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from threading import local
from wsgiref.simple_server import make_server
import caucase.exceptions
import caucase.http
import caucase.utils
from caucase.http_wsgibase import CleanServerHandler
import datetime
import json
import os
import random
import signal
import sqlite3
import ssl
import string
from six.moves.urllib import parse as urlparse
import logging
import logging.handlers

import socket
socket.setdefaulttimeout(10)


class UserExists(Exception):
  pass


class Unauthorized(Exception):
  pass


class ReferenceNotFound(Exception):
  pass


class SQLite3Storage(local):
  """
  Data storage.

  Stolen^WInspired on caucase/storage.py
  """
  def __init__(
    self,
    db_path,
    mode=0o600,
  ):
    """
    db_path (str)
      SQLite connection string.
    mode (int)
      Permissions of the main database file upon creation.
    """
    super(SQLite3Storage, self).__init__()
    # Create database file if it does not exist, so mode can be controlled.
    os.close(os.open(
      db_path,
      os.O_CREAT | os.O_RDONLY,
      mode,
    ))
    self._db = db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    with db:
      db.cursor().executescript('''
        CREATE TABLE IF NOT EXISTS reserved_reference (
          reference VARCHAR(255) PRIMARY KEY,
          active INTEGER
        );
        CREATE TABLE IF NOT EXISTS certificate (
          id INTEGER,
          reference VARCHAR(255),
          submission_date INTEGER,
          not_valid_before_date INTEGER,
          not_valid_after_date INTEGER,
          pem TEXT,
          PRIMARY KEY (id, reference)
        );
        CREATE TABLE IF NOT EXISTS counter (
          name TEXT PRIMARY KEY,
          value INTEGER
        );
        CREATE TABLE IF NOT EXISTS uploader (
          reference TEXT PRIMARY KEY,
          key TEXT,
          active INTEGER
        )
      ''')

  def _incrementCounter(self, name, increment=1, initial=0):
    """
    Increment counter with <name> by <increment> and return resulting value.
    If <name> is not found, it is created with <initial>, and then incremented.
    Does not commit.
    """
    row = self._executeSingleRow(
      'SELECT value FROM counter WHERE name = ? LIMIT 2',
      (name, )
    )
    if row is None:
      value = initial
    else:
      value = row['value']
    value += increment
    self._db.cursor().execute(
      'INSERT OR REPLACE INTO counter (name, value) VALUES (?, ?)',
      (name, value),
    )
    return value

  def _executeSingleRow(self, sql, parameters=()):
    """
    Execute <sql>, raise if it produces more than 1 row, and return it.
    """
    result_list = self._db.cursor().execute(sql, parameters).fetchall()
    if result_list:
      result, = result_list
      return result
    return None

  def addUploader(self, reference):
    self.checkReservedId(reference)
    with self._db as db:
      result = self._executeSingleRow(
        'SELECT reference FROM uploader WHERE reference = ? ',
        (reference, ),
      )
      if result is not None:
        raise UserExists
      key = ''.join(
        random.choice(
          string.ascii_lowercase + string.digits) for i in range(32))
      db.cursor().execute(
        'INSERT INTO uploader '
        '(reference, key, active) '
        'VALUES (?, ?, ?)',
        (
          reference,
          key,
          1
        ),
      )
      return key

  def validateUploader(self, reference, key):
    result = self._executeSingleRow(
      'SELECT 1 FROM uploader '
      'WHERE reference = ? AND key = ? AND active = 1',
      (reference, key),
    )
    return bool(result)

  def reserveId(self):
    for trynum in range(10):
      reserved_id = ''.join(
        random.choice(
          string.ascii_lowercase + string.digits) for _ in range(32))
      result = self._executeSingleRow(
        'SELECT 1 FROM reserved_reference WHERE reference = ?', (
          reserved_id,),
      )
      if not result:
        break
    else:
      raise ValueError
    with self._db as db:
      db.cursor().execute(
        'INSERT INTO reserved_reference '
        '(reference, active) '
        'VALUES (?, 1)', (reserved_id,)
      )
      return reserved_id

  def checkReservedId(self, reference):
    if not self._executeSingleRow(
      'SELECT 1 FROM reserved_reference WHERE reference = ?', (
        reference,)
    ):
      raise ReferenceNotFound

  def addCertificate(self, reference, submission_timestamp,
                     not_valid_before_timestamp, not_valid_after_timestamp,
                     pem):
    self.checkReservedId(reference)
    with self._db as db:
      certificate_id = self._incrementCounter(reference)
      db.cursor().execute(
        'INSERT INTO certificate '
        '(id, reference, submission_date, not_valid_before_date,'
        ' not_valid_after_date, pem) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (
          certificate_id,
          reference,
          submission_timestamp,
          not_valid_before_timestamp,
          not_valid_after_timestamp,
          pem,
        ),
      )
    return certificate_id

  def _cleanCertificate(self):
    now = datetime.datetime.utcnow()
    with self._db as db:
      cursor = db.cursor()
      cursor.execute(
        'DELETE FROM certificate '
        'WHERE not_valid_after_date < ?', (now,))
      cursor.execute(
        'DELETE FROM certificate '
        'WHERE not_valid_before_date > ?', (now,))

  def getCertificate(self, reference, index=None):
    self._cleanCertificate()
    now = datetime.datetime.utcnow()
    query = \
        'SELECT pem FROM certificate WHERE reference = ? ' + \
        'AND submission_date < ? '
    order = 'ORDER BY submission_date DESC LIMIT 1'
    if index is None:
      result = self._executeSingleRow(
        query + order,
        (reference, now),
      )
    else:
      result = self._executeSingleRow(
        query + 'AND id=? ' + order,
        (reference, now, index),
      )
    if result:
      return result['pem']
    return None

  def iterCertificateIndexes(self, reference):
    self._cleanCertificate()
    with self._db as db:
      now = datetime.datetime.utcnow()
      c = db.cursor()
      for row in c.execute(
        'SELECT id FROM certificate WHERE reference=? '
        'AND submission_date < ? '
        'ORDER BY submission_date DESC',
        (reference, now)):
        yield row['id']


class CertificateError(Exception):
  pass


class Kedifa(object):
  """KeDiFa application API

/

  GET (not auth required) GETs self descriptive API
      content-type: application/json

/reserve-id

  POST (SSL authorisation) reserves new id to be used

/{reserved-id}[?auth=XXX]

  PUT (key authorisation in query string) puts certificate,
      content-type: application/x-x509-ca-cert
  GET (SSL authorisation) GETs most recently submitted certificate
      content-type: text/plain

/{reserved-id}/list?auth=XXX

  GET (SSL authorisation) GETs list of stored certificates, most
      recent first
      content-type: application/json

/{reserved-id}/{id}?auth=XXX

  GET (SSL authorisation) exact certificate
  content-type: text/plain

/{reserved-id}/generateauth

  GET (no auth required) one time access URL which returns auth key
  content-type: text/plain
"""
  def loadCertificate(self, ca_certificate_path, crl_path):
    self.ca_certificate_list = [
      caucase.utils.load_ca_certificate(x)
      for x in caucase.utils.getCertList(ca_certificate_path)]

    self.crl_list = [
      crl
      for _, crl in caucase.utils.iter_valid_crl_list(
        crl_pem_list=caucase.utils.getCRLList(crl_path),
        trusted_cert_list=self.ca_certificate_list,
      )
    ]

  def __init__(self, pocket, ca_certificate, crl):
    self.pocket_db = SQLite3Storage(pocket)

    self.loadCertificate(ca_certificate, crl)

  def checkKeyCertificate(self, data):
    try:
      # this is the only place where caucase.utils is NOT used, as this
      # certificate comes without any CA, so caucase.utils.load_certificate
      # can't be used
      certificate = x509.load_pem_x509_certificate(
        data, caucase.utils._cryptography_backend)
    except ValueError:
      raise CertificateError('Certificate incorrect')

    try:
      key = caucase.utils.load_privatekey(data)
    except ValueError:
      raise CertificateError('Key incorrect')

    utcnow = datetime.datetime.utcnow()
    if utcnow > certificate.not_valid_after:
      raise CertificateError('Certificate expired')

    if utcnow < certificate.not_valid_before:
      raise CertificateError('Certificate not valid yet')

    if certificate.public_key().public_numbers() != \
       key.public_key().public_numbers():
      raise CertificateError('Key and certificate do not match')

    return certificate

  def SSLAuth(self, environ):
    try:
      caucase.utils.load_certificate(
        environ.get('SSL_CLIENT_CERT', b''),
        trusted_cert_list=self.ca_certificate_list,
        crl_list=self.crl_list,
      )
    except (caucase.exceptions.CertificateVerificationError, ValueError):
      raise Unauthorized

  def __call__(self, environ, start_response):
    headers_text_plain = [('Content-Type', 'text/plain')]
    headers_application_json = [('Content-Type', 'application/json')]
    path_list = environ['PATH_INFO'].split('/')
    qs = environ.get('QUERY_STRING', '')
    parameters = {}
    if qs:
      try:
        parameters = urlparse.parse_qs(qs, strict_parsing=True)
      except ValueError:
        start_response('400 Bad Request', headers_text_plain)
        return (b'Query string %r was not correct.' % (qs, ),)

    if len(path_list) == 2:
      _, reference = path_list
      index = None
    elif len(path_list) == 3:
      _, reference, index = path_list
      if not index:
        index = None
    else:
      start_response('400 Bad Request', headers_text_plain)
      return (b'Wrong path',)

    if not reference:
      start_response('400 Bad Request', headers_text_plain)
      return (b'Wrong path',)

    if environ['REQUEST_METHOD'] == 'PUT':
      # key auth
      if 'auth' not in parameters:
        start_response('400 Bad Request', headers_text_plain)
        return (b'Missing auth',)
      elif not self.pocket_db.validateUploader(
        reference, parameters['auth'][0]):
        headers = headers_text_plain + [('WWW-Authenticate', 'transport')]
        start_response('401 Unauthorized', headers)
        return (b'',)
      # play with curl --data-binary
      if index is not None:
        raise ValueError
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
      request_body = environ['wsgi.input'].read(request_body_size)
      try:
        certificate = self.checkKeyCertificate(request_body)
      except CertificateError as e:
        start_response('422 Unprocessable Entity', headers_text_plain)
        return (str(e).encode(),)
      else:
        try:
          certificate_id = self.pocket_db.addCertificate(
            reference,
            datetime.datetime.utcnow(),
            certificate.not_valid_before,
            certificate.not_valid_after,
            request_body
          )
        except ReferenceNotFound:
          start_response('404 Not Found', headers_text_plain)
          return (b'Reservation required',)
        start_response('201 Created', headers_text_plain + [
          ('Location', '/'.join(path_list + [str(certificate_id)]))])
        return (b'',)
    elif environ['REQUEST_METHOD'] == 'POST':
      # SSL-auth
      try:
        self.SSLAuth(environ)
      except Unauthorized:
        headers = headers_text_plain + [('WWW-Authenticate', 'transport')]
        start_response('401 Unauthorized', headers)
        return (b'',)
      if index is not None:
        raise ValueError
      if reference != 'reserve-id':
        raise ValueError

      reserved_id = self.pocket_db.reserveId()
      start_response('201 Created', headers_text_plain + [
        ('Location', '/%s' % reserved_id)])
      return (reserved_id.encode(),)
    elif environ['REQUEST_METHOD'] == 'GET':
      if index == 'list':
        # SSL-auth
        try:
          self.SSLAuth(environ)
        except Unauthorized:
          headers = headers_text_plain + [('WWW-Authenticate', 'transport')]
          start_response('401 Unauthorized', headers)
          return (b'',)
        key_list = [
          str(q) for q in self.pocket_db.iterCertificateIndexes(reference)]
        start_response('200 OK', headers_application_json)
        return (json.dumps(dict(key_list=key_list), indent=2).encode(),)
      elif index == 'generateauth':
        try:
          key = self.pocket_db.addUploader(reference)
        except UserExists:
          start_response('403 Forbidden', headers_text_plain)
          return (b'Already exists',)
        except ReferenceNotFound:
          start_response('404 Not Found', headers_text_plain)
          return (b'Reservation required',)
        else:
          start_response('201 Created', headers_text_plain)
          return (key.encode(),)
      else:
        # SSL-auth
        try:
          self.SSLAuth(environ)
        except Unauthorized:
          headers = headers_text_plain + [('WWW-Authenticate', 'transport')]
          start_response('401 Unauthorized', headers)
          return (b'',)
        certificate = self.pocket_db.getCertificate(reference, index)
        if certificate is None:
          start_response('404 Not Found', headers_text_plain)
          return (b'',)
        else:
          start_response('200 OK', headers_text_plain)
          if getattr(certificate, 'encode', None) is not None:
            certificate = certificate.encode()
          return (certificate,)
    else:
      raise NotImplementedError


def getSSLContext(server_key_path, ca_certificate_path, crl_path):
  ssl_context = ssl.create_default_context(
    purpose=ssl.Purpose.CLIENT_AUTH,
  )
  # Do not trust CRL check on ssl_context level, as it will happen in more
  # controllable conditions on application level
  # ssl_context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
  # ssl_context.load_verify_locations(cafile=crl_path)

  ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
  ssl_context.verify_mode = ssl.CERT_OPTIONAL
  ssl_context.load_verify_locations(cafile=ca_certificate_path)
  ssl_context.load_cert_chain(server_key_path)
  return ssl_context


class Reloader(object):
  def __init__(self, httpd, app, server_key_path, ca_certificate_path,
               crl_path):
    self.httpd = httpd
    self.server_key_path = server_key_path
    self.ca_certificate_path = ca_certificate_path
    self.crl_path = crl_path
    self.app = app

  def handle(self, signum, frame):
    self.app.loadCertificate(self.ca_certificate_path, self.crl_path)
    ssl_context = getSSLContext(
      self.server_key_path, self.ca_certificate_path, self.crl_path)
    ssl_socket = self.httpd.socket
    try:
      ssl_socket.context = ssl_context
    except AttributeError:
      # Workaround for python bug 34747: changing a listening
      # SSLSocket's SSL context fails on
      # "self._sslobj.context = context" while "self._sslobj" is only
      # set on connected sockets.
      # Luckily is it done just after updating "self._context" which is
      # what is actually used when accepting a connection - so the update
      # is actually successful.
      pass
    logger.warning('KeDiFa reloaded.')


logger = logging.getLogger('kedifa')


def setuplog(logfile):
  if logfile == '-':
    ch = logging.StreamHandler()
  else:
    ch = logging.handlers.WatchedFileHandler(logfile)
  formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  logger.setLevel(logging.INFO)


class KedifaSSLWSGIRequestHandler(caucase.http.CaucaseSSLWSGIRequestHandler):
  def log_message(self, format, *args):
    """
    Log an arbitrary message.

    Compared to caucase.http.CaucaseSSLWSGIRequestHandler:
    - use logger
    """
    logger.info(
      '%s - %s [%s] %s',
      self.client_address[0],
      self.remote_user_name,
      self.log_date_time_string(),
      format % args,
    )


def log_exception(self, exc_info):
  try:
    logger.exception(
      'Exception while handling the request:', exc_info=exc_info)
  finally:
      exc_info = None


CleanServerHandler.log_exception = log_exception


def http(host, port, pocket, certificate, ca_certificate, crl, pidfile,
         logfile):
  setuplog(logfile)
  pid = str(os.getpid())
  pidfile.write(pid)
  pidfile.close()
  kedifa = Kedifa(pocket, ca_certificate.name, crl.name)
  if ':' in host:
    access_format = 'https://[%s]:%s/'
  else:
    access_format = 'https://%s:%s/'
  httpd = make_server(
    host, port, kedifa, caucase.http.ThreadingWSGIServer,
    KedifaSSLWSGIRequestHandler
  )
  ssl_context = getSSLContext(certificate.name, ca_certificate.name, crl.name)
  httpd.socket = ssl_context.wrap_socket(
     httpd.socket,
     server_side=True)

  try:
    httpd.server_bind()
    httpd.server_activate()
  except Exception:
    httpd.server_close()
    raise

  logger.info(
   'Kedifa started at %s with pid %s stored in %s',
   access_format % httpd.server_address[:2], pid, pidfile.name)

  reloader = Reloader(
    httpd, kedifa, certificate.name, ca_certificate.name, crl.name)
  signal.signal(signal.SIGHUP, reloader.handle)

  try:
    httpd.serve_forever()
  finally:
    httpd.server_close()
    httpd.shutdown()
