import pytest
import database_functions as db


def test_initialize():
    db.initialize()
    assert db.__run_query('SELECT * FROM player') == []
    assert db.__run_query('SELECT * FROM score') == []


def test_get_player_id():
    db.initialize()
    players = {'test_1': 1, 'test_2': 2, 'test_3': 3}
    for player in players.keys():
        db.login(player)

    for username, player_id in players.items():
        assert player_id == db.get_player_id(username)


def test_insertion():
    db.initialize()
    players = {'test_1': 1, 'test_2': 2, 'test_3': 3}
    for player in players.keys():
        db.login(player)

    for test, expected_id in players.items():
        assert db.login(test) == expected_id


def test_insert_score():
    db.initialize()
    players = {'test_1': 1, 'test_2': 2, 'test_3': 3}
    for player in players:
        db.login(player)
    scores = {1: 101, 2: 202, 3: 303}
    for player_id, score in scores.items():
        db.insert_score(player_id, score)

    for player_id, score in scores.items():
        query = '''SELECT score FROM score WHERE Player_ID = %s LIMIT 1''' % player_id
        assert db.__run_query(query)[0][0] == score


def test_update_score():
    db.initialize()
    players = {'test_1': 100, 'test_2': 200, 'test_3': 300}
    for player, score in players.items():
        player_id = db.login(player)
        db.insert_score(player_id, score)

    db.update_top_score()

    for user, score in players.items():
        top_score_query = '''SELECT top_score FROM player WHERE ID = %s ''' % db.get_player_id(user)
        top_score = db.__run_query(top_score_query)[0][0]
        assert top_score == score


