CREATE DATABASE cfg_game;

USE cfg_game;

CREATE TABLE Player (
ID INT PRIMARY KEY AUTO_INCREMENT,
USERNAME VARCHAR(255),
TOP_SCORE INT);

DROP TABLE IF EXISTS Score;

CREATE TABLE Score (
Score_ID INT PRIMARY KEY AUTO_INCREMENT,
Player_ID INT,
FOREIGN KEY (Player_ID) REFERENCES Player(ID),
SCORE INT,
TIME_RECORDED TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- Add new player
INSERT INTO Player (
    USERNAME, TOP_SCORE
)
VALUES(given_name, 0);

INSERT INTO Score (
    Player_ID, Score
)


-- top 3 scores of all time
SELECT USERNAME, TOP_SCORE
FROM Player
ORDER BY TOP_SCORE desc
LIMIT 3;

-- top 3 most recent scores
SELECT USERNAME, SCORE, TIME_RECORDED
FROM Score
INNER JOIN Player
ON Score.Player_ID = Player.ID
ORDER BY TIME_RECORDED desc
LIMIT 3;

-- select an individual users score
SELECT USERNAME, SCORE, TIME_RECORDED
FROM Score
INNER JOIN Player
ON Score.Player_ID = Player.ID
WHERE Player.ID = ID_provided
ORDER BY TIME_RECORDED desc;

-- test if a USERNAME is already in use
SELECT *
FROM Player
WHERE USERNAME = given_name;

UPDATE Player
INNER JOIN (SELECT Player_ID as score_player_id, max(SCORE) as max_score FROM Score GROUP BY Player_ID) max_grouped_scores
ON Player.ID = max_grouped_scores.score_player_id
SET TOP_SCORE = max_grouped_scores.max_score
WHERE Player.ID = max_grouped_scores.score_player_id
AND Player.ID <> -1