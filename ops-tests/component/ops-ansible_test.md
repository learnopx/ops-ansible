# Ansible Test Cases

- [Test the SSH reachability to OpenSwitch](#test-the-ssh-reachability)

## Test the SSH reachability
### Objective
Verify that the ssh public key can be copied from control machine
to OpenSwitch by running `utils/copy_public_key.yaml` playbook and
check the SSH communication can be established by running
`utils/ping.yaml` playbook.

### Requirements
The topology framework test setup is required for this test.

### Setup

#### Topology diagram

```
      +-----------------+             +------------+
      |     Ansible     | eth0   eth0 |            |
      | control machine |-------------| OpenSwitch |
      |    (server)     |             |  (switch)  |
      +-----------------+             +------------+
```

### Description
This test confirms that we can establish ssh communication
between Ansible control machine and the openswitch. We use
the ansible playbook to copy the ssh key from ansible control
machine to openswitch and then try using a ping module through
ansible playbook to check if we can communicate with OpenSwitch.

#### Test steps

1. Play `utils/copy_public_key.yaml` playbook with `root` account
   by `ansible-playbook utils/copy_public_key.yaml` command on
   Ansible control machine.
2. Check the exit code of the above command by executing `echo $?`.
3. Play `utils/ping.yaml` playbook with `admin` account by
   `ansible-playbook utils/ping.yaml` command on Ansible
   control machine.
4. Check the exit code of the above command by executing `echo $?`.

### Test result criteria
#### Test pass criteria
All the `ansible-playbook` execution returns zero.

#### Test fail criteria
One of the `ansible-playbook` execution returns non-zero.
