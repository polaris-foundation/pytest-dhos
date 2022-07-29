# pytest-dhos
A pytest plugin library containing common pytest fixtures for Polaris projects.

* Initial setup for test environments
* Fixtures that may be reused in multiple DHOS projects

## Maintainers
The Polaris platform was created by Sensyne Health Ltd., and has now been made open-source. As a result, some of the
instructions, setup and configuration will no longer be relevant to third party contributors. For example, some of
the libraries used may not be publicly available, or docker images may not be accessible externally. In addition,
CICD pipelines may no longer function.

For now, Sensyne Health Ltd. and its employees are the maintainers of this repository.

## Installation

Include pytest-dhos as a dependency in test-requirements.txt or pyproject.toml

To develop new tests:

```
make dev-install
```

## Running the Tests

```
make test
```

## Running Coverage

Coverage should be 100%, but unfortunately when using pytest
to test a pytest plugin it doesn't record its own coverage correctly.
(This may be fixable but for now the required coverage has been deliberately
set low.)

```
make test-coverage
```

## Deploy

- bump the semvar `VERSION` in `setup.py`
- update the `RELEASE` notes
- ensure these are both committed to master
- create a GitHub release


```
make deploy
```

## Available fixtures

When installed in a project, this plugin reads tox.ini in the project folder and any environment
variables specified by tox.ini are set in the environment even if pytest is run outside of tox.
Also, if flask-batteries-included is available the environment variables are set in the flask
configuration before tests are loaded.

If the project includes flask-batteries, the following fixtures are made available:

* **jwt_scopes**
    parametrize to scopes required by a test

* **jwt_system**
    Use this fixture to make requests as a system

* **jwt_send_admin_uuid**
    Use this fixture to make requests as a SEND administrator

* **jwt_gdm_admin_uuid**
    Use this fixture to make requests as a GDM administrator

* **jwt_send_clinician_uuid**
    Use this fixture to make requests as a SEND clinician

* **jwt_gdm_clinician_uuid**
    Use this fixture to make requests as a GDM clinician

* **jwt_send_superclinician_uuid**
    Use this fixture to make requests as a SEND superclinician

* **node_factory**
    Fixture provding a factory to create an arbitrary neo4j node.
    The node will be automatically deleted at the end of the test.
    Usage: node_factory(node_name, **fields) -> uuid
* **location_uuid**
    Default location for SEND tests 'Tester Hospital'
* **gdm_location_uuid**
    Default location for GDM tests 'GdmTest Hospital'
* **clinician_factory**
    Fixture providing a factory to create clinicians.
    Usage: clinician_factory(first_name, last_name, nhs_smartcard, product_name='SEND',
         expiry=None, login_active=None, **fields) -> uuid
    All fields may be overridden with additional keyword parameters.
* **clinician**
    SEND clinician fixture: Jane Deer

* **gdm_clinician**
    GDM clinician fixture: Lou Rabbit

* **clinician2_uuid**
    SEND clinician fixture: Kate Wildcat

* **clinician_temp_uuid**
    SEND temporary clinician fixture: Lou Armadillo

* **relation_factory**
    Fixture providing a factory to create an arbitrary neo4j relation.
    Usage: `relation_factory(relation_name, from_uuid, to_uuid)`

* **neo4j_teardown_node**
    Fixture providing a function that marks neo4j nodes to be cleaned up at the end of the test
    `neo4j_teardown_node(uuid1, [uuid2, ...])`

* **location_factory**
    Fixture providing a factory to create locations.
    Usage: `location_factory(name, parent=None, product_name='SEND', **fields) -> uuid`
    If parent is None the display name is `"{name} Hospital"`, otherwise it is
    `"{name} Ward"` and the ods_code is set to a ward.
    All fields may be overridden with additional keyword parameters.
