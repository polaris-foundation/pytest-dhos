import pytest

TEST_CONFTEST = """
        import pytest

        @pytest.fixture
        def app():
            from flask_batteries_included import create_app
            return create_app(testing=True)

        @pytest.fixture
        def app_context(app):
            with app.app_context():
                yield

"""

TEST_TOXINI = """
[testenv]
envdir = {toxworkdir}/py37

setenv = ENVIRONMENT = DEVELOPMENT
         AUTH0_AUDIENCE = https://dhos-dev.draysonhealth.com/
         IGNORE_JWT_VALIDATION = True
         HS_KEY = secret
         PROXY_URL = http://localhost
         EPR_SERVICE_ADAPTER_ISSUER = https://epr.dev.sensynehealth.com/
         REDIS_INSTALLED=False
"""


@pytest.mark.parametrize(
    "fixture,test_scope",
    [
        ("jwt_system", "read:location_by_ods"),
        ("jwt_send_admin_uuid", "read:send_clinician_all"),
        ("jwt_gdm_admin_uuid", "read:gdm_clinician_all"),
        ("jwt_send_clinician_uuid", "read:send_clinician"),
        ("jwt_gdm_clinician_uuid", "read:gdm_patient"),
        ("jwt_send_superclinician_uuid", "read:send_clinician_temp"),
    ],
)
def test_clinician_scopes(testdir, fixture, test_scope):
    testdir.makeini(TEST_TOXINI)
    testdir.makepyfile(
        f"""
        import pytest


        @pytest.mark.parametrize("jwt_scopes, expected", [
            (None, [{test_scope!r}]),
            ("read:foo,write:bar", ["read:foo", "write:bar"])
        ], ids=['default-scopes','custom-scopes'])
        def test_example({fixture}, app_context, jwt_scopes, expected):
            assert {fixture} is not None

            from flask import g
            for scope in expected:
                assert scope in g.jwt_scopes
        """,
        conftest=TEST_CONFTEST,
    )
    result = testdir.runpytest("--verbose")

    result.stdout.fnmatch_lines(
        r"""
        *test_example*default-scopes*PASSED*
        *test_example*custom-scopes*PASSED*
        """
    )


def test_clinicians(testdir):
    testdir.makeini(TEST_TOXINI)
    testdir.makepyfile(
        f"""
        import pytest

        def test_example(clinician, clinician2, clinician_temp):
            assert len(set(clinician, clinician2, clinician_temp)) == 3
        """,
        conftest=TEST_CONFTEST,
    )
    result = testdir.runpytest("--verbose")

    result.stdout.fnmatch_lines(
        r"""
        *test_example*ERROR*
        """
    )
