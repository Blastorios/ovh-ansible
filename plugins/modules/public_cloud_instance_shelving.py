#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: public_cloud_instance_shelving
short_description: Manage shelving status of an OVH public cloud instance
description:
    - This module manage shelving status of an OVH public cloud instance.
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
    instance_id:
        required: true
        description: The instance id
    shelving_state:
        required: true
        choices: ["shelved", "unshelved"]
        description: The shelved desired status
"""

EXAMPLES = r"""
- name: Shelve the instance
  synthesio.ovh.public_cloud_instance_shelving:
    instance_id: "{{ instance_id }}"
    service_name: "{{ service_name }}"
    shelve_state: "shelved"
 delegate_to: localhost

- name: Unshelve the instance
  synthesio.ovh.public_cloud_instance_shelving:
    instance_id: "{{ instance_id }}"
    service_name: "{{ service_name }}"
    shelve_state: "unshelved"
  delegate_to: localhost
"""

RETURN = """ # """

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(
        service_name=dict(required=True),
        shelve_state=dict(required=True, choices=["shelved", "unshelved"]),
        instance_id=dict(required=True),
    )
)
def main(
    module: AnsibleModule,
    client: OVH,
    service_name: str,
    shelve_state: str,
    instance_id: str,
):
    # Set the route depending on the action
    if shelve_state == "shelved":
        route = f"/cloud/project/{service_name}/instance/{instance_id}/shelve"
    elif shelve_state == "unshelved":
        route = f"/cloud/project/{service_name}/instance/{instance_id}/unshelve"
    else:
        module.fail_json(msg=f"Shelve state {shelve_state} is unknown", changed=False)

    # Do the call
    client.wrap_call("POST", route)

    message = f"State change to {shelve_state} for instance {instance_id}. This might take a couple of minutes."

    module.exit_json(
        result=message,
        changed=True,
    )


if __name__ == "__main__":
    main()
