import logging
from typing import Dict

from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import RequestMicroService

logger = logging.getLogger(__name__)


class ForwardAuthorizationParams(RequestMicroService):
    """
    This Satosa microservice picks configured properties from request
    and forwards them using context under 'params_to_forward' property. Optionally,
    it can add default params with preconfigured values for certain IdPs and SPs.
    params passed via HTTP GET and POST requests are prioritized over default ones
    from config in case of a conflict.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("ForwardAuthorizationParams is active")

        self.__param_names_to_forward = config.get(
            "param_names_to_forward", ["session_started_with"]
        )
        self.__default_values = config.get("default_values", [])

    def apply_default_values(
        self, data: InternalData, params_to_forward: Dict[str, str]
    ) -> None:
        current_idp = data.auth_info["issuer"]
        current_sp = data.requester

        idps_to_forward = ["", current_idp]
        sps_to_forward = ["", current_sp]

        for default_value in self.__default_values:
            if (
                default_value["idp"] in idps_to_forward
                and default_value["sp"] in sps_to_forward
            ):
                param_to_forward = default_value["param"]
                params_to_forward.update(param_to_forward)

    def extract_params_to_forward(
        self, context: Context, context_params_to_forward: Dict[str, str]
    ) -> None:
        for param_name_to_forward in self.__param_names_to_forward:
            #  For GET methods
            if context.qs_params:
                param_value_to_forward = context.qs_params.get(param_name_to_forward)
            # For POST methods
            elif context.request:
                param_value_to_forward = context.request.get(param_name_to_forward)
            else:
                param_value_to_forward = None

            # Overwriting of default values can happen here
            if param_value_to_forward:
                context_params_to_forward[
                    param_name_to_forward
                ] = param_value_to_forward

    def add_params_to_context(
        self, context: Context, context_params_to_forward: Dict[str, str]
    ):
        state_auth_req_params = context.state.get(Context.KEY_AUTH_REQ_PARAMS) or {}
        context_auth_req_params = (
            context.get_decoration(Context.KEY_AUTH_REQ_PARAMS) or {}
        )

        for k, v in context_params_to_forward.items():
            state_auth_req_params[k] = v
            context_auth_req_params[k] = v

        context.state[Context.KEY_AUTH_REQ_PARAMS] = state_auth_req_params
        context.decorate(Context.KEY_AUTH_REQ_PARAMS, context_auth_req_params)

    def process(self, context: Context, data: InternalData):
        # Prevent forwarding of default values in case of unsupported HTTP method
        if context.request_method not in ["GET", "POST"]:
            return super().process(context, data)

        context_params_to_forward = {}
        self.apply_default_values(data, context_params_to_forward)
        self.extract_params_to_forward(context, context_params_to_forward)
        self.add_params_to_context(context, context_params_to_forward)

        return super().process(context, data)
