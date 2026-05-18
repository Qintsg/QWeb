-- QWeb PostgreSQL 本地初始化脚本。
--
-- :project: QWeb
-- :file: postgresql-init.sql
-- :author: Qintsg
-- :date: 2026-05-12 00:00

\set ON_ERROR_STOP on

-- 执行前可通过 psql 变量覆盖：
-- psql -U postgres -v qweb_db=qweb -v qweb_user=qweb_app -v qweb_password='replace-with-local-password' -f docs/postgresql-init.sql
\set qweb_db :qweb_db
\set qweb_user :qweb_user
\set qweb_password :qweb_password

DO
$$
DECLARE
    target_user text := :'qweb_user';
    target_password text := :'qweb_password';
BEGIN
    IF target_user IS NULL OR target_user = '' THEN
        RAISE EXCEPTION 'qweb_user 不能为空，请通过 -v qweb_user=... 传入数据库用户';
    END IF;
    IF target_password IS NULL OR target_password = '' THEN
        RAISE EXCEPTION 'qweb_password 不能为空，请通过 -v qweb_password=... 传入数据库密码';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_catalog.pg_roles
        WHERE rolname = target_user
    ) THEN
        EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L', target_user, target_password);
    ELSE
        EXECUTE format('ALTER ROLE %I WITH LOGIN PASSWORD %L', target_user, target_password);
    END IF;
END
$$;

SELECT format('CREATE DATABASE %I OWNER %I ENCODING ''UTF8'' TEMPLATE template0', :'qweb_db', :'qweb_user')
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = :'qweb_db'
)\gexec

SELECT format('ALTER DATABASE %I OWNER TO %I', :'qweb_db', :'qweb_user')\gexec
SELECT format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', :'qweb_db', :'qweb_user')\gexec

\connect :qweb_db

SELECT format('ALTER SCHEMA public OWNER TO %I', :'qweb_user')\gexec
SELECT format('GRANT ALL ON SCHEMA public TO %I', :'qweb_user')\gexec
