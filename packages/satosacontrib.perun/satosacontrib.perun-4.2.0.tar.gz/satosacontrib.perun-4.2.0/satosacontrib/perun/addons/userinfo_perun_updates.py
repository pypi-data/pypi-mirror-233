from perun.connector.adapters.AdaptersManager import AdaptersManager
from satosacontrib.perun.utils.EntitlementUtils import EntitlementUtils


def update_userinfo(response, current, state):
    user_id = response["sub"]
    del response["sub"]
    updated = AdaptersManager.get_user_attributes(user_id, response)
    for key, value in updated.items():
        if value:
            response[key] = value
    response["sub"] = user_id

    entitlements = EntitlementUtils()
    response = entitlements.update_entitlements(response)
    return response


def add_support(endpoint, **kwargs):
    _userinfo_endp = endpoint["userinfo"]
    _userinfo_endp.post_parse_process.append(update_userinfo)
