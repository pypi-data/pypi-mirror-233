from __future__ import print_function

from six.moves import http_client as httplib
import json
import os
import requests
import sys
import time
import zc.lockfile


class Updater(object):
  def __init__(self, sleep, mapping_file, state_file, master_certificate_file,
               on_update, identity_file, server_ca_certificate_file, once,
               prepare_only):
    self.sleep = sleep
    self.mapping_file = mapping_file
    self.state_file = state_file
    self.state_lock_file = '%s.lock' % (state_file, )
    self.master_certificate_file = master_certificate_file
    self.on_update = on_update
    self.identity_file = identity_file
    self.server_ca_certificate_file = server_ca_certificate_file
    self.once = once
    self.prepare_only = prepare_only

  def updateMapping(self):
    self.mapping = {}
    with open(self.mapping_file) as fh:
      for line in fh.readlines():
        line = line.strip()
        if line.startswith('#'):
          continue
        if not line:
          continue
        line_content = line.split()
        if len(line_content) == 2:
          url, certificate = line_content
          fallback = None
        elif len(line_content) == 3:
          url, certificate, fallback = line_content
        else:
          print('Line %r is incorrect' % (line,))
          continue
        if certificate in self.mapping:
          print('Line %r is incorrect, duplicated certificate %r' % (
            line, certificate))
          raise ValueError
        self.mapping[certificate] = (url, fallback)

  def fetchCertificate(self, url, certificate_file):
    certificate = ''
    try:
      response = requests.get(
        url, verify=self.server_ca_certificate_file, cert=self.identity_file,
        timeout=10)
    except Exception as e:
      print('Certificate %r: problem with %r not downloaded: %s' % (
        certificate_file, url, e))
    else:
      if response.status_code != httplib.OK:
        print('Certificate %r: %r not downloaded, HTTP code %s' % (
          certificate_file, url, response.status_code))
      else:
        certificate = response.text
        if len(certificate) == 0:
          print('Certificate %r: %r is empty' % (certificate_file, url,))
    return certificate

  def updateCertificate(self, certificate_file, master_content=None):
    url, fallback_file = self.mapping[certificate_file]
    certificate = self.fetchCertificate(url, certificate_file)

    fallback_overridden = self.state_dict.get(certificate_file, False)
    fallback = ''
    if fallback_file:
      try:
        with open(fallback_file, 'r') as fh:
          fallback = fh.read() or None
      except IOError:
        pass
    current = ''
    try:
      with open(certificate_file, 'r') as fh:
        current = fh.read()
    except IOError:
      current = ''

    if not(certificate):
      if fallback and not fallback_overridden:
        certificate = fallback
      elif not current and master_content is not None:
        url = self.master_certificate_file
        certificate = master_content
      else:
        return False
    else:
      self.state_dict[certificate_file] = True

    if current != certificate:
      with open(certificate_file, 'w') as fh:
        fh.write(certificate)
        print('Certificate %r: updated from %r' % (certificate_file, url))
        return True
    else:
      return False

  def callOnUpdate(self):
    if self.on_update is not None:
      status = os.system(self.on_update)
      print('Called %r with status %i' % (self.on_update, status))

  def readState(self):
    self.state_dict = {}
    try:
      with open(self.state_file, 'r') as fh:
        try:
          self.state_dict = json.load(fh)
        except ValueError:
          pass
    except IOError:
      pass

  def writeState(self):
    with open(self.state_file, 'w') as fh:
      json.dump(self.state_dict, fh, indent=2)

  def prepare(self):
    self.updateMapping()
    prepare_mapping = self.mapping.copy()
    _, master_certificate_file_fallback = prepare_mapping.pop(
      self.master_certificate_file, (None, None))

    # update master certificate from fallback
    if self.master_certificate_file:
      if not os.path.exists(self.master_certificate_file):
        if master_certificate_file_fallback and os.path.exists(
          master_certificate_file_fallback):
          open(self.master_certificate_file, 'w').write(
            open(master_certificate_file_fallback, 'r').read()
          )
          print('Prepare: Used %r for %r' % (
            master_certificate_file_fallback, self.master_certificate_file))

    master_content = None
    if self.master_certificate_file and os.path.exists(
      self.master_certificate_file):
      master_content = open(self.master_certificate_file, 'r').read()

    for certificate, (_, fallback) in prepare_mapping.items():
      if os.path.exists(certificate):
        continue
      if fallback and os.path.exists(fallback):
        open(certificate, 'w').write(open(fallback, 'r').read())
        print('Prepare: Used %r for %r' % (fallback, certificate))
      elif master_content:
        open(certificate, 'w').write(master_content)
        print('Prepare: Used %r for %r' % (
          self.master_certificate_file, certificate))

  def action(self):
    self.readState()
    updated = False

    if self.master_certificate_file in self.mapping:
      updated = self.updateCertificate(self.master_certificate_file)
      self.mapping.pop(self.master_certificate_file)

    master_content = None
    if self.master_certificate_file is not None:
      try:
        with open(self.master_certificate_file, 'r') as fh:
          master_content = fh.read() or None
          if master_content:
            print('Using master certificate from %r' % (
              self.master_certificate_file,))
      except IOError:
        pass

    for certificate_file in self.mapping.keys():
      if self.updateCertificate(certificate_file, master_content):
        updated = True

    if updated:
      self.callOnUpdate()
    self.writeState()

  def loop(self):
    while True:
      try:
        if not self.prepare_only:
          lock = zc.lockfile.LockFile(self.state_lock_file)
      except zc.lockfile.LockError as e:
        print(e,)
        if self.once or self.prepare_only:
          print('...exiting.')
          sys.exit(1)
        else:
          print("...will try again later.")
      else:
        try:
          self.prepare()
          if not self.prepare_only:
            self.action()
        finally:
          if not self.prepare_only:
            lock.close()
            try:
              os.unlink(self.state_lock_file)
            except Exception:
              print('Problem while unlinking %r' % (self.state_lock_file,))
      if self.once or self.prepare_only:
        break
      print('Sleeping for %is' % (self.sleep,))
      time.sleep(self.sleep)
