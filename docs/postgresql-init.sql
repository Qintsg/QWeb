\set ON_ERROR_STOP on

DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_catalog.pg_roles
        WHERE rolname = 'qintsg'
    ) THEN
        CREATE ROLE qintsg LOGIN PASSWORD 'Ss201803';
    ELSE
        ALTER ROLE qintsg WITH LOGIN PASSWORD 'Ss201803';
    END IF;
END
$$;

SELECT 'CREATE DATABASE qweb OWNER qintsg ENCODING ''UTF8'' TEMPLATE template0'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'qweb'
)\gexec

ALTER DATABASE qweb OWNER TO qintsg;
GRANT ALL PRIVILEGES ON DATABASE qweb TO qintsg;

\connect qweb

ALTER SCHEMA public OWNER TO qintsg;
GRANT ALL ON SCHEMA public TO qintsg;
