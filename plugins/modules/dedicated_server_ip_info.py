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
module: dedicated_server_ip_info
short_description: Retrieve IP specifications for an OVH dedicated server
description:
    - This module retrieves detailed IP specifications for an OVH dedicated server
author: David Harkis
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service_name
"""
EXAMPLES = r"""
- name: Retrieve IP specifications for an OVH dedicated server
  blastorios.ovh.dedicated_server_ip_info:
    service_name: "{{ service_name }}"
  delegate_to: localhost
  register: ip_info
"""
RETURN = """
ipv4:
    description: Orderable IP v4 details.
    returned: always
    type: list
    elements: dict
    contains:
        blockSizes:
            description: Orderable IP blocks sizes.
            type: list
            elements: int
            sample: [1, 4, 8, 16, 32, 64, 128]
        included:
            description: Are those IP included with your offer.
            type: bool
            sample: true
        ipNumber:
            description: Total number of IP that can be routed to this server.
            type: int
            sample: 256
        number:
            description: Total number of prefixes that can be routed to this server.
            type: int
            sample: 254
        optionRequired:
            description: Which option is required to order this type of IP.
            type: str
            choices: [professionalUse]
        type:
            description: This IP type.
            type: str
            choices: [failover, static, unshielded]
            sample: failover
ipv6:
    description: Orderable IP v6 details.
    returned: always
    type: list
    elements: dict
    contains:
        blockSizes:
            description: Orderable IP blocks sizes.
            type: list
            elements: int
            choices: [1, 4, 8, 16, 32, 64, 128, 256]
        included:
            description: Are those IP included with your offer.
            type: bool
        ipNumber:
            description: Total number of IP that can be routed to this server.
            type: int
        number:
            description: Total number of prefixes that can be routed to this server.
            type: int
        optionRequired:
            description: Which option is required to order this type of IP.
            type: str
            choices: [professionalUse]
        type:
            description: This IP type.
            type: str
            choices: [failover, static, unshielded]
"""


@collection_module(dict(service_name=dict(required=True)), use_default_check_mode=True)
def main(module: AnsibleModule, client: OVH, service_name: str):
    result = client.wrap_call(
        "GET", f"/dedicated/server/{service_name}/specifications/ip"
    )
    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
