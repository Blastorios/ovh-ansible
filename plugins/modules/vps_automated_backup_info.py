#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: vps_automated_backup_info
short_description: Retrieve the automated backup info for a OVH vps
description:
    - This module retrieves the automated backup info for a OVH vps
author: Blastorios
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
"""

EXAMPLES = r"""
- name: Retrieve the automated backup settings for an OVH vps
  blastorios.ovh.vps_automated_backup_info:
    service_name: "{{ service_name }}"
  register: vps_automated_backup_info
"""

RETURN = """ # """

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(dict(service_name=dict(required=True)))
def main(module: AnsibleModule, client: OVH, service_name: str):
    result = client.wrap_call("GET", f"/vps/{service_name}/automatedBackup")

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
