# OpenSwitch Ansible Roles and sample playbooks

## Overview

Here is the quote from the [official Ansible site](http://www.ansible.com):

> Ansible is a radically simple IT automation platform that makes your
> applications and systems easier to deploy.  Avoid writing scripts or
> custom code to deploy and update your applications - automate in a
> language that approaches plain English, using SSH, with no agents to
> install on remote systems.

OpenSwitch follows this philosophy and brings this simplicity into the
networking industry by providing the simple yet powerful APIs for Ansible
to interact with.

As Ansible does not require any agents on the remote systems as mentioned
above, and OpenSwitch is the remote system in this context, OpenSwitch
does not need the repository to host the software that runs on the switch.
Instead, [ops-ansible](http://git.openswitch.net/cgit/openswitch/ops-ansible)
repository hosts useful tools which will run on the control machine,
along with the Ansible core and the modules.


## Modules

OpenSwitch Ansible support is achieved through those four modules:

- OpenSwitch APIs
- Ansible OpenSwitch module
- Ansible playbooks and inventory files
- Optional Ansible OpenSwitch Roles*

*An operator can use the Ansible OpenSwitch Roles provided by
the OpenSwitch community.


Among those four, only OpenSwitch APIs is on the actual switch, and
the rest are installed on the control machine.


## High-level design

The diagram in this section shows:

1. Interaction between the Ansible control machine and OpenSwitch
2. Individual building blocks both in the control machine and OpenSwitch

The diagram also shows the two ways to interact with the switch through
the Ansible:

- Option A: Write a playbook that directory interacts with the Ansible
            OpenSwitch modules, for example ops\_template.py and/or
            ops\_facts.py.
- Option B: Write a simplified version of the playbook that leverages
            the abstraction offered by the Ansible OpenSwitch roles.

Option A gives you the full configuration power, as there is no
abstraction between your playbooks and the final JSON output, which
describes the switch state.

Option B simplifies your playbooks through the abstraction offered by
the roles.

You can also mix those two options to match your needs.  Refer to the
[Ansible playbook roles](http://docs.ansible.com/ansible/playbooks_roles.html),
for more information.

```
         +-----------------------------------------------+
         |            Control machine (e.g. laptop)      |
         |                                               |
         |       Option A                 Option B       |
         |  +-----------------+      +-----------------+ |
         |  |    Playbooks    |      |    Playbooks    | |
         |  +-----------------+      +-----------------+ |
         |  +-----------------+      +-----------------+ |
         |  | Inventory files |      | Inventory files | |
         |  +-----------------+      +-----------------+ |
         |  +-----------------+      +-----------------+ |
         |  | Ansible Jinja2  |      |     Ansible     | |
         |  | template files  |      | OpenSwitch Roles| |
         |  |    (Optional)   |      |(switch, bgp etc)| |
         |  +-----------------+      +-----------------+ |
         |           |                        |          |
         |           v                        v          |
         |  +------------------------------------------+ |
         |  |           Ansible 2.1 and above          | |
         |  | +----------------+     +---------------+ | |
         |  | |ops_template.py |     | ops_facts.py  | | |
         |  | |  for config    |     |   for facts   | | |
         |  | +----------------+     +---------------+ | |
         |  +------------------------------------------+ |
         +-----------------------------------------------+
                                 ^
                                 | Ansible transport (ssh etc)
                                 v
         +-----------------------------------------------+
         |                  OpenSwitch                   |
         |    +---------------+     +---------------+    |
         |    |  Declarative  |     |  RESTful API  |    |
         |    | Config(DC) API|     |      for      |    |
         |    |   for config  |     |     facts     |    |
         |    +-------------- +     +---------------+    |
         |    +-------------------------------------+    |
         |    |                                     |    |
         |    |            OVSDB database           |    |
         |    |                                     |    |
         |    +-------------------------------------+    |
         |    +---------+ +--------+ +-------+           |
         |    | switchd | |  bgpd  | | ospfd |  ...      |
         |    +---------+ +--------+ +-------+           |
         +-----------------------------------------------+
```


## References

- [www.ansible.com](http://www.ansible.com)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible core](https://github.com/ansible/ansible)
- [Ansible modules core](https://github.com/ansible/ansible-modules-core)
- [Ansible playbook roles](http://docs.ansible.com/ansible/playbooks_roles.html)
