#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: dedicated_server_boot_wait
short_description: Wait until the dedicated server hard reboot is done
description:
    - Wait until the dedicated server hard reboot is done
    - Can be used to wait before running next task in your playbook
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    service_name:
        required: true
        description: Ovh name of the server
    max_retry:
        required: false
        description: Number of retry
        default: 240
    sleep:
        required: false
        description: Time to sleep between retries
        default: 10

"""

EXAMPLES = r"""
- name: Wait until the dedicated server hard reboot is done
  blastorios.ovh.dedicated_server_boot_wait:
    service_name: "ns12345.ip-1-2-3.eu"
    max_retry: "240"
    sleep: "10"
  delegate_to: localhost
"""

RETURN = """ # """

import time

from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
    OVH,
    collection_module,
)


@collection_module(
    dict(
        service_name=dict(required=True),
        max_retry=dict(required=False, default=240),
        sleep=dict(required=False, default=10),
    )
)
def main(
    module: AnsibleModule, client: OVH, service_name: str, max_retry: str, sleep: str
):
    if module.check_mode:
        module.exit_json(msg="done - (dry run mode)", changed=False)

    for i in range(1, int(max_retry)):
        tasklist = client.wrap_call(
            "GET", f"/dedicated/server/{service_name}/task", function="hardReboot"
        )
        result = client.wrap_call(
            "GET", f"/dedicated/server/{service_name}/task/{max(tasklist)}"
        )

        message = ""
        # Get details in reboot progression
        if "done" in result["status"]:
            module.exit_json(
                msg="{}: {}".format(result["status"], message), changed=False
            )
        else:
            message = result["status"]

        time.sleep(float(sleep))
    module.fail_json(
        msg="Max wait time reached, about %i x %i seconds" % (i, int(sleep))
    )


if __name__ == "__main__":
    main()
