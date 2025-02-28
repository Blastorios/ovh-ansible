#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: vps_display_name
short_description: Modify the vps display name in ovh manager
description:
    - Modify the vps display name in ovh manager, to help you find your vps with your own naming
author: Synthesio SRE Team / Paul Tap (armorica)
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
- name: "Set display name to {{ display_name }} on vps {{ ovhname }}"
  blastorios.ovh.vps_display_name:
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

    resource = {"displayName": display_name}

    # Endpoint /vps/{service_name} retrieves (among others) the current value for displayName

    get_result = client.wrap_call("GET", f"/vps/{service_name}", **resource)

    # Now check if the value is different and if necessary set it
    if get_result["displayName"] != display_name:
        client.wrap_call("PUT", f"/vps/{service_name}", **resource)
        module.exit_json(
            msg="displayName succesfully set to {} for {} !".format(
                display_name, service_name
            ),
            changed=True,
        )
    else:
        module.exit_json(
            msg="No change required to displayName {} for {} !".format(
                display_name, service_name
            ),
            changed=False,
        )


if __name__ == "__main__":
    main()
