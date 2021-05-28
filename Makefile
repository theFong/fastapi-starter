define setup_env_from_file
	$(eval ENV_FILE := $(1))
	$(eval include $(1))
	$(eval export)
	$(eval export sed 's/=.*//' $(1))
endef

define setup_env
	[ "${env}" ] || ( echo "'env' not provided"; exit 1 )
	$(call setup_env_from_file, ${env})
endef

run:
	$(call setup_env)
	poetry run python fastapi_starter

make_db_migration:
	[ "${name}" ] || ( echo "'name' not provided"; exit 1 )
	$(call setup_env)
	poetry run alembic revision --autogenerate -m "${name}"

REVISION := $(or ${REVISION},${REVISION},head)
upgrade_db:
	$(call setup_env)
	poetry run alembic upgrade ${REVISION}