import logging
from satosa.micro_services.base import ResponseMicroService
from saml2.saml import NAMEID_FORMAT_PERSISTENT

logger = logging.getLogger(__name__)


class NameIDAttribute(ResponseMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("NameIDAttribute is active")
        self.__sp_entity_id = config["sp_entity_id"]
        self.__subject_attribute = config.get("subject_attribute", None)
        # deprecated way of setting name_id attribute using a single value
        self.__nameid_attribute = config.get("nameid_attribute", None)
        # current way of setting name_id attribute using a dictionary
        self.__nameid_attributes = config.get("nameid_attributes", None)

    def assign_auth_info(self, data, nameid_attribute, nameid_format):
        if data.subject_type == nameid_format and data.subject_id:
            data.attributes[nameid_attribute] = "{}!{}!{}".format(
                data["auth_info"]["issuer"], self.__sp_entity_id, data.subject_id
            )

    def process(self, context, data):
        """
        Copy SAML nameID to an internal attribute.
        :param context: request context
        :param data: the internal request
        """
        if self.__nameid_attributes:
            for nameid_format, nameid_attribute in self.__nameid_attributes.items():
                self.assign_auth_info(data, nameid_attribute, nameid_format)
        elif self.__nameid_attribute:
            self.assign_auth_info(
                data, self.__nameid_attribute, NAMEID_FORMAT_PERSISTENT
            )

        if self.__subject_attribute:
            # instead of e.g. user_id_from_attrs: [publicid]
            data.subject_id = data.attributes[self.__subject_attribute][0]

        return super().process(context, data)
