from satosa.micro_services.base import ResponseMicroService
from satosacontrib.perun.utils.EntitlementUtils import EntitlementUtils
from satosacontrib.perun.utils.Utils import Utils
from satosacontrib.perun.utils.ConfigStore import ConfigStore


class Entitlement(ResponseMicroService):

    """This Satosa microservice joins
    eduPersonEntitlement, forwardedEduPersonEntitlement,
    resource capabilities and facility capabilities"""

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__utils = EntitlementUtils(config)
        self.__global_cfg = ConfigStore.get_global_cfg(config["global_cfg_path"])
        self.__allowed_requesters = self.__global_cfg.get("allowed_requesters", {})

    def process(self, context, data):
        """
        This is where the micro service should modify the request / response.
        Subclasses must call this method (or in another way make sure the
        next callable is called).

        @param context: The current context
        @param data: Data to be modified
        """
        if not Utils.allow_by_requester(context, data, self.__allowed_requesters):
            return super().process(context, data)

        data = self.__utils.update_entitlements(data)
        return super().process(context, data)
