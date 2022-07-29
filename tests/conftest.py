import os
import signal
import socket
import sys
import time
from urllib.parse import urlparse

import pytest

pytest_plugins = ["pytester"]


def pytest_configure(config):
    for env_var, tox_var in [
        ("NEO4J_DB_PORT", "NEO4J_7687_TCP_PORT"),
        ("NEO4J_DB_BROWSER_PORT", "NEO4J_7474_TCP_PORT"),
        ("NEO$NEO4J_DB_BROWSER_PORT", "NEO4J_7474_TCP_PORT"),
        ("NEO4J_DB_URL", "NEO4J_HOST"),
    ]:
        if tox_var in os.environ:
            os.environ[env_var] = os.environ.get(tox_var)

    # # f-b-i will have already been imported at this point, so we have to update
    # # the configured database url.
    # import neomodel.config
    # from flask_batteries_included.config import Neo4jConfig
    #
    # config = Neo4jConfig()
    # neomodel.config.DATABASE_URL = config.NEO4J_DATABASE_URI
    # print(f"DATABASE_URL {config.NEO4J_DATABASE_URI}")


def _wait_for_it(service, timeout=30):
    url = urlparse(service, scheme="http")

    host = url.hostname
    port = url.port or (443 if url.scheme == "https" else 80)

    friendly_name = f"{host}:{port}"

    def _handle_timeout(signum, frame):
        print(f"timeout occurred after waiting {timeout} seconds for {friendly_name}")
        sys.exit(1)

    if timeout > 0:
        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.alarm(timeout)
        print(f"waiting {timeout} seconds for {friendly_name}")
    else:
        print(f"waiting for {friendly_name} without a timeout")

    t1 = time.time()

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = sock.connect_ex((host, port))
            if s == 0:
                seconds = round(time.time() - t1)
                print(f"{friendly_name} is available after {seconds} seconds")
                break
        except socket.gaierror:
            pass
        finally:
            time.sleep(1)

    signal.alarm(0)


@pytest.fixture(scope="session", autouse=True)
def wait_for_neo4j(request):
    # Wait for neo4j to have fully started
    host = os.getenv("NEO4J_DB_URL", "localhost")
    port = os.getenv("NEO4J_DB_BROWSER_PORT", "7474")
    print(f"Wait for //{host}:{port}")
    _wait_for_it(f"//{host}:{port}", 30)


@pytest.fixture
def testdir(testdir):
    rc_path = os.path.join(os.path.dirname(__file__), os.pardir, ".coveragerc")
    os.environ["COVERAGE_PROCESS_START"] = os.path.normpath(rc_path)

    sitecustomize = """
        import coverage; coverage.process_startup()
    """
    testdir.makepyfile(sitecustomize=sitecustomize)

    return testdir
