# FastAPI Starter

## Run

1. `poetry install`
2. `make upgrade_db env=local.env`
3. `make run env=local.env`
4. open http://localhost:8000/docs

## Model Changes (Migrations)

1. Change database models
2. `make make_db_migration env=local.env name=${NAME OF MIGRATION}`
3. Revise migration file
4. `make upgrade_db env=local.env`

Note: [You will need to fix non-null changed attributes manually](https://medium.com/the-andela-way/alembic-how-to-add-a-non-nullable-field-to-a-populated-table-998554003134)

## Features

- [x] Config
- [x] Logging
- [x] vscode debugger
- [x] linting
- [x] formatting
- [x] auto api docs
- [x] sql database
- [x] migrations
- [x] prefix ids
- [x] pagination
- [x] filtering pattern
- [ ] async/background tasks
- [ ] cron jobs
- [ ] authentication
- [ ] authorization
- [ ] relations
- [x] object versioning/audit
- [ ] api versioning
- [ ] Unit testing
- [ ] Hypothesis testing
- [ ] Codecov
- [ ] Tour

## Recommended VSCode Extensions

- [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)
