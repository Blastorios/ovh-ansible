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
module: ip_move
short_description: Move IP to another service
description:
    - Move IP to another service
author: Erwan Ben Souiden
requirements:
    - ovh >= 0.5.0
options:
    ip:
        required: true
        description: The ip
    service_name:
        required: true
        description: The service_name
"""
EXAMPLES = r"""
- name: Modify reverse on IP
  blastorios.ovh.ip_move:
    ip: 192.0.2.1
    service_name: "nsXXXXX.ip-YY-YYY-YYY.net"
  delegate_to: localhost
"""
RETURN = """ # """


@collection_module(
    dict(ip=dict(required=True), service_name=dict(required=True)),
    use_default_check_mode=True,
)
def main(module: AnsibleModule, client: OVH, ip: str, service_name: str):
    result = {}
    result = client.wrap_call("GET", f"/ip/{ip}")

    try:
        current_service_name = result["routedTo"]["serviceName"]
    except KeyError:
        current_service_name = ""

    if current_service_name == service_name:
        module.exit_json(
            msg="{} already moved to {} !".format(ip, service_name), changed=False
        )

    client.wrap_call("POST", f"/ip/{ip}/move", nexthop=None, to=service_name)
    module.exit_json(
        msg="{} successfully moved to {} !".format(ip, service_name), changed=True
    )


if __name__ == "__main__":
    main()
