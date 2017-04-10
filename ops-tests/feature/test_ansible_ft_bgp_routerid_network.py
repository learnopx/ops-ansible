# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from time import sleep
from pytest import mark

TOPOLOGY = """
#
#      +-----------------+             +------------+
#      |     Ansible     | eth0   eth0 |            |
#      | control machine |-------------| OpenSwitch |
#      |    (server)     |             |  (switch)  |
#      +-----------------+             +------------+
#
# Nodes
[type=oobmhost name="server" image="openswitch/ops-ansible:2.1"] server
[type=openswitch name="switch"] switch
#
# Links
[force_name=oobm] switch:eth0
server:eth0 -- switch:eth0
"""


def _setup(topo):
    """ setup server and switch to be ready for the ansible play """
    server = topo.get('server')
    switch = topo.get('switch')

    # Wait switch to come up
    sleep(10)

    # Server IP address
    server.libs.ip.interface('eth0', addr='192.168.1.254/24', up=True)

    # Switch IP address
    with switch.libs.vtysh.ConfigInterfaceMgmt() as ctx:
        ctx.ip_static('192.168.1.1/24')

    return server


def copy_ssh_key(server, step):
    # Copy SSH public key through playbook
    step("copy ssh-key from host to ops")
    _test_playbook(server, 'utils/copy_public_key.yaml', ops='-u root')


def git_clone_ops_ansible_copy_sshkey(server):
    server("git clone https://git.openswitch.net/openswitch/"
           "ops-ansible.git /etc/ansible/")
    while (server("echo $?") == 0):
        sleep(30)
    server("cp -r /etc/ansible/utils/id* /root/.ssh/")
    while (server("echo $?") == 0):
        sleep(10)


def _cmd(playbook, ops=''):
    return "ansible-playbook %s /etc/ansible/%s" % (ops, playbook)


def _test_playbook(server, playbook, ops=''):
    bash = server.get_shell('bash')
    bash.send_command(_cmd(playbook, ops), timeout=90)
    out = bash.get_response()
    print(out)
    assert '0' == server('echo $?'), "fail in %s" % playbook


@mark.platform_incompatible(['docker'])
def test_bgp_role(topology, step):
    test_playbooks = ['roles/bgp/tests/test_bgp_network.yml',
                      'roles/bgp/tests/test_bgp_router_id.yml']

    server = _setup(topology)
    if(topology.engine == 'ostl'):
        git_clone_ops_ansible_copy_sshkey(server)
    sleep(30)
    copy_ssh_key(server, step)
    for playbook in test_playbooks:
        step("Test %s playbook" % playbook)
        _test_playbook(server, playbook, ops='-v')
