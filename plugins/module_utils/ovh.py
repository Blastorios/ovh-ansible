from __future__ import absolute_import, division, print_function

__metaclass__ = type

from functools import wraps
from inspect import getfile
from typing import Dict

from ansible.module_utils.basic import AnsibleModule

try:
    import ovh
    from ovh.exceptions import (
        APIError,
        InvalidKey,
        NotGrantedCall,
        BadParametersError,
        HTTPError,
        ResourceNotFoundError,
    )

    HAS_OVH = True
except ImportError:
    HAS_OVH = False

    class ResourceNotFoundError(Exception):
        pass


class OVH:
    def __init__(self, module: AnsibleModule):
        self.module = module

        self._validate()
        self._credentials()

        if all(self.credentials_in_parameters):
            self.client = ovh.Client(
                **{
                    credential: self.module.params[credential]
                    for credential in self.credentials
                }
            )
        else:
            self.client = ovh.Client()

    def _validate(self):
        # TODO; This should not have to validate every single time.
        # Simply assume python-ovh is installed.
        if not HAS_OVH:
            self.module.fail_json(msg="python-ovh must be installed to use this module")

    def _credentials(self):
        self.credentials = [
            "endpoint",
            "application_key",
            "application_secret",
            "consumer_key",
        ]
        self.credentials_in_parameters = [
            cred in self.module.params for cred in self.credentials
        ]

    def wrap_call(self, verb: str, path: str, need_auth: bool = True, **kwargs):
        """
        Wrapper for the call to the api. Set kwargs using methods from the ovh module.

        Parameters
        ----------
        verb: str
            http verb to use for the call.
        path: str
            API route to call.
        need_auth: bool
            If True, send authentication headers. This is the default.

        Returns
        -------
        The API Call result.
        """
        # This is copied from the OVH python module
        # https://github.com/ovh/python-ovh/blob/master/ovh/client.py#L330
        if kwargs:
            kwargs = self.client._canonicalize_kwargs(kwargs)
            if verb in ["GET", "DELETE"]:
                query_string = self.client._prepare_query_string(kwargs)
                if query_string != "":
                    if "?" in path:
                        path = f"{path}&{query_string}"
                    else:
                        path = f"{path}?{query_string}"
        if not kwargs:
            kwargs = None

        try:
            return self.client.call(verb, path, kwargs, need_auth)

        except InvalidKey as e:
            self.module.fail_json(msg=f"Key {self.client._application_key}: {e}")
        except (BadParametersError, NotGrantedCall, HTTPError, APIError) as e:
            self.module.fail_json(
                msg=f"Fails calling API ({verb} {self.client._endpoint}{path}): {e}"
            )


def ovh_argument_spec() -> Dict:
    return dict(
        endpoint=dict(type="str", required=False, default=None),
        application_key=dict(type="str", required=False, default=None),
        application_secret=dict(type="str", required=False, default=None),
        consumer_key=dict(type="str", required=False, default=None),
    )


def collection_module(
    parameters: Dict,
    supports_check_mode: bool = True,
    use_default_check_mode: bool = False,
    **kwargs,
):
    """
    The top-level decorator to create a new OVH Collection Module.

    Both the AnsibleModule and OVH Client are invoked prior to the module
    function call, passing the required module arguments to the wrapped
    function.

    Optionally, you can pass AnsibleModule arguments directly into the
    decorator as they will be passed into the AnsibleModule construct.

    Parameters
    ----------
    parameters: dict
        A dictionary containing all module parameters.
    **kwargs:
        AnsibleModule parameters.

    Returns
    -------
    decorator: callable
        A wrapped module function with the required
        AnsibleModule and OVH client code.

    Raises
    ------
    TypeError
        If the specified module arguments differ from
        the function's input arguments.

    Example
    -------
    ```python
    from ansible_collections.blastorios.ovh.plugins.module_utils.ovh import (
        OVH,
        collection_module,
    )
    @collection_module(dict(service_name=dict(required=True)))
    def main(module: AnsibleModule, client: OVH, service_name: str):
        ...
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper():
            module_args = ovh_argument_spec()
            module_args.update(parameters)

            module = AnsibleModule(
                argument_spec=module_args,
                supports_check_mode=supports_check_mode,
                **kwargs,
            )
            client = OVH(module)

            # Extract parameters and pass as arguments
            params = {key: module.params[key] for key in parameters}

            if use_default_check_mode and module.check_mode:
                module_path = getfile(func)
                module_name = module_path.split("/")[-1].replace(".py", "")
                module.exit_json(
                    msg=f"(DRY RUN) Called .{module_name} using the following parameters:",
                    **params,
                    changed=False,
                )
            return func(module, client, **params)

        return wrapper

    return decorator
