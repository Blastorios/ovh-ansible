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
  blastorios.ovh.vps_reboot:
    service_name: "{{ service_name }}"
"""
RETURN = """ # """


@collection_module(dict(service_name=dict(required=True)), use_default_check_mode=True)
def main(module: AnsibleModule, client: OVH, service_name: str):
    result: dict = client.wrap_call("POST", f"/vps/{service_name}/reboot")

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
