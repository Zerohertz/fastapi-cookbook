## Init

```shell
$ source .venv/bin/activate
$ alembic init alembic
  Creating directory '/home/zerohertz/workspace/alembic' ...  done
  Creating directory '/home/zerohertz/workspace/alembic/versions' ...  done
  Generating /home/zerohertz/workspace/alembic/env.py ...  done
  Generating /home/zerohertz/workspace/alembic.ini ...  done
  Generating /home/zerohertz/workspace/alembic/script.py.mako ...  done
  Generating /home/zerohertz/workspace/alembic/README ...  done
  Please edit configuration/connection/logging settings in
  '/home/zerohertz/workspace/alembic.ini' before proceeding.
```

## Setup

<!-- markdownlint-disable -->

```shell
$ sed -i '1i\from app.core.configs import configs\nfrom app.models.base import BaseModel\n' alembic/env.py
$ sed -i 's|target_metadata = None|target_metadata = BaseModel.metadata|g' alembic/env.py
$ sed -i '19i\config.set_main_option("sqlalchemy.url", configs.DATABASE_URI)' alembic/env.py
$ isort alembic && black alembic
```

<!-- markdownlint-enable -->

## Migration

### Revision

```shell
$ make alembic revision="init: alembic"
Resolved 75 packages in 0.69ms
Audited 41 packages in 0.01ms
INFO  [sqlalchemy.engine.Engine] select pg_catalog.version()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] select current_schema()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] show standard_conforming_strings
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relname = $1::VARCHAR AND pg_catalog.pg_class.relkind = ANY (ARRAY[$2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR, $6::VARCHAR]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $7::VARCHAR
INFO  [sqlalchemy.engine.Engine] [generated in 0.00010s] ('alembic_version', 'r', 'p', 'f', 'v', 'm', 'pg_catalog')
INFO  [sqlalchemy.engine.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.Engine] [generated in 0.00006s] ()
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relname = $1::VARCHAR AND pg_catalog.pg_class.relkind = ANY (ARRAY[$2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR, $6::VARCHAR]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $7::VARCHAR
INFO  [sqlalchemy.engine.Engine] [cached since 0.002318s ago] ('alembic_version', 'r', 'p', 'f', 'v', 'm', 'pg_catalog')
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relkind = ANY (ARRAY[$1::VARCHAR, $2::VARCHAR]) AND pg_catalog.pg_class.relpersistence != $3::CHAR AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $4::VARCHAR
INFO  [sqlalchemy.engine.Engine] [generated in 0.00007s] ('r', 'p', 't', 'pg_catalog')
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added table 'oauth'
INFO  [sqlalchemy.engine.Engine] COMMIT
  Generating /home/zerohertz/workspace/alembic/versions/0bdf3abd5213_init_alembic.py ...  done
```

### Upgrade

```shell
$ make alembic
Resolved 75 packages in 0.67ms
Audited 41 packages in 0.01ms
INFO  [sqlalchemy.engine.Engine] select pg_catalog.version()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] select current_schema()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] show standard_conforming_strings
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relname = $1::VARCHAR AND pg_catalog.pg_class.relkind = ANY (ARRAY[$2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR, $6::VARCHAR]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $7::VARCHAR
INFO  [sqlalchemy.engine.Engine] [generated in 0.00011s] ('alembic_version', 'r', 'p', 'f', 'v', 'm', 'pg_catalog')
INFO  [sqlalchemy.engine.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.Engine] [generated in 0.00007s] ()
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relname = $1::VARCHAR AND pg_catalog.pg_class.relkind = ANY (ARRAY[$2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR, $6::VARCHAR]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $7::VARCHAR
INFO  [sqlalchemy.engine.Engine] [cached since 0.002368s ago] ('alembic_version', 'r', 'p', 'f', 'v', 'm', 'pg_catalog')
INFO  [alembic.runtime.migration] Running upgrade  -> 0bdf3abd5213, init: alembic
INFO  [sqlalchemy.engine.Engine] CREATE TYPE role AS ENUM ('ADMIN', 'USER')
INFO  [sqlalchemy.engine.Engine] [no key 0.00005s] ()
INFO  [sqlalchemy.engine.Engine]
CREATE TABLE "user" (
 name VARCHAR(255) NOT NULL,
 email VARCHAR(255) NOT NULL,
 role role NOT NULL,
 refresh_token VARCHAR(255),
 id SERIAL NOT NULL,
 created_at TIMESTAMP WITH TIME ZONE NOT NULL,
 updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
 PRIMARY KEY (id),
 UNIQUE (email),
 UNIQUE (name)
)


INFO  [sqlalchemy.engine.Engine] [no key 0.00005s] ()
INFO  [sqlalchemy.engine.Engine] CREATE TYPE oauthprovider AS ENUM ('PASSWORD', 'GITHUB', 'GOOGLE')
INFO  [sqlalchemy.engine.Engine] [no key 0.00006s] ()
INFO  [sqlalchemy.engine.Engine]
CREATE TABLE oauth (
 user_id INTEGER NOT NULL,
 provider oauthprovider NOT NULL,
 password VARCHAR(255),
 oauth_id VARCHAR(255),
 oauth_token VARCHAR(255),
 id SERIAL NOT NULL,
 created_at TIMESTAMP WITH TIME ZONE NOT NULL,
 updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
 PRIMARY KEY (id),
 FOREIGN KEY(user_id) REFERENCES "user" (id),
 CONSTRAINT uq_oauth_user_provider UNIQUE (user_id, provider)
)


INFO  [sqlalchemy.engine.Engine] [no key 0.00005s] ()
INFO  [sqlalchemy.engine.Engine] INSERT INTO alembic_version (version_num) VALUES ('0bdf3abd5213') RETURNING alembic_version.version_num
INFO  [sqlalchemy.engine.Engine] [generated in 0.00007s] ()
INFO  [sqlalchemy.engine.Engine] COMMIT
```

### Downgrade

```shell
$ make alembic revision=downgrade
Resolved 75 packages in 0.68ms
Audited 41 packages in 0.01ms
INFO  [sqlalchemy.engine.Engine] select pg_catalog.version()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] select current_schema()
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [sqlalchemy.engine.Engine] show standard_conforming_strings
INFO  [sqlalchemy.engine.Engine] [raw sql] ()
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.Engine] SELECT pg_catalog.pg_class.relname
FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
WHERE pg_catalog.pg_class.relname = $1::VARCHAR AND pg_catalog.pg_class.relkind = ANY (ARRAY[$2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR, $6::VARCHAR]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != $7::VARCHAR
INFO  [sqlalchemy.engine.Engine] [generated in 0.00011s] ('alembic_version', 'r', 'p', 'f', 'v', 'm', 'pg_catalog')
INFO  [sqlalchemy.engine.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.Engine] [generated in 0.00006s] ()
INFO  [alembic.runtime.migration] Running downgrade 0bdf3abd5213 -> , init: alembic
INFO  [sqlalchemy.engine.Engine]
DROP TABLE oauth
INFO  [sqlalchemy.engine.Engine] [no key 0.00004s] ()
INFO  [sqlalchemy.engine.Engine]
DROP TABLE "user"
INFO  [sqlalchemy.engine.Engine] [no key 0.00004s] ()
INFO  [sqlalchemy.engine.Engine] DELETE FROM alembic_version WHERE alembic_version.version_num = '0bdf3abd5213'
INFO  [sqlalchemy.engine.Engine] [generated in 0.00007s] ()
INFO  [sqlalchemy.engine.Engine] COMMIT
```
