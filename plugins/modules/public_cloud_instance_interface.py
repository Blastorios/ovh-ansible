#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: public_cloud_instance_interface

short_description: Manage OVH API for public cloud interfaces.

description:
    - This module attach or detach an interface of an instance on OVH public Cloud.

requirements:
    - ovh >= 0.5.0

options:
    service_name:
        required: true
        description: The service name
    instance_id:
        required: true
        description: The instance uuid
    state:
        required: false
        default: present
        choices: ['present','absent']
        description: Indicate the desired state of the interface
    interface_ip:
        required: true
        description: The fixed IP to set to the interface
    interface_openstack_id:
        required: true
        description:
            - The network's openstack id to attache the interface to
            - This is returned by a call to public_cloud_private_network_info.
"""

EXAMPLES = r"""
  - name: Create vrack interface
  blastorios.ovh.public_cloud_instance_interface:
    service_name: "{{ service_name }}"
    instance_id: "{{ instance_id }}"
    interface_ip: "{{ network_vrack.ip }}"
    interface_openstack_id: "{{ network_info.openstack_id }}"
  delegate_to: localhost
  register: interface_metadata

"""

RETURN = r""" # """

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)
from ansible_collections.blastorios.ovh.plugins.module_utils.types import (
    StatePresentAbsent,
)


@collection_module(
    dict(
        service_name=dict(required=True),
        instance_id=dict(required=True),
        state=dict(choices=["present", "absent"], default="present"),
        interface_ip=dict(required=True),
        interface_openstack_id=dict(required=True),
    )
)
def main(
    module: AnsibleModule,
    client: OVH,
    service_name: str,
    instance_id: str,
    state: StatePresentAbsent,
    interface_ip: str,
    interface_openstack_id: str,
):
    if module.check_mode:
        module.exit_json(
            msg="Ensure interface {} on {} is {} on instance id {} - (dry run mode)".format(
                interface_ip, interface_openstack_id, state, instance_id
            ),
            changed=True,
        )

    if state == "absent":
        # Need to get the interface id (via /cloud/project/{serviceName}/instance/{instanceId}/interface).
        # How to manage multiple interfaces ?
        module.fail_json(msg="Removing an interface is not yet implemented")
    if state == "present":
        result = client.wrap_call(
            "POST",
            f"/cloud/project/{service_name}/instance/{instance_id}/interface",
            ip=interface_ip,
            networkId=interface_openstack_id,
        )
        module.exit_json(
            changed=True,
            msg="Interface has been attached to instance id {}".format(instance_id),
            **result,
        )


if __name__ == "__main__":
    main()
