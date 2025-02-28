#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: public_cloud_instance_info
short_description: Retrieve all info for a OVH public cloud instance
description:
    - This module retrieves all info from a OVH public cloud instance
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service_name
    instance_id:
        required: true
        description: The instance uuid

"""

EXAMPLES = r"""
- name: Retrieve all info for a OVH public cloud instance
  synthesio.ovh.public_cloud_instance_info:
    instance_id: "{{ instance_id }}"
    service_name: "{{ service_name }}"
  delegate_to: localhost
  register: instance_metadata
"""

RETURN = """ # """

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(service_name=dict(required=True), instance_id=dict(required=True))
)
def main(module: AnsibleModule, client: OVH, service_name: str, instance_id: str):
    result = client.wrap_call(
        "GET", f"/cloud/project/{service_name}/instance/{instance_id}"
    )

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
