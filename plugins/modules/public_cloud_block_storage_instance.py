#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    collection_module,
)
from ..module_utils.types import (
    StatePresentAbsent,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: public_cloud_block_storage_instance

short_description: Manage OVH API for public cloud volume and instance.

description:
    - This module attach or detach a volume of an instance on OVH public Cloud.

requirements:
    - ovh >= 0.5.0

options:
    service_name:
        required: true
        description: The service_name
    volume_id:
        required: true
        description: The volume uuid
    instance_id:
        required: true
        description: The instance uuid
    state:
        required: false
        default: present
        choices: ['present','absent']
        description: Indicate the desired state of volume
"""
EXAMPLES = r"""
- name: Ensure Volume is affected to instance
  blastorios.ovh.public_cloud_block_storage_instance:
    service_name: "{{ service_name }}"
    volume_id: "{{ volume_id }}"
    instance_id: "{{ instance_id }}"
  delegate_to: localhost
  register: block_storage_instance_metadata
"""
RETURN = """ # """


@collection_module(
    dict(
        service_name=dict(required=True),
        instance_id=dict(required=True),
        volume_id=dict(required=True),
        state=dict(choices=["present", "absent"], default="present"),
    ),
    use_default_check_mode=True,
)
def main(
    module: AnsibleModule,
    client: OVH,
    service_name: str,
    instance_id: str,
    volume_id: str,
    state: StatePresentAbsent,
):
    volume_details = {}
    volume_details = client.wrap_call(
        "GET", f"/cloud/project/{service_name}/volume/{volume_id}"
    )

    # Search if the volume exist. Consider you manage a strict nomenclature.
    if instance_id in volume_details["attachedTo"] and state == "absent":
        result = client.wrap_call(
            "POST",
            f"/cloud/project/{service_name}/volume/{volume_id}/detach",
            instanceId=instance_id,
        )
        module.exit_json(
            changed=True,
            msg="Volume id {} has been detached from instance id {}".format(
                volume_id, instance_id
            ),
            **result,
        )

    elif instance_id not in volume_details["attachedTo"] and state == "present":
        result = client.wrap_call(
            "POST",
            f"/cloud/project/{service_name}/volume/{volume_id}/attach",
            instanceId=instance_id,
        )
        module.exit_json(
            changed=True,
            msg="Volume id {} has been attached to instance id {}".format(
                volume_id, instance_id
            ),
            **result,
        )

    else:  # ( if instance_id not in volume_details and state == 'absent' ) or (if instance_id in volume_details and state == 'present' )
        module.exit_json(changed=False, **volume_details)


if __name__ == "__main__":
    main()
