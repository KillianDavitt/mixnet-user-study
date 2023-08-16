CREATE TABLE response (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    prolific_id STRING,
    delay INTEGER NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER NOT NULL, 
    start_time uint, 
    end_time uint, 
    education VARCHAR(50), 
    automerge_data VARCHAR(100000), 
    speed_rating uint, 
    adapted bool);
CREATE TABLE sqlite_sequence(name,seq);
