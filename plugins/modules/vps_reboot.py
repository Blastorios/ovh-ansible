#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: vps_reboot
short_description: Reboot a VPS
description:
    - Reboot a VPS
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
  synthesio.ovh.vps_reboot:
    service_name: "{{ service_name }}"
"""

RETURN = """ # """

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(dict(service_name=dict(required=True)))
def main(module: AnsibleModule, client: OVH, service_name: str):
    result: dict = client.wrap_call("POST", f"/vps/{service_name}/reboot")

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
