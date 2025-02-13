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
