from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from core.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
MYSQL = {
    "PORT": settings.MYSQL_PORT,
    "HOST": settings.MYSQL_HOST,
    "USER": settings.MYSQL_USER,
    "PASSWORD": settings.MYSQL_PASSWORD,
    "DB_NAME": settings.MYSQL_DB,
    "DB_URI": settings.DB_URI,
}
config = context.config

config_section = config.config_ini_section
config.set_section_option(config_section, "MYSQL_HOST", MYSQL["HOST"])
config.set_section_option(config_section, "MYSQL_PORT", MYSQL["PORT"])
config.set_section_option(config_section, "MYSQL_USER", MYSQL["USER"])
config.set_section_option(config_section, "MYSQL_PASSWORD", MYSQL["PASSWORD"])
config.set_section_option(config_section, "MYSQL_DB", MYSQL["DB_NAME"])
config.set_section_option(config_section, "DB_URI", MYSQL["DB_URI"])

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
from db.base import Base  # noqa

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url", settings.DB_URI)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
