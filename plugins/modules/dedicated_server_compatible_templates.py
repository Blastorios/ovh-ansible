#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
---
module: dedicated_server_compatible_templates
short_description: Retrieve all compatible templates for a OVH dedicated server
description:
    - This module retrieves all compatible templates for a OVH dedicated server
authors: Saul Bertuccio, Atlantis Boengkih
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service name
"""

EXAMPLES = r"""
- name: Retrieve all compatible templates for an OVH dedicated server
  synthesio.ovh.dedicated_server_compatible_templates:
    service_name: "{{ service_name }}"
  delegate_to: localhost
  register: dedicated_templates
"""

RETURN = r"""
compatible_templates:
    description: List of available templates for a the given host
    returned: always
    type: dict
    sample: {
              "ovh": [
                       "debian11_64",
                       "debian12-plesk18_64",
                       "debian12_64",
              ],
              "personal": [
                       "template_1",
                       "template_2"
              ]
    }
"""

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(dict(service_name=dict(required=True)))
def main(module: AnsibleModule, client: OVH, service_name: str):
    if module.check_mode:
        module.exit_json(
            msg=f"Retrieving templates for {service_name} - (dry run mode)",
            changed=False,
        )

    compatible_templates = client.wrap_call(
        "GET", f"/dedicated/server/{service_name}/install/compatibleTemplates"
    )

    module.exit_json(changed=False, compatible_templates=compatible_templates)


if __name__ == "__main__":
    main()
