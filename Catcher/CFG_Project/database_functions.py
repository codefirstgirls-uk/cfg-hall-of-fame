from mysql.connector import connect, Error
from config import db_HOST, db_USERNAME, db_PASSWORD, db_NAME


def convert_time(score_list):
    return [(score[0], score[1], str(score[2])) for score in score_list]


def connect_to_database():
    """
    Function to connect to a specified database

    :param db_name: str
    :return cnx: database object

    """

    cnx = connect(
        host=db_HOST,
        user=db_USERNAME,
        password=db_PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_NAME
    )
    return cnx


def __run_query(query):
    """
    A private method for connecting to the database and then running the query provided

    Parameters
    ---------
    query : str
        The query to be run

    Returns
    ---------
    list
        A list of tuples being the rows returned from the statement
    """

    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return result
    except Error as e:
        print(e)
        return


def initialize():
    queries = [
        'DROP TABLE IF EXISTS Score;',

        '''DROP TABLE IF EXISTS Player;''',

        '''CREATE TABLE PLAYER (ID INT PRIMARY KEY AUTO_INCREMENT, 
            USERNAME VARCHAR(255), 
            TOP_SCORE INT);''',

        '''CREATE TABLE Score (Score_ID INT PRIMARY KEY AUTO_INCREMENT, 
            Player_ID INT, FOREIGN KEY (Player_ID) REFERENCES Player(ID), 
            SCORE INT, 
            TIME_RECORDED TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'''
    ]
    for query in queries:
        __run_query(query)


# this can be easily changed to a be a login method, whereby if the name entered is already in the dictionary
# then the player id is returned, if not, a new player is created


def login(given_name):
    """
    login returns the player ID of the given name, or inserts the provided name if it is not currently in the database

    Parameters
    ----------
    given_name : str
        The name of the user wished to be inserted

    Returns
    ----------
    int
        The ID of player with the given username
    """

    check_name_query = '''SELECT ID FROM Player WHERE USERNAME = '%s' ''' % given_name
    player_id = __run_query(check_name_query)
    if player_id:
        return player_id[0][0]
    insert_query = """INSERT INTO Player(USERNAME, TOP_SCORE) VALUES("%s", %s);""" % (given_name, 0)
    id_query = '''SELECT max(ID) FROM Player;'''
    __run_query(insert_query)
    result = __run_query(id_query)
    result = result[0][0]
    return result


def get_player_id(username):
    query = '''SELECT id FROM player WHERE USERNAME = '%s' ''' % username
    return __run_query(query)[0][0]


def update_top_score(player_id=0):
    """
    Updates the player table to reflect the top score by comparing with the score table

    Parameters
    ----------

    Returns
    ----------
    None

    """
    if player_id:
        query = '''
                UPDATE Player
                INNER JOIN (SELECT Player_ID as score_player_id, max(SCORE) as max_score FROM Score GROUP BY Player_ID) max_grouped_scores
                ON Player.ID = max_grouped_scores.score_player_id
                SET TOP_SCORE = max_grouped_scores.max_score
                WHERE Player.ID = %s
                AND Player.ID <> -1;
                ''' % player_id
    else:
        query = '''
                        UPDATE Player
                        INNER JOIN (SELECT Player_ID as score_player_id, max(SCORE) as max_score FROM Score GROUP BY Player_ID) max_grouped_scores
                        ON Player.ID = max_grouped_scores.score_player_id
                        SET TOP_SCORE = max_grouped_scores.max_score
                        WHERE Player.ID = max_grouped_scores.score_player_id
                        AND Player.ID <> -1;
                        '''
    scores = __run_query(query)


def insert_score(player_id, score):

    """
    Inserts a given score into the database, corresponding to the player whose ID is provided.
    :param player_id: int
    :param score: int
    :return: None
    """
    query = '''INSERT INTO Score(Player_ID, Score, Time_Recorded) VALUES(%s, %s, NOW());''' % (player_id, score)
    __run_query(query)
    update_top_score(player_id)


def get_user_scores(player_id):
    """
    Returns a tuple containing all the scores for a given player

    :param player_id: int
    :return: list of tuples containing username, score, and time achieved
    """

    query = '''
            SELECT USERNAME, SCORE, TIME_RECORDED
            FROM Score
            INNER JOIN Player
            ON Score.Player_ID = Player.ID
            WHERE Player.ID = %s
            ORDER BY TIME_RECORDED desc
            ''' % player_id
    scores = __run_query(query)
    # scores is a list of tuples formatted as (USERNAME, SCORE, TIME)
    return convert_time(scores)


def get_recent_scores(number_of_scores=3):
    """
    Returns a tuple containing the most recent scores, 3 by default

    :param number_of_scores: int

    :return list of tuples containing USERNAME, SCORE, TIME ACHIEVED
    """
    query = '''
            SELECT USERNAME, SCORE, TIME_RECORDED
            FROM Score
            INNER JOIN Player
            ON Score.player_id = Player.ID
            ORDER BY TIME_RECORDED desc
            LIMIT %s
            ''' % number_of_scores
    scores = __run_query(query)
    return convert_time(scores)


def get_top_scores(number_of_scores=3):
    """
    Returns a list of tuples containing the highest scores, 3 by default

    """
    update_top_score()
    query = '''
            SELECT USERNAME, TOP_SCORE
            FROM Player
            ORDER BY TOP_SCORE desc
            LIMIT %s
            ''' % number_of_scores
    scores = __run_query(query)
    return scores


def get_user_top_score(player_id):
    query = '''SELECT top_score FROM player WHERE id = '%s' ''' % player_id
    return __run_query(query)[0][0]


if __name__ == '__main__':
    get_player_id(username="san")
