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
#   along with Foobar. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# version 0.1 Michael-Angelos Simos

import unittest
import types


class VimaAnsibleTestCase(unittest.TestCase):

    def test_mechanize(self):
        import mechanize
        self.assertTrue(isinstance(getattr(mechanize, 'Browser'), types.ClassType))

    def test_cookielib(self):
        import cookielib
        self.assertTrue(isinstance(getattr(cookielib, 'LWPCookieJar'), types.ClassType))

    def test_hook(self):
        import inventory_hooks
        self.assertTrue(hasattr(inventory_hooks, 'grouping'))
        self.assertTrue(callable(getattr(inventory_hooks, 'grouping')))

    def test_list_and_cache(self):
        import vima_inventory
        self.assertTrue(hasattr(vima_inventory, 'list_and_cache'))
        self.assertTrue(callable(getattr(vima_inventory, 'list_and_cache')))

    def test_get_inventory(self):
        import vima_inventory
        self.assertTrue(hasattr(vima_inventory, 'list_and_cache'))
        self.assertTrue(callable(getattr(vima_inventory, 'list_and_cache')))

if __name__ == '__main__':
    unittest.main()