#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    collection_module,
)
from ..module_utils.types import (
    OVHPolicies,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: public_cloud_object_storage_policy

short_description: Manage OVH API for public cloud S3 bucket policy.

description:
    - This module applies a policy to an existing S3 user on a OVH public cloud bucket.

requirements:
    - ovh >= 0.5.0

options:
    service_name:
        required: true
        description: The service_name (OVH public cloud project ID)
    region:
        required: true
        description: The region where is located the S3 bucket
    name:
        required: true
        description: The S3 bucket name
    user_name:
        required: true
        description: The S3 user name (must already exists on public cloud project)
    policy:
        required: true
        description: Role associated to the user on this bucket
"""
EXAMPLES = r"""
- name: Add a read-only user to a S3 bucket
  blastorios.ovh.public_cloud_object_storage:
    service_name: "{{ service_name }}"
    region: "{{ region }}"
    name: "bucket-{{ inventory_hostname }}"
    user_name: "user-RaNdOm"
    policy: "readOnly"
  delegate_to: localhost
  register: object_storage_policy_metadata
"""
RETURN = """ # """


@collection_module(
    dict(
        service_name=dict(required=True),
        region=dict(required=True),
        name=dict(required=True),
        user_name=dict(required=True),
        policy=dict(required=True, choices=["deny", "admin", "readOnly", "readWrite"]),
    ),
    use_default_check_mode=True,
)
def main(
    module: AnsibleModule,
    client: OVH,
    service_name: str,
    region: str,
    name: str,
    user_name: str,
    policy: OVHPolicies,
):
    """Apply a policy (user <-> role) to an OVH public cloud S3 bucket"""
    user_list = []
    user_list = client.wrap_call("GET", f"/cloud/project/{service_name}/user")

    # Search user ID in cloud project existing users
    for user in user_list:
        if user["username"] == user_name:
            _ = client.wrap_call(
                "POST",
                f"/cloud/project/{service_name}/region/{region}/storage/{name}/policy/{user['id']}",
                roleName=policy,
            )
            module.exit_json(
                msg="Policy {} was applied to user {} on S3 bucket {} ({})".format(
                    policy, user_name, name, region
                ),
                changed=True,
            )

    module.fail_json(
        msg="User {} was not found on OVH public cloud project {}".format(
            user_name, service_name
        ),
        changed=False,
    )


if __name__ == "__main__":
    main()
