#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    collection_module,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: dedicated_server_terminate
short_description: Terminate a dedicated server renting
description:
    - Terminate a dedicated server renting. Need mail confirmation
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service_name to terminate
"""
EXAMPLES = r"""
- name: Terminate a dedicated server renting
  blastorios.ovh.dedicated_server_terminate:
    service_name: "{{ service_name }}"
  delegate_to: localhost
"""
RETURN = """ # """


@collection_module(dict(service_name=dict(required=True)), use_default_check_mode=True)
def main(module: AnsibleModule, client: OVH, service_name: str):
    client.wrap_call("POST", f"/dedicated/server/{service_name}/terminate")

    module.exit_json(
        changed=True,
        msg="Terminate {} is done, please confirm via the email sent".format(
            service_name
        ),
    )


if __name__ == "__main__":
    main()
