import pytest
import json
import os


@pytest.fixture
def match_set_1():
    with open(os.path.join(os.path.dirname(__file__), "data", "match_set_1.json"), "r") as f:
        matches = json.load(f)
    return matches

@pytest.fixture
def match_set_2():
    with open(os.path.join(os.path.dirname(__file__), "data", "match_set_2.json"), "r") as f:
        matches = json.load(f)
    return matches

@pytest.fixture
def league():
    with open(os.path.join(os.path.dirname(__file__), "data", "league.json"), "r") as f:
        league = json.load(f)
    return league


@pytest.fixture
def leagues():
    with open(os.path.join(os.path.dirname(__file__), "data", "leagues.json"), "r") as f:
        leagues = json.load(f)
    return leagues