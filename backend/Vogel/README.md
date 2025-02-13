# SHELL

```
createuser --superuser vogel
createdb vogel -O vogel
```

# SQL

```
CREATE EXTENSION postgis;

ALTER USER vogel PASSWORD 'changeme';
ALTER USER vogel CREATEDB;
ALTER ROLE vogel SET client_encoding TO 'utf8';
ALTER ROLE vogel SET default_transaction_isolation TO 'read committed';
ALTER ROLE vogel SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vogel TO vogel;
```
