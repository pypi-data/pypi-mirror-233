from unittest.mock import patch, MagicMock

import pytest
from perun.connector.adapters.AdaptersManager import AdaptersManager
from perun.connector.models.Group import Group
from perun.connector.models.User import User
from perun.connector.models.VO import VO

from satosacontrib.perun.utils.ConfigStore import ConfigStore
from satosacontrib.perun.utils.EntitlementUtils import EntitlementUtils
from satosacontrib.perun.utils.Utils import Utils
from tests.test_microservice_loader import Loader, TestContext, TestData

TEST_VO = VO(1, "vo", "vo_short_name")
TEST_GROUP_1 = Group(1, TEST_VO, "uuid", "group1", "group1", "")
TEST_GROUP_2 = Group(2, TEST_VO, "uuid", "group2", "group2", "")

DATA = {
    "perun": {"groups": [TEST_GROUP_1, TEST_GROUP_2], "user": User(1, "name")},
    "attributes": {},
}

DATA_WITHOUT_USER = {
    "perun": {
        "groups": ["grp1", "grp2"],
    }
}

TEST_CONTEXT = TestContext()

CONFIG = {
    "entitlement_extended": False,
    "global_cfg_path": "path",
    "group_name_AARC": "group_name_AARC",
    "group_mapping": {
        "entity_id_1": {"group1": "mapped_group1", "group2": "mapped_group2"},
        "entity_id_2": {"group1": "mapped_group1"},
        "entity_id_3": {"default_group": "default_group_mapped"},
    },
    "entitlement_prefix": "prefix:",
    "entitlement_authority": "authority",
}

CONFIG_EXTENDED = {
    "entitlement_extended": True,
    "global_cfg_path": "path",
    "group_name_AARC": "group_name_AARC",
    "group_mapping": {
        "entity_id_1": {"group1": "mapped_group1", "group2": "mapped_group2"},
        "entity_id_2": {"group1": "mapped_group1"},
        "entity_id_3": {"default_group": "default_group_mapped"},
    },
    "entitlement_prefix": "prefix:",
    "entitlement_authority": "authority",
}

CONFIG_2 = {
    "entitlement_extended": "true",
    "global_cfg_path": "path",
    "group_name_AARC": "groupN=_name_AARC",
    "group_mapping": {
        "entity_id_1": {"group1": "mapped_group1", "group2": "mapped_group2"},
        "entity_id_2": {"group1": "mapped_group1"},
        "entity_id_3": {"default_group": "default_group_mapped"},
    },
    "entitlement_prefix": None,
    "entitlement_authority": "authority",
}

CONFIG_3 = {
    "entitlement_extended": "true",
    "global_cfg_path": "path",
    "group_name_AARC": "group_name_AARC",
    "group_mapping": {
        "entity_id_1": {"group1": "mapped_group1", "group2": "mapped_group2"},
        "entity_id_2": {"group1": "mapped_group1"},
        "entity_id_3": {"default_group": "default_group_mapped"},
    },
    "entitlement_prefix": "prefix:",
    "entitlement_authority": None,
}


@patch("satosacontrib.perun.utils.ConfigStore.ConfigStore.get_global_cfg")
@patch("satosacontrib.perun.utils.ConfigStore.ConfigStore.get_attributes_map")
@patch("perun.connector.adapters.AdaptersManager.AdaptersManager.__init__")
def create_mocked_EntUt_instance(mock_request, mock_request2, mock_request3, config):
    ConfigStore.get_global_cfg = MagicMock(return_value=Loader.GLOBAL_CONFIG)
    ConfigStore.get_attributes_map = MagicMock(return_value=None)
    AdaptersManager.__init__ = MagicMock(return_value=None)
    return EntitlementUtils(config)


TEST_INSTANCE = create_mocked_EntUt_instance(config=CONFIG)

TEST_INSTANCE_WITHOUT_PREFIX = create_mocked_EntUt_instance(config=CONFIG_2)
TEST_INSTANCE_WITHOUT_AUTHORITY = create_mocked_EntUt_instance(config=CONFIG_3)


