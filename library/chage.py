#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>, and others
# (c) 2016, Toshio Kuratomi <tkuratomi@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: chage
short_description: Set expiry attributes on a user
version_added: historical
options:
  user:
    description:
      - The user to manage expiry attributes for.
    required: true
    default: null
  password_last_changed:
    description:
      - The date that the users password was last changed.
    required: no
    default: null
[...]
'''

EXAMPLES = '''
[...]
'''

import sys
import glob
import shlex
import os
import json

args_file = sys.argv[1]
args_data = file(args_file).read()
args = shlex.split(args_data)

executable = "chage"
clargs = dict()
argnames = {
  "password_last_changed": "lastday",
  "account_expires": "expiredate",
  "inactive_days": "inactive",
  "password_minimum_days": "mindays",
  "password_maximum_days": "maxdays",
  "password_warn_days": "warndays",
}
user = False

for arg in args:
    # ignore any arguments without an equals in it
    if "=" in arg:
        (key, value) = arg.split("=")
        if key == 'user':
            user = value
        else:
            keyname = argnames.get(key, False)
            if keyname != False:
                if value == 'False':
                    clargs[keyname] = '-1'
                else:
                    clargs[keyname] = value

if user == False:
    print json.dumps({
        "failed" : True,
        "msg"    : "You need to select a user to manage"
    })
    sys.exit(1)

def chage_check(user):
  os.system('chage -l "%s" > tmp' % user)
  return open('tmp', 'r').read()

before = chage_check(user)

arguments = list()
for key, val in clargs.items():
    arguments.append("--%s %s" % (key, val))

command = executable + ' ' + ' '.join(arguments) + ' ' + user
rc = os.system(command)

if rc != 0:
    print json.dumps({
        "failed" : True,
        "msg"    : "Failed setting the expiry attributes",
        "command": command
    })
    sys.exit(1)

changed = before != chage_check(user)

print json.dumps({
    "changed": changed,
    "command": command
})
sys.exit(0)
