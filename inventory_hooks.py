"""
Groupping hook function for Ansible Inventory
An example of formating.
"""


def grouping(data, vm, field):
    if vm['status'] == 'Running':
        if vm['ipaddress']:
            if 'pubExtcloud' in data:
                data['pubExtcloud'].append(vm[field])
            else:
                data['pubExtcloud'] = [vm[field]]
        else:
            if 'vExtcloud0' in data:
                data['vExtcloud0'].append(vm[field])
            else:
                data['vExtcloud0'] = [vm[field]]
