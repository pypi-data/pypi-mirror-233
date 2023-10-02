# satosacontrib.perun

Microservices for [SATOSA](https://github.com/IdentityPython/SATOSA) authentication
proxy, made by the Perun team.

## Backends

### Seznam backend

A backend for SATOSA which implements login
using [Seznam OAuth](https://partner.seznam.cz/seznam-oauth/).

Use the [example config](./example/plugins/backends/seznam.yaml) and fill in your client
ID and client secret.

## Microservices

### AuthSwitcher Lite

This request microservice takes ACRs (AuthnContextClassRefs in SAML, acr_values in OIDC)
from a frontend
and sets them as requested ACRs for the backends. It relies
on [SATOSA!419](https://github.com/IdentityPython/SATOSA/pull/419)

### Context attributes microservice

The microservice adds the target IdP data to attributes:

- display name
- logo
- target issuer

The [MetaInfoIssuer](https://github.com/SUNET/swamid-satosa/blob/main/src/swamid_plugins/metainfo/metainfo.py)
microservice needs to be run beforehand with the
following [patch](https://github.com/SUNET/swamid-satosa/compare/main...kofzera:swamid-satosa:add_collector_metadata.patch).
Another [patch](https://github.com/IdentityPython/SATOSA/compare/master...kofzera:SATOSA:decorate_context_with_metadata.patch)
is
also needed for the satosa package until they are incorporated into the upstream.

### Is banned microservice

The microservice connects to database storing user bans and redirects banned users to
configured URL.

### Persist authorization params microservice

This request microservice retrieves configured parameters from GET or POST request (if
available) and
stores the values to internal context state.

### Forward authorization params microservice

This request microservice retrieves configured parameters from GET or POST request (if
available) and
forwards them through a context parameter. Optionally, `default_values` can be
provided in the config file. These will be forwarded for configured SP and/or IdP if
not provided in the GET/POST request. If the parameter with preconfigured
default value is sent via GET/POST request anyway, the value form the request will be
used instead of the default.

### Session started with microservice

This Satosa microservice checks, if configured attribute's value is present
in "session_started_with" values (retrieved by Persist authorization params
microservice).
If so, adds attribute with configured name. The value is expected to be converted
to boolean by Attribute typing microservice.

### Compute eligibility microservice

The microservice obtains dict with format { eligiblility_type: <unix_timestamp> }
from the internal data and runs a function configured for the
given eligibility type. The config is of format `type: function_path`.

The function should have a following signature:  
`example_func(data: InternalData, *args, **kwargs) -> timestamp | bool`, and it either
returns `False` or
a new timestamp, in which case the time in the dictionary is
updated in internal data. It strongly relies on the PerunAttributes microservice to fill
the dict
beforehand. If you want to update eligibility in the IDM, use the UpdateUserExtSource
microservice.

### NameID Attribute microservice

This microservice copies SAML NameID to an internal attribute with preconfigured name (
and format).

It has two modes of operation. The deprecated way of configuring the microservice
requires the config to
include `nameid_attribute: saml2_nameid_persistent`, where `saml2_nameid_persistent`
stands for the name of the SAML NameID
attribute in format: `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`. The new way
of configuring this
microservice expects a dictionary named `nameid_attributes` containing items
like `saml2_nameid_format: saml2_nameid_attribute`. In case of the newer configuration,
both the format and attribute need
to be configured correctly in order for the NameID attribute to be copied to the
internal attribute.

If one of the ways to use the microservice is configured, it will be used. If both ways
are configured, the newer way of
configuration - dictionary, will be used.

Demonstrations of both ways of configuration are shown in the example config.

## Perun Microservices

Subpackage of microservices connecting to perun. These have to be allowed (or not
denied) for
a given combination of requester/target_entity in order to run.

### Additional Identifiers

Takes user attributes by config, checks values with regexes and creates hashes by
specified algorithm. Values prepared to hash are parsed into List of List of strings and
serialized with json. User ext source and user is found by mathing this hashes.
If not even one hash can be created, user will be redirected to error page.
If user is not found, he will be redirected to registration page.

This microservice does not update the user in Perun with new values. To update save
freshly computed values for the
current user, you need to run `update_user_ext_source` microservice.

[RFC - eduTEAMS Identifier Generation](https://docs.google.com/document/d/1UwnEnzFG6SM9cv6gx1AsjDXw09ZkUmkyl-NqcXg0OVo/edit#heading=h.y5g6a74d5ukn) <br/>
Differences between our soulution and RFC:

- the selections are represented as list of list of attributes values serialized to JSON
- all identifiers are hashed by same hash function and with same salt
- The user’s home IdP entity-id does not need to be part of selection
- hashed values can be scoped but does not have to be

### Entitlement

Calculates Perun user's entitlements by joining `eduPersonEntitlements`,
`forwardedEduPersonEntitlements`, resource capabilities and facility capabilities.

Without the `group_entitlement_disabled` attribute set, user's entitlements are
computed based on all user's groups on facility.

When `group_entitlement_disabled` is set, resources
which have this attribute set to `true` are excluded from the computation.
This means that for a group to be included in the computation,
it needs to be assigned through at least one resource without this attribute set to
`true`.

### SP Authorization

Provides group based access control.

Without the `proxy_access_control_disabled` attribute set, this microservice denies access
to users who are not members of any group assigned to any resource on the current
facility.

If the `proxy_access_control_disabled` attribute is defined in config, resources which
have this attribute set to true are excluded. Groups assigned to these resources are
not counted towards user's groups on the current facility. This means, that the user
has to be a member of at least one group assigned to a resource without this
attribute set.

This feature allows computing entitlements while excluding groups which should not be
allowed to access the current service.

## Addons for SATOSA-oidcop frontend

### userinfo_perun_updates

SATOSA by default caches user data in subsequent calls of the userinfo endpoint.
Thanks to this addon the data is loaded from Perun IDM on each call so they are always
up to date.
