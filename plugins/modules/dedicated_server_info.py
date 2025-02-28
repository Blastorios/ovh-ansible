#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: dedicated_server_info
short_description: Retrieve basic info for an OVH dedicated server
description:
    - This module retrieves basic info for an OVH dedicated server
author: Maxime Dupré
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service_name
"""

EXAMPLES = r"""
- name: Retrieve basic info for an OVH dedicated server
  blastorios.ovh.dedicated_server_info:
    service_name: "{{ service_name }}"
  delegate_to: localhost
  register: dedicated_info
"""

RETURN = """ # """

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(dict(service_name=dict(required=True)))
def main(module: AnsibleModule, client: OVH, service_name: str):
    result = client.wrap_call("GET", f"/dedicated/server/{service_name}")

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
