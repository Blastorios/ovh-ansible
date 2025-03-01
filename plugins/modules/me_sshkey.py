#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    collection_module,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: me_sshkey
short_description: Retrieve ssh key by name
description:
    - This module retrieves a ssh key by its name
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    ssh_key_name:
        required: true
        description: The ssh key name
"""
EXAMPLES = r"""
- name: Retrieve ssh key by name
  blastorios.ovh.me_sshkey:
    ssh_key_name: "{{ ssh_key_name }}"
  delegate_to: localhost
  register: ssh_key

- name: "Set the ssh key for access in rescue mode {{ service_name }}"
  blastorios.ovh.dedicated_server_rescuesshkey:
    service_name: "{{ service_name }}"
    ssh_key: "{{ ssh_key.key }}"
  delegate_to: localhost
"""
RETURN = """ # """


@collection_module(dict(ssh_key_name=dict(required=True)), use_default_check_mode=True)
def main(module: AnsibleModule, client: OVH, ssh_key_name: str):
    result = client.wrap_call("GET", f"/me/sshKey/{ssh_key_name}")

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
