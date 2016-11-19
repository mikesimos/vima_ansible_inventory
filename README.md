# Description
Vima Ansible Inventory is dynamic inventory script for listing GRNET VPS
service (vima.grnet.gr) virtual machines. It can be easily configured via
it's configuration file (vima_inventory.ini).

# Installation
###### install prerequisites:
* Ubuntu/Debian
``
apt-get install python-mechanize
``
* RHEL/CentOS/Other using pip:
``
pip install -r requirements.txt
``
###### Clone vima_ansible_inventory at your IT Automation server:
``git clone https://github.com/mikeSimos/vima_ansible_inventory.git``
###### Configure vima_inventory.ini file accordingly.

# Usage
Example usage:
``
$ ansible all -i vima_inventory.py -m ping
``
# Testing
* Sample testing using unittests auto discovery:
``
python -m unittest discover
``
