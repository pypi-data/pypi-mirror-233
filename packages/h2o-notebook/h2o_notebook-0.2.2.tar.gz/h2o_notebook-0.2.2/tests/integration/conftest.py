import pytest as pytest

import h2o_notebook


@pytest.fixture(scope="session")
def session():
    return h2o_notebook.Session()
