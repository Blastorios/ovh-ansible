#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: public_cloud_sshkey
short_description: Create a new ssh key for OVH public cloud
description:
    - This module manage creation of a new ssh key for OVH public cloud
author: Marco Sarti <m.sarti@onetag.com>
requirements:
    - ovh >= 0.5.0
options:
    name:
        required: true
        description:
            - The name of the ssh key to create
    public_cloud_ssh_key:
        required: true
        description:
            - The public key to upload
    region:
        required: false
        description:
            - The region where to deploy public key
    service_name:
        required: true
        description:
            - The service_name
"""

EXAMPLES = r"""
- name: "Create a new ssh key on public cloud OVH"
  blastorios.ovh.public_cloud_sshkey:
    name: "{{ sshkey_name }}"
    public_cloud_ssh_key: "{{ sshkey_key }}"
    service_name: "{{ service_name }}"
    region: "{{ region }}"
  delegate_to: localhost
  register: sshkey_data
"""

RETURN = """ # """


from typing import Optional

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(
        name=dict(required=True),
        public_cloud_ssh_key=dict(required=True),
        region=dict(required=False, default=None),
        service_name=dict(required=True),
    )
)
def main(
    module: AnsibleModule,
    client: OVH,
    name: str,
    service_name: str,
    public_cloud_ssh_key: str,
    region: Optional[str],
):
    sshkey_list = client.wrap_call("GET", f"/cloud/project/{service_name}/sshkey")

    for k in sshkey_list:
        if k["name"] == name:
            module.exit_json(changed=False, msg=f"Key {name} is already present")

    result = client.wrap_call(
        "POST",
        f"/cloud/project/{service_name}/sshkey",
        name=name,
        region=region,
        publicKey=public_cloud_ssh_key,
    )

    module.exit_json(changed=True, **result)


if __name__ == "__main__":
    main()
