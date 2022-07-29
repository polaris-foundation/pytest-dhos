import pytest

from . import jwt_permissions


@pytest.fixture(autouse=True)
def jwt_scopes():
    "parametrize to scopes required by a test"
    return None


@pytest.fixture
def jwt_system(app_context, jwt_scopes):
    """Use this fixture to make requests as a system"""
    from flask import g

    g.jwt_claims = {"system_id": "dhos-robot"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.SYSTEM_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["system_id"]


@pytest.fixture
def jwt_send_admin_uuid(app_context, jwt_scopes):
    """Use this fixture to make requests as a SEND administrator"""
    from flask import g

    g.jwt_claims = {"clinician_id": "some-clinician-uuid"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.SEND_ADMIN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["clinician_id"]


@pytest.fixture
def jwt_gdm_admin_uuid(app_context, jwt_scopes):
    """Use this fixture to make requests as a GDM administrator"""
    from flask import g

    g.jwt_claims = {"clinician_id": "some-gdm-clinician-uuid"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.GDM_ADMIN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["clinician_id"]


@pytest.fixture
def jwt_send_clinician_uuid(app_context, jwt_scopes):
    """Use this fixture to make requests as a SEND clinician"""
    from flask import g

    g.jwt_claims = {"clinician_id": "some-clinician-uuid"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.SEND_CLINICIAN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["clinician_id"]


@pytest.fixture
def jwt_gdm_clinician_uuid(app_context, jwt_scopes):
    """Use this fixture to make requests as a GDM clinician"""
    from flask import g

    g.jwt_claims = {"clinician_id": "some-gdm-clinician-uuid"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.GDM_CLINICIAN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["clinician_id"]


@pytest.fixture
def jwt_send_superclinician_uuid(app_context, jwt_scopes):
    """Use this fixture to make requests as a SEND superclinician"""
    from flask import g

    g.jwt_claims = {"clinician_id": "some-clinician-uuid"}
    if jwt_scopes is None:
        g.jwt_scopes = jwt_permissions.SEND_SUPERCLINICIAN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return g.jwt_claims["clinician_id"]
