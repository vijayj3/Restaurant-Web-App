-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE restaurant(id SERIAL primary key,
			name text);

CREATE TABLE menu_item(id INTEGER references restaurant(id),
		       name text,
		       description text,
                       price integer,
		       course text);