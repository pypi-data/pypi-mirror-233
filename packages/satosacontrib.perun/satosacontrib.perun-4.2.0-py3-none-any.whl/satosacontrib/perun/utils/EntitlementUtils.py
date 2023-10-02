import os
from re import sub
from typing import Optional
from urllib.parse import quote

import yaml
from natsort import natsorted
from perun.connector import Facility, AdaptersManager
from perun.connector.utils.Logger import Logger
from satosa.exception import SATOSAError
from satosa.internal import InternalData

from satosacontrib.perun.utils.ConfigStore import ConfigStore
from satosacontrib.perun.utils.Utils import Utils


def encode_entitlement(group_name):
    return quote(group_name, safe="!$'()*,;&=@:+")


def encode_name(name):
    return quote(name, safe="!'()*")


class EntitlementUtils:
    __config_path = "/etc/satosa/plugins/microservices/perun_entitlement_idm.yaml"

    def __load_cfg(self):
        if not os.path.exists(self.__config_path):
            raise Exception("Config: missing config file: ", self.__config_path)
        with open(self.__config_path, "r") as f:
            return yaml.safe_load(f)

    def __init__(self, config=None):
        self.__logger = Logger.get_logger(self.__class__.__name__)
        self.__DEBUG_PREFIX = self.__class__.__name__
        self.OUTPUT_ATTR_NAME = "output_attr_name"
        self.RELEASE_FORWARDED_ENTITLEMENT = "release_forwarded_entitlement"
        self.FORWARDED_EDUPERSON_ENTITLEMENT = "forwarded_eduperson_entitlement"
        self.ENTITLEMENT_PREFIX_ATTR = "entitlement_prefix"
        self.ENTITLEMENT_AUTHORITY_ATTR = "entitlement_authority"
        self.GROUP_NAME_AARC_ATTR = "group_name_AARC"
        self.GROUP_ENTITLEMENT_DISABLED_ATTR = "group_entitlement_disabled"

        if config is None:
            config = self.__load_cfg()
        self.__config = config

        self.__group_mapping = self.__config.get("group_mapping")
        self.__extended = self.__config.get("entitlement_extended", False) in [
            True,
            "True",
            "true",
            "1",
            1,
        ]

        self.__global_cfg = ConfigStore.get_global_cfg(config.get("global_cfg_path"))

        self.__attr_map_cfg = ConfigStore.get_attributes_map(
            self.__global_cfg["attrs_cfg_path"]
        )

        self.__adapters_manager = AdaptersManager(
            self.__global_cfg["adapters_manager"], self.__attr_map_cfg
        )

        # TODO maybe use inheritance EntitlementUtils(Utils) instead of this instance
        self.__utils = Utils(self.__adapters_manager)

        self.__output_attr_name = self.__config.get(
            self.OUTPUT_ATTR_NAME, "eduperson_entitlement"
        )

        self.__release_forwarded_entitlement = self.__config.get(
            self.RELEASE_FORWARDED_ENTITLEMENT, True
        )

        self.__forwarded_eduperson_entitlement = self.__config.get(
            self.FORWARDED_EDUPERSON_ENTITLEMENT
        )

        self.__group_name_aarc = self.__config.get(self.GROUP_NAME_AARC_ATTR)

        self.__entitlement_prefix = self.__config.get(self.ENTITLEMENT_PREFIX_ATTR)

        self.__entitlement_authority = self.__config.get(
            self.ENTITLEMENT_AUTHORITY_ATTR
        )

        self.__group_entitlement_disabled = self.__config.get(
            self.GROUP_ENTITLEMENT_DISABLED_ATTR
        )

    def update_entitlements(self, data: InternalData):
        """
        This method updates all entitlement related data stored in `data`

        @param data: Data to be modified
        @return: list of entitlements
        """
        eduperson_entitlement = []
        eduperson_entitlement_extended = []
        capabilities = []
        forwarded_eduperson_entitlement = []
        if data.data["perun"]["groups"]:
            if not self.__extended:
                eduperson_entitlement = self.__get_eduperson_entitlement(data)
            else:
                eduperson_entitlement_extended = (
                    self.__get_eduperson_entitlement_extended(data)
                )

            capabilities = self.__get_capabilities(data)

        else:
            self.__logger.debug(
                "perun:Entitlement: There are no user "
                "groups assigned to facility. => Skipping "
                "getEduPersonEntitlement and getCapabilities"
            )

        if self.__release_forwarded_entitlement:
            forwarded_eduperson_entitlement = (
                self.__get_forwarded_eduperson_entitlement(
                    data,
                )
            )

        values = data.attributes.get(self.__output_attr_name, [])
        values = values + (
            eduperson_entitlement_extended if self.__extended else eduperson_entitlement
        )
        values = values + forwarded_eduperson_entitlement
        values = values + capabilities
        values = list(set(values))
        data.attributes[self.__output_attr_name] = values
        return data

    def __get_facility_from_sp(self, data: InternalData) -> Optional[Facility]:
        rp_id = data.requester
        facility = self.__adapters_manager.get_facility_by_rp_identifier(rp_id)

        if not facility:
            self.__logger.debug(
                f"No facility found for SP '{data.requester}', skipping "
                "processing filter."
            )

        return facility

    def __get_eduperson_entitlement(self, data):
        """
        This method gets entitlements of groups stored in `data`

        @param data: Data to be modified
        @return: list of entitlements
        """

        eduperson_entitlement = []

        facility = self.__get_facility_from_sp(data)
        user_id = data.attributes.get(self.__global_cfg["perun_user_id_attribute"])
        if facility and user_id:
            eligible_groups = self.__utils.get_eligible_groups(
                facility, user_id, self.__group_entitlement_disabled
            )
            for group in eligible_groups:
                group_name = group.unique_name
                group_name = sub(r"^(\w*):members$", r"\1", group_name)

                if self.__config["group_name_AARC"] or self.__group_name_aarc:
                    if (
                        not self.__entitlement_authority
                        or not self.__entitlement_prefix
                    ):
                        raise SATOSAError(
                            "perun:Entitlement: missing "
                            "mandatory configuration options "
                            "'groupNameAuthority' "
                            "or 'groupNamePrefix'."
                        )

                    group_name = self.__group_name_wrapper(group_name)
                else:
                    group_name = self.__map_group_name(group_name, data.requester)

                eduperson_entitlement.append(group_name)

        natsorted(eduperson_entitlement)

        return eduperson_entitlement

    def __get_eduperson_entitlement_extended(self, data: InternalData):
        """
        This method gets entitlements of groups stored in `data`
        in extended mode

        @param data: Data to be modified
        @return: list of entitlements
        """

        eduperson_entitlement_extended = []

        groups = data.data["perun"]["groups"]
        for group in groups:
            entitlement = self.__group_entitlement_wrapper(group.uuid)

            eduperson_entitlement_extended.append(entitlement)

            group_name = group.unique_name
            group_name = sub(r"^(\w*):members$", r"\1", group_name)

            entitlement_with_attributes = (
                self.__group_entitlement_with_attributes_wrapper(group.uuid, group_name)
            )
            eduperson_entitlement_extended.append(entitlement_with_attributes)

        natsorted(eduperson_entitlement_extended)
        return eduperson_entitlement_extended

    def __get_forwarded_eduperson_entitlement(self, data):
        """
        This method gets forwarded_eduperson_entitlement
        based on the user in `data`

        @param data: Data to be modified
        @return: list of forwarded edu person entitlements
        """

        result = []

        user_id = data.attributes.get(self.__global_cfg["perun_user_id_attribute"])
        if not user_id:
            self.__logger.debug(
                "perun:Entitlement: Perun User Id is not "
                "specified. => Skipping getting forwardedEntitlement."
            )

            return result

        forwarded_eduperson_entitlement_map = dict()

        try:
            forwarded_eduperson_entitlement_map = (
                self.__adapters_manager.get_user_attributes(
                    user_id, [self.__forwarded_eduperson_entitlement]
                )
            )
        except Exception as e:
            self.__logger.debug(
                "perun:Entitlement: Exception "
                + str(e)
                + " was thrown in method 'getForwardedEduPersonEntitlement'."
            )

        if forwarded_eduperson_entitlement_map:
            result = [list(forwarded_eduperson_entitlement_map.values())[0]]

        return result

    def __get_capabilities(self, data):
        """
        This method gets forwarded_eduperson_entitlement
        based on the user in `data`

        @param data: Data to be modified
        @return: list of forwarded edu person entitlements
        """

        resource_capabilities = []
        facility_capabilities = []
        capabilities_result = []

        try:
            resource_capabilities = (
                self.__adapters_manager.get_resource_capabilities_by_rp_id(
                    data.requester, data.data["perun"]["groups"]
                )
            )

            facility_capabilities = (
                self.__adapters_manager.get_facility_capabilities_by_rp_id(
                    data.requester
                )
            )

        except Exception as e:
            self.__logger.warning(
                "perun:EntitlementUtilss: Exception "
                + str(e)
                + " was thrown in method 'getCapabilities'."
            )

        capabilities = list(set(facility_capabilities + resource_capabilities))

        for capability in capabilities:
            wrapped_capability = self.__capabilities_wrapper(capability)
            capabilities_result.append(wrapped_capability)

        return capabilities_result

    def __map_group_name(self, group_name, requester):
        """
        This method translates given name of group based on
        'groupMapping' in config

        @param group_name: given name of group
        @return: mapped group name
        """

        if (
            requester in self.__group_mapping
            and group_name in self.__group_mapping[requester]
            and self.__group_mapping[requester][group_name]
        ):
            self.__logger.debug(
                "Mapping "
                + group_name
                + " to "
                + self.__group_mapping[requester][group_name]
            )

            return self.__group_mapping[requester][group_name]

        self.__logger.debug(
            "No mapping found for group " + group_name + " for entity " + requester
        )

        return self.__entitlement_prefix + "group:" + group_name

    def __group_name_wrapper(self, group_name):
        return "{prefix}group:{name}#{authority}".format(
            prefix=self.__entitlement_prefix,
            name=encode_entitlement(group_name),
            authority=self.__entitlement_authority,
        )

    def __capabilities_wrapper(self, capabilities):
        return "{prefix}{capabilities}#{authority}".format(
            prefix=self.__entitlement_prefix,
            capabilities=encode_entitlement(capabilities),
            authority=self.__entitlement_authority,
        )

    def __group_entitlement_wrapper(self, uuid):
        return "{prefix}group{uuid}#{authority}".format(
            prefix=self.__entitlement_prefix,
            uuid=encode_name(uuid),
            authority=self.__entitlement_authority,
        )

    def __group_entitlement_with_attributes_wrapper(self, group_uuid, group_name):
        return (
            "{prefix}groupAttributes:{uuid}?=displayName={name}#{"
            "authority}".format(
                prefix=self.__entitlement_prefix,
                uuid=group_uuid,
                name=encode_name(group_name),
                authority=self.__entitlement_authority,
            )
        )
