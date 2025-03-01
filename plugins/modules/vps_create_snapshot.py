#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from typing import Optional

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    collection_module,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: vps_create_snapshot
short_description: Create a VPS snapshot
description:
    - Create a new Snapshot if the option is enabled and there is not existing snapshot
author: Blastorios
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
    description:
        required: false
        description: A Snapshot description
"""
EXAMPLES = r"""
- name: Retrieve the automated backup settings for an OVH vps
  blastorios.ovh.vps_create_snapshot:
    service_name: "{{ service_name }}"
    description: Quickly saving before I do something weird
"""
RETURN = """ # """


@collection_module(
    dict(
        service_name=dict(required=True), description=dict(required=False, default=None)
    ),
    use_default_check_mode=True,
)
def main(
    module: AnsibleModule, client: OVH, service_name: str, description: Optional[str]
):
    if description is None:
        description = ""

    result = client.wrap_call(
        "POST", f"/vps/{service_name}/createSnapshot", description=description
    )

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
