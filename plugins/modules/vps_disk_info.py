#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: vps_disk_info
short_description: Get the VPS disk info
description:
    - Get the disk information for a VPS
author: Blastorios
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
    disk_ids:
        required: false
        type: list
        description: The disk id, leave empty to get all disks
"""

EXAMPLES = r"""
- name: Retrieve the automated backup settings for an OVH vps
  synthesio.ovh.vps_automated_backup_info:
    service_name: "{{ service_name }}"
  register: vps_automated_backup_info
"""

RETURN = """ # """

from typing import Optional, List

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(
        service_name=dict(required=True),
        disk_ids=dict(required=False, type="list", default=None),
    )
)
def main(
    module: AnsibleModule, client: OVH, service_name: str, disk_ids: Optional[List[str]]
):
    if disk_ids is None:
        result = client.wrap_call("GET", f"/vps/{service_name}/disks")
    else:
        result = {}
        for disk_id in disk_ids:
            result[disk_id] = client.wrap_call(
                "GET", f"/vps/{service_name}/disks/{disk_id}"
            )

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
