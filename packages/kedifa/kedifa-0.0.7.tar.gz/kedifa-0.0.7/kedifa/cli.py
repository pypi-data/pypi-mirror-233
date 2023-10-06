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

from __future__ import print_function

import argparse
from six.moves import http_client as httplib
import requests
import sys

from . import app
from .updater import Updater


def http(*args):
  if not args:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(description='KeDiFa webapp')
  parser.add_argument(
    '--ip',
    help='IP to bind to (v4 or v6).',
    required=True
  )
  parser.add_argument(
    '--port',
    type=int,
    help='Port to bind to.',
    required=True
  )
  parser.add_argument(
    '--db',
    help='Path to the SQLite database.',
    required=True
  )
  parser.add_argument(
    '--certificate',
    type=argparse.FileType('r'),
    help='Path SSL certificate.',
    required=True
  )
  parser.add_argument(
    '--ca-certificate',
    type=argparse.FileType('r'),
    help='Path SSL CA certificate.',
    required=True
  )
  parser.add_argument(
    '--crl',
    type=argparse.FileType('r'),
    help='Path SSL CRL.',
    required=True
  )
  parser.add_argument(
    '--pidfile',
    type=argparse.FileType('w'),
    help='Path to PID file.',
    required=True
  )
  parser.add_argument(
    '--logfile',
    type=str,
    help='Path to logfile.',
    default='-'
  )
  parsed = parser.parse_args(args)

  app.http(parsed.ip, parsed.port, parsed.db, parsed.certificate,
           parsed.ca_certificate, parsed.crl, parsed.pidfile, parsed.logfile)


def getter(*args):
  """Downloads a file with SSL client & server authentication, storing
     received data only when successful.
  """
  if not args:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(description='KeDiFa getter')
  parser.add_argument(
    'url',
    nargs=1,
    help='URL to fetch certificate from.'
  )
  parser.add_argument(
    '--identity',
    type=argparse.FileType('r'),
    help='Certificate to identify itself on the URL.',
    required=True
  )
  parser.add_argument(
    '--server-ca-certificate',
    type=argparse.FileType('r'),
    help='CA Certificate of the server.',
    required=True
  )
  parser.add_argument(
    '--out',
    help='Destination to store the downloaded certificate.',
    required=True
  )
  parsed = parser.parse_args(args)

  url = parsed.url[0]
  try:
    response = requests.get(url, verify=parsed.server_ca_certificate.name,
                            cert=parsed.identity.name)
  except Exception as e:
    print('%r not downloaded, problem %s' % (url, e))
    sys.exit(1)
  else:
    if response.status_code != httplib.OK:
      print('%r not downloaded, HTTP code %s' % (
        url, response.status_code))
      sys.exit(1)
    if len(response.text) > 0:
      with open(parsed.out, 'wb') as out:
        out.write(response.text.encode('utf-8'))


def updater(*args):
  """Periodically downloads file with SSL client & server authentication,
    updating it on change and success.
  """
  if not args:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(description='KeDiFa updater')

  parser.add_argument(
    'mapping',
    type=argparse.FileType('r'),
    help='File mapping of URL to DESTINATION, where URL is the source of the '
         'certificate, and DESTINATION is the output file.'
  )

  parser.add_argument(
    'state',
    type=str,
    help='Path to JSON state file for fallback recognition, on which locks '
         'will happen.',
    nargs='?'
  )

  parser.add_argument(
    '--identity',
    type=argparse.FileType('r'),
    help='Certificate to identify itself on the URL.',
  )

  parser.add_argument(
    '--server-ca-certificate',
    type=argparse.FileType('r'),
    help='CA Certificate of the server.',
  )

  parser.add_argument(
    '--master-certificate',
    type=str,
    help='Master certificate, to use in some cases. If it exsists in mapping '
         'file, will be updated.',
  )

  parser.add_argument(
    '--on-update',
    type=str,
    help='Executable to be run when update happens.'
  )

  parser.add_argument(
    '--sleep',
    type=int,
    help='Sleep time in seconds.',
    default=60
  )

  parser.add_argument(
    '--once',
    action='store_true',
    help='Run only once.',
  )

  parser.add_argument(
    '--prepare-only',
    action='store_true',
    help='Only prepares, without using netowrk. Enforces --once, disables '
         '--on-update, does not use nor lock state file, as it is not used.',
  )

  parsed = parser.parse_args(args)

  u = Updater(
    parsed.sleep, parsed.mapping.name, parsed.state, parsed.master_certificate,
    parsed.on_update,
    parsed.identity and parsed.identity.name or None,
    parsed.server_ca_certificate and parsed.server_ca_certificate.name or None,
    parsed.once, parsed.prepare_only
  )
  parsed.mapping.close()
  parsed.identity and parsed.identity.close()
  parsed.server_ca_certificate and parsed.server_ca_certificate.close()
  u.loop()
