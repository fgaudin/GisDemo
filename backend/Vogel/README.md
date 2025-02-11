SQL

ALTER ROLE vogel SET client_encoding TO 'utf8';
ALTER ROLE vogel SET default_transaction_isolation TO 'read committed';
ALTER ROLE vogel SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vogel TO vogel;
