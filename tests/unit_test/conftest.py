import pytest

# local application imports
import server


# constants
PATH_COMPETITIONS_TESTS = "tests/resources/test_competitions.json"
PATH_CLUBS_TESTS = "tests/resources/test_clubs.json"


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    yield client


@pytest.fixture
def info_for_testing(mocker):
    """
    Declaration of all information to pass
    tests with test data.
    """

    path_clubs_json = mocker.patch.object(
        server,
        'PATH_CLUBS',
        PATH_CLUBS_TESTS
    )
    path_competitions_json = mocker.patch.object(
        server,
        'PATH_COMPETITIONS',
        PATH_COMPETITIONS_TESTS
    )

    competitions = server.load_competitions()
    clubs = server.load_clubs()

    comp = mocker.patch.object(server, 'competitions', competitions)
    c = mocker.patch.object(server, 'clubs', clubs)

    data = {
        'competitions': comp,
        'clubs': c,
        'PATH_CLUBS': path_clubs_json,
        'PATH_COMPETITIONS': path_competitions_json
    }

    return data
