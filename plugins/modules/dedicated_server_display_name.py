#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: dedicated_server_display_name
short_description: Modify the server display name in ovh manager
description:
    - Modify the server display name in ovh manager, to help you find your server with your own naming
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
    display_name:
        required: true
        description: The display name to set

"""

EXAMPLES = r"""
- name: "Set display name to {{ display_name }} on server {{ ovhname }}"
  blastorios.ovh.dedicated_server_display_name:
    service_name: "{{ ovhname }}"
    display_name: "{{ display_name }}"
  delegate_to: localhost
"""

RETURN = """ # """

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(display_name=dict(required=True), service_name=dict(required=True))
)
def main(module: AnsibleModule, client: OVH, display_name: str, service_name: str):
    if module.check_mode:
        module.exit_json(
            msg="display_name has been set to {} ! - (dry run mode)".format(
                display_name
            ),
            changed=True,
        )

    result = client.wrap_call("GET", f"/dedicated/server/{service_name}/serviceInfos")

    service_id = result["serviceId"]
    resource = {"resource": {"displayName": display_name, "name": service_name}}

    client.wrap_call("PUT", f"/service/{service_id}", **resource)
    module.exit_json(
        msg="displayName succesfully set to {} for {} !".format(
            display_name, service_name
        ),
        changed=True,
    )


if __name__ == "__main__":
    main()
