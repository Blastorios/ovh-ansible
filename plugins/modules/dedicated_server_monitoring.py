#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: dedicated_server_monitoring
short_description: Enable or disable ovh monitoring on a dedicated server
description:
    - Enable or disable ovh monitoring on a dedicated server
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: The service_name
    state:
        required: true
        description: Indicate the desired state of monitoring
        choices:
          - present
          - absent

"""

EXAMPLES = r"""
- name: "Enable monitoring on dedicated server {{ service_name }}"
  blastorios.ovh.dedicated_server_monitoring:
    service_name: "{{ service_name }}"
    state: "present"
  delegate_to: localhost
"""

RETURN = """ # """

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
        state=dict(choices=["present", "absent"], default="present"),
    )
)
def main(
    module: AnsibleModule, client: OVH, service_name: str, state: StatePresentAbsent
):
    if state == "present":
        monitoring_bool = True
    elif state == "absent":
        monitoring_bool = False

    if module.check_mode:
        module.exit_json(
            msg="Monitoring is now {} for {} - (dry run mode)".format(
                state, service_name
            ),
            changed=True,
        )

    server_state = client.wrap_call("GET", f"/dedicated/server/{service_name}")

    if server_state["monitoring"] == monitoring_bool:
        module.exit_json(
            msg="Monitoring is already {} on {}".format(state, service_name),
            changed=False,
        )

    client.wrap_call(
        "PUT", f"/dedicated/server/{service_name}", monitoring=monitoring_bool
    )

    module.exit_json(
        msg="Monitoring is now {} on {}".format(state, service_name), changed=True
    )


if __name__ == "__main__":
    main()
