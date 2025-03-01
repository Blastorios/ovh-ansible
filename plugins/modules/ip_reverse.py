#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from typing import Optional
from urllib import parse

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.ovh import (
    OVH,
    ResourceNotFound,
    collection_module,
)


__metaclass__ = type


DOCUMENTATION = """
---
module: ip_reverse
short_description: Modify reverse on IP
description:
    - Modify reverse on IP
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    ip:
        required: true
        description: The ip
    reverse:
        required: true
        description: The reverse to assign
    ip_block:
        required: false
        description: The ipBlock (only for vrack IPs)
        default: None

"""
EXAMPLES = r"""
- name: Modify reverse on IP
  blastorios.ovh.ip_reverse:
    ip: 192.0.2.1
    reverse: host.domain.example.
  delegate_to: localhost
"""
RETURN = """ # """


@collection_module(
    dict(
        ip=dict(required=True),
        reverse=dict(required=True),
        ip_block=dict(required=False, default=None),
    ),
    use_default_check_mode=True,
)
def main(
    module: AnsibleModule, client: OVH, ip: str, reverse: str, ip_block: Optional[str]
):
    # ip_block is only needed for vrack IPs. Default it to "ip" when not used
    if ip_block is None:
        ip_block = ip
    else:
        # url encode the ip mask (/26 -> %2F)
        ip_block = parse.quote(ip_block, safe="")

    result = {}
    try:
        result = client.wrap_call("GET", f"/ip/{ip_block}/reverse/{ip}")
    except ResourceNotFound:
        result["reverse"] = ""

    if result["reverse"] == reverse:
        module.exit_json(
            msg="Reverse {} to {} already set !".format(ip, reverse), changed=False
        )

    client.wrap_call("POST", f"/ip/{ip_block}/reverse", ipReverse=ip, reverse=reverse)
    module.exit_json(
        msg="Reverse {} to {} succesfully set !".format(ip, reverse), changed=True
    )


if __name__ == "__main__":
    main()
