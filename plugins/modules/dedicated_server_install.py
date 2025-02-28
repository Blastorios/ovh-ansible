#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: dedicated_server_install
short_description: Install a new dedicated server
description:
    - Install a new dedicated server
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: Ovh name of the server
    hostname:
        required: true
        description: Name of the new dedicated server
    template:
        required: true
        description: template to use to spawn the server
    soft_raid_devices:
        required: false
        description: number of devices in the raid software
    user_metadata:
        required: false
        description: list of key,value objects metadata
    raid:
        required: false
        description: enable (md) or disable (jbod) software raid

"""

EXAMPLES = r"""
- name: Install a new dedicated server
  blastorios.ovh.dedicated_server_install:
    service_name: "ns12345.ip-1-2-3.eu"
    hostname: "server01.example.net"
    template: "debian10_64"
    soft_raid_devices: "2"
    raid: "enabled"
    partition_scheme_name: "custom"
    user_metadata:
        - key: sshKey
          value: "ssh-ed25519 AAAAC3 ..."
  delegate_to: localhost
"""

RETURN = """ # """

from typing import Optional, List

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)
from ansible_collections.blastorios.ovh.plugins.module_utils.types import (
    StateEnabledDisabled,
)


@collection_module(
    dict(
        service_name=dict(required=True),
        hostname=dict(required=True),
        template=dict(required=True),
        soft_raid_devices=dict(required=False, default=None),
        partition_scheme_name=dict(required=False, default="default"),
        raid=dict(choices=["enabled", "disabled"], default="enabled", required=False),
        user_metadata=dict(type="list", requirements=False, default=None),
    )
)
def main(
    module: AnsibleModule,
    client: OVH,
    service_name: str,
    hostname: str,
    template: str,
    soft_raid_devices: Optional[str],
    partition_scheme_name: str,
    raid: StateEnabledDisabled,
    user_metadata: Optional[List],
):
    if module.check_mode:
        module.exit_json(
            msg=f"Installation in progress on {service_name} as {hostname} with template {template} - (dry run mode)",
            changed=True,
        )

    compatible_templates = client.wrap_call(
        "GET", f"/dedicated/server/{service_name}/install/compatibleTemplates"
    )
    if (
        template not in compatible_templates["ovh"]
        and template not in compatible_templates["personal"]
    ):
        module.fail_json(msg="f{template} doesn't exist in compatibles templates")

    if raid == "enabled":
        no_raid = False
    elif raid == "disabled":
        no_raid = True

    details = {
        "details": {
            "language": "en",
            "customHostname": hostname,
            "softRaidDevices": soft_raid_devices,
            "noRaid": no_raid,
        }
    }

    client.wrap_call(
        "POST",
        f"/dedicated/server/{service_name}/install/start",
        **details,
        templateName=template,
        partitionSchemeName=partition_scheme_name,
        userMetadata=user_metadata,
    )

    module.exit_json(
        msg=f"Installation in progress on {service_name} as {hostname} with template {template}!",
        changed=True,
    )


if __name__ == "__main__":
    main()
