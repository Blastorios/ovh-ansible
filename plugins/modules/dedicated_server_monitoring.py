#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: dedicated_server_monitoring
short_description: Enable or disable ovh monitoring on a dedicated server
description:
    - Enable or disable ovh monitoring on a dedicated server
author: Synthesio SRE Team
requirements:
    - ovh >= 0.5.0
options:
    serviceName:
        required: true
        description: The serviceName
    state:
        required: true
        description: Indicate the desired state of monitoring
        choices:
          - present
          - absent

'''

EXAMPLES = '''
synthesio.ovh.dedicated_server_monitoring:
    serviceName: "{{ serviceName }}"
    state: "present"
delegate_to: localhost
'''

RETURN = ''' # '''

from ansible_collections.synthesio.ovh.plugins.module_utils.ovh import ovh_api_connect, ovh_argument_spec

try:
    from ovh.exceptions import APIError
    HAS_OVH = True
except ImportError:
    HAS_OVH = False


def run_module():
    module_args = ovh_argument_spec()
    module_args.update(dict(
        serviceName=dict(required=True),
        state=dict(choices=['present', 'absent'], default='present')
    ))

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    client = ovh_api_connect(module)

    serviceName = module.params['serviceName']
    state = module.params['state']

    if state == 'present':
        monitoring_bool = True
    elif state == 'absent':
        monitoring_bool = False

    if module.check_mode:
        module.exit_json(msg="Monitoring is now {} for {} - (dry run mode)".format(state, serviceName), changed=True)

    try:
        server_state = client.get('/dedicated/server/%s' % serviceName)

        if server_state['monitoring'] == monitoring_bool:
            module.exit_json(msg="Monitoring is already {} on {}".format(state, serviceName), changed=False)

        client.put('/dedicated/server/%s' % serviceName, monitoring=monitoring_bool)

        module.exit_json(msg="Monitoring is now {} on {}".format(state, serviceName), changed=True)
    except APIError as api_error:
        module.fail_json(msg="Failed to call OVH API: {0}".format(api_error), changed=False)


def main():
    run_module()


if __name__ == '__main__':
    main()