def test_map_group_name():
    group_name_1 = "group1"
    group_name_2 = "group2"
    not_existing_group = "group420"

    result_1 = "mapped_group1"
    result_2 = "mapped_group2"
    result_3 = "prefix:group:group420"

    assert (
        TEST_INSTANCE._EntitlementUtils__map_group_name(group_name_1, "entity_id_1")
        == result_1
    )
    assert (
        TEST_INSTANCE._EntitlementUtils__map_group_name(group_name_2, "entity_id_1")
        == result_2
    )
    assert (
        TEST_INSTANCE._EntitlementUtils__map_group_name(
            not_existing_group, "entity_id_1"
        )
        == result_3
    )


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_resource_capabilities_by_rp_id"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_facility_capabilities_by_rp_id"
)
def test_get_capabilities(mock_request_1, mock_request_2):
    resource_capabilities = ["res_cap_1", "res_cap_2"]
    facility_capabilities = ["fac_cap_1", "fac_cap_2"]

    AdaptersManager.get_resource_capabilities_by_rp_id = MagicMock(
        return_value=resource_capabilities
    )
    AdaptersManager.get_facility_capabilities_by_rp_id = MagicMock(
        return_value=facility_capabilities
    )

    result = [
        "prefix:fac_cap_2#authority",
        "prefix:fac_cap_1#authority",
        "prefix:res_cap_1#authority",
        "prefix:res_cap_2#authority",
    ]

    for capability in TEST_INSTANCE._EntitlementUtils__get_capabilities(
        TestData(DATA, None)
    ):
        assert capability in result


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_resource_capabilities_by_rp_id"
)
def test_get_capabilities_exception(mock_request_1):
    AdaptersManager.get_resource_capabilities_by_rp_id = MagicMock(
        side_effect=[Exception("sth went wrong")]
    )

    assert TEST_INSTANCE._EntitlementUtils__get_capabilities(TestData(DATA, None)) == []


def test_get_forwarded_eduperson_entitlement_user_missing():
    attrs = {"example_user_id": "example_user_id"}

    test_data = TestData(data=DATA_WITHOUT_USER, attributes=attrs)
    assert not TEST_INSTANCE._EntitlementUtils__get_forwarded_eduperson_entitlement(
        test_data
    )


@patch("perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_attributes")
def test_get_forwarded_eduperson_entitlement(mock_request):
    ext_src_attrs = {"attr1": "this_is_entitlement", "attr2": "attr2", "attr3": "attr3"}

    attrs = {"example_user_id": "example_user_id"}

    test_data = TestData(data=DATA, attributes=attrs)

    result = ["this_is_entitlement"]
    AdaptersManager.get_user_attributes = MagicMock(return_value=ext_src_attrs)

    assert (
        TEST_INSTANCE._EntitlementUtils__get_forwarded_eduperson_entitlement(test_data)
        == result
    )


def test_get_eduperson_entitlement_extended():
    expected_result = [
        "prefix:groupuuid#authority",
        "prefix:groupAttributes:uuid?=displayName=group1#authority",  # noqa
        "prefix:groupuuid#authority",
        "prefix:groupAttributes:uuid?=displayName=group2#authority",
    ]  # noqa

    result = TEST_INSTANCE._EntitlementUtils__get_eduperson_entitlement_extended(
        TestData(DATA, None)
    )  # noqa

    assert expected_result == result


@patch("satosacontrib.perun.utils.Utils.AdaptersManager.get_facility_by_rp_identifier")
@patch("satosacontrib.perun.utils.Utils.Utils.get_eligible_groups")
def test_get_eduperson_entitlement(mock_request1, mock_request2):
    expected_result = ["prefix:group:group1#authority", "prefix:group:group2#authority"]

    AdaptersManager.get_facility_by_rp_identifier = MagicMock(
        return_value="example facility"
    )
    Utils.get_eligible_groups = MagicMock(return_value=DATA["perun"]["groups"])
    result = TEST_INSTANCE._EntitlementUtils__get_eduperson_entitlement(
        TestData(DATA, {"example_user_id": "user_id_attr"})
    )  # noqa

    assert result == expected_result


@patch("satosacontrib.perun.utils.Utils.AdaptersManager.get_facility_by_rp_identifier")
@patch("satosacontrib.perun.utils.Utils.Utils.get_eligible_groups")
def test_get_eduperson_entitlement_exception(mock_request1, mock_request2):
    AdaptersManager.get_facility_by_rp_identifier = MagicMock(
        return_value="example facility"
    )
    Utils.get_eligible_groups = MagicMock(return_value=DATA["perun"]["groups"])

    expected_error_message = (
        "perun:Entitlement: missing "
        "mandatory configuration options "
        "'groupNameAuthority' "
        "or 'groupNamePrefix'."
    )
    with pytest.raises(Exception) as error:
        _ = TEST_INSTANCE_WITHOUT_PREFIX._EntitlementUtils__get_eduperson_entitlement(
            TestData(DATA, {"example_user_id": "user_id_attr"})
        )

    assert str(error.value.args[0]) == expected_error_message

    with pytest.raises(Exception) as error:
        _ = TEST_INSTANCE_WITHOUT_AUTHORITY._EntitlementUtils__get_eduperson_entitlement(
            TestData(DATA, {"example_user_id": "user_id_attr"})
        )

    assert str(error.value.args[0]) == expected_error_message
