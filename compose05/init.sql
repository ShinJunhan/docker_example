-- init.sql

CREATE TABLE member(num SERIAL PRIMARY KEY, name VARCHAR(20), addr TEXT);
INSERT INTO member (name, addr) VALUES ('kim', 'seoul');
INSERT INTO member (name, addr) VALUES ('shin', 'daejeon');
