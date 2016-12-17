#!/usr/bin/env python

#   This file is part of Ansible Vima Inventory.
#
#   Ansible Vima Inventory is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   Ansible Vima Inventory is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with vima_ansible_inventory. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# version 0.1 Michael-Angelos Simos

from json import load, dump, loads, dumps
from time import time
from sys import exit
from argparse import ArgumentParser
import os
import sys
from robobrowser import RoboBrowser
import errno
from inventory_hooks import grouping
try:
    from json import dumps, dump, load
except ImportError:
    from simplejson import dumps, dump, load
from argparse import ArgumentParser
try:
    # python 2
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    # python 3
    from configparser import ConfigParser



class GRnetVima:

    def __init__(self, v_url, v_user, v_password):
        try:
            br = RoboBrowser(parser="html.parser")
            br.open("{}{}".format(v_url.rstrip('/'), "/user/login"))
            form = br.get_forms()[1]
            form['username'].value = v_user
            form['password'].value = v_password
            br.submit_form(form)

        except Exception as error:
            print("Could not create browser: {}".format(error))
            sys.exit(1)
        self.v_url = v_url
        self.br = br

    def list_inventory(self):
        try:
            self.br.open("{}{}".format(self.v_url.rstrip('/'), "/instances/json/"))
            ret_page = self.br.response.content
            data = loads(ret_page.decode('utf-8'))
            inventory = self.grouped_inventory(data['aaData'], group_func=grouping)
            return inventory

        except Exception as e:
            print("[Error] : " + str(e))
            exit(1)

    @staticmethod
    def grouped_inventory(inventory, group='status', field='name', group_func=None):
        data = {}
        for d in inventory:
            if d[field]:
                if group_func:
                    group_func(data, d, field)
                else:

                    if type(d[group]) == list:
                        for g in d[group]:
                            if g in data:
                                data[g].append(d[field])
                            else:
                                data[g] = [d[field]]
                    else:
                        if d[group] in data:
                            data[d[group]].append(d[field])
                        else:
                            data[d[group]] = [d[field]]
        return data


def list_and_cache(hostname, user, password, cache_path):
    v = GRnetVima(hostname, user, password)
    data = v.list_inventory()
    with open(cache_path, 'w') as fp:
        dump(data, fp)
    return data


def get_inventory(hostname, user, password, cache_path=None, cache_ttl=3600, refresh=False):
    if refresh:
        return list_and_cache(hostname, user, password, cache_path)
    else:
        if os.path.isfile(cache_path) and time() - os.stat(cache_path).st_mtime < cache_ttl:
            try:
                with open(cache_path) as f:
                    data = load(f)
                    return data
            except (ValueError, IOError):
                return list_and_cache(hostname, user, password, cache_path)
        else:
            if not os.path.exists(os.path.dirname(cache_path)):
                try:
                    if cache_path:
                        os.makedirs(os.path.dirname(cache_path))
                    else:
                        raise OSError("cache_path not defined: {}".format(cache_path))
                # handle race condition
                except OSError as exc:
                    if exc.errno == errno.EACCES:
                        print("{}".format(str(exc)))
                        exit(1)
                    elif exc.errno != errno.EEXIST:
                        raise
            return list_and_cache(hostname, user, password, cache_path)


def main():

    # Parse Config

    config = ConfigParser()
    default_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    'vima_inventory.ini')
    ini_path = os.path.expanduser(os.path.expandvars(os.environ.get('VIMA_INVENTORY_INI_PATH',
                                                                    default_ini_path)))
    config.read(ini_path)

    cache_path = config.get('GENERIC', 'cache_path', fallback='/tmp/ansible-vima-inventory-cache.tmp')
    cache_ttl = config.getint('GENERIC', 'cache_ttl')
    ini_host = config.get('GENERIC', 'vima_url', fallback='')
    ini_user = config.get('GENERIC', 'vima_user', fallback='')
    ini_pass = config.get('GENERIC', 'vima_pass', fallback='')

    # Parse Arguments

    parser = ArgumentParser()

    parser.add_argument('-s', '--url', help='Vima url', dest='hostname')
    parser.add_argument('-u', '--username', help='Vima Server username', dest='user')
    parser.add_argument('-p', '--password', help='Vima Server password', dest='password')
    parser.add_argument('-l', '--list', help='List all VMs', action='store_true', default=True)
    parser.add_argument('-g', '--guest', help='Print a single guest')
    parser.add_argument('-x', '--host', help='Print a single guest')
    parser.add_argument('-r', '--reload-cache', help='Reload cache', action='store_true', default=False)

    args = parser.parse_args()

    # Override with arg parameters if defined

    if not args.password:
        if not ini_pass:
            import getpass
            ini_pass = getpass.getpass()
        setattr(args, 'password', ini_pass)
    if not args.user:
        setattr(args, 'user', ini_user)
    if not args.hostname:
        setattr(args, 'hostname', ini_host)

    # Perform requested operations

    if args.host or args.guest:
        print ('{}')
        exit(0)
    elif args.list:
        data = get_inventory(args.hostname, args.user, args.password,
                             cache_path=cache_path, cache_ttl=cache_ttl, refresh=args.reload_cache)
        print ("{}".format(dumps(data)))


if __name__ == "__main__":
    main()
