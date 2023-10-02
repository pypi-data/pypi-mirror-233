from collections import Counter
from typing import List, Any
from unittest.mock import patch, MagicMock

from perun.connector import Group, VO, Resource, Facility, User, AdaptersManager

from satosacontrib.perun.utils.Utils import Utils

TEST_VO = VO(1, "vo", "vo_short_name")
GROUP_1 = Group(1, TEST_VO, "uuid1", "group1", "group_1", "")
GROUP_2 = Group(2, TEST_VO, "uuid2", "group2", "group_2", "")
GROUP_3 = Group(3, TEST_VO, "uuid3", "group3", "group_3", "")

USERS_GROUPS_ON_FACILITY = (GROUP_1, GROUP_2)

USER = User(1, "John Doe")
FACILITY = Facility(1, "example_name", "example_description", "example_rp_id", [])
APPLICABLE_RESOURCE_1 = Resource(1, TEST_VO, FACILITY, "applicable_1")
APPLICABLE_RESOURCE_2 = Resource(2, TEST_VO, FACILITY, "applicable_2")
APPLICABLE_RESOURCE_3 = Resource(3, TEST_VO, FACILITY, "applicable_3")
NON_APPLICABLE_RESOURCE_1 = Resource(4, TEST_VO, FACILITY, "non_applicable_1")
RESOURCES_ON_FACILITY = [
    APPLICABLE_RESOURCE_1,
    APPLICABLE_RESOURCE_2,
    NON_APPLICABLE_RESOURCE_1,
]


@patch("perun.connector.adapters.AdaptersManager.AdaptersManager.__init__")
def create_mocked_utils_instance(mock_request_1):
    AdaptersManager.__init__ = MagicMock(return_value=None)
    adapters_manager_mock = AdaptersManager({}, {})

    return Utils(adapters_manager_mock)


TEST_INSTANCE = create_mocked_utils_instance()


def are_equal_lists(lst1: List[Any], lst2: List[Any]) -> bool:
    return Counter(lst1) == Counter(lst2)


def get_resource_applicability_attr(resource: Resource, _: str):
    is_disabled = "non_applicable" in resource.name
    return {"isDisabled": is_disabled}


def get_groups_for_resource(resouce: Resource):
    resource_groups = {
        APPLICABLE_RESOURCE_1: [GROUP_1],
        APPLICABLE_RESOURCE_2: [GROUP_3],
        NON_APPLICABLE_RESOURCE_1: [GROUP_2],
    }

    return resource_groups[resouce]


"""
Legend:
APPLICABLE RESOURCE - R_APP
NON-APPLICABLE RESOURCE (DISABLED BY ATTRIBUTE) - R_NON
GROUP - G

We test all possibilities in this test:

- facility has associated resources [R_APP_1, R_APP_2, R_APP_3, R_NON_1]
- resources are associated with groups {
    R_APP_1: G_1, ✓
    R_APP_2: G_3, ✓
    R_NON_1: G_2  ˟
    }
- groups sourced from resources which are not disabled are [G_1, G_3] (marked with ✓)
- user belongs to groups [G_1, G_2]
- groups passing the filter are {G_1, G_2} ∩ {G_1, G_3} = {G_1}
- {G_1} is the only eligible group passing all the restrictions
"""


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_users_groups_on_facility"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_resources_for_facility"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_resource_attributes"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_groups_for_resource"
)
def test_get_eligible_groups_attribute_provided_filtered_groups(
    mock_request_1, mock_request_2, mock_request_3, mock_request_4
):
    AdaptersManager.get_users_groups_on_facility = MagicMock(
        return_value=USERS_GROUPS_ON_FACILITY
    )
    AdaptersManager.get_resources_for_facility = MagicMock(
        return_value=RESOURCES_ON_FACILITY
    )
    AdaptersManager.get_resource_attributes = MagicMock(
        side_effect=get_resource_applicability_attr
    )
    AdaptersManager.get_groups_for_resource = MagicMock(
        side_effect=get_groups_for_resource
    )

    eligible_groups = TEST_INSTANCE.get_eligible_groups(
        FACILITY, USER, "mock_applicability_attr_name"
    )
    eligible_groups = [group.name for group in eligible_groups]
    expected_eligible_groups = [GROUP_1.name]

    assert Counter(expected_eligible_groups) == Counter(eligible_groups)


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_users_groups_on_facility"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_resources_for_facility"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_resource_attributes"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager"
    ".get_groups_for_resource"
)
def test_get_eligible_groups_attribute_not_provided_filtering_skipped(
    mock_request_1, mock_request_2, mock_request_3, mock_request_4
):
    AdaptersManager.get_users_groups_on_facility = MagicMock(
        return_value=USERS_GROUPS_ON_FACILITY
    )
    AdaptersManager.get_resources_for_facility = MagicMock(
        return_value=RESOURCES_ON_FACILITY
    )
    AdaptersManager.get_resource_attributes = MagicMock(
        side_effect=get_resource_applicability_attr
    )
    AdaptersManager.get_groups_for_resource = MagicMock(
        side_effect=get_groups_for_resource
    )

    eligible_groups = TEST_INSTANCE.get_eligible_groups(FACILITY, USER, None)
    eligible_groups = [group.name for group in eligible_groups]
    expected_eligible_groups = [GROUP_1.name, GROUP_2.name]

    assert Counter(expected_eligible_groups) == Counter(eligible_groups)
