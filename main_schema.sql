
DROP TABLE IF EXISTS db_user CASCADE ;

SHOW TIMEZONE;
SET TIME ZONE 'Europe/Moscow';

CREATE TABLE db_user (
    pk SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password TEXT
);

SELECT * FROM db_user;

INSERT INTO db_user(username, password) VALUES ('user1', 'pass1');
