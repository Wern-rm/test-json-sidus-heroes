from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


def configure_postgresql() -> str:
    """
    Configure Postgresql DB
    """
    user = os.environ.get('PSQL_USER', 'gen_user')
    password = os.environ.get('PSQL_PASSWORD', 'Rdfynjdfybt2022')
    ip = os.environ.get('PSQL_HOST', '85.193.81.33')
    port = os.environ.get('PSQL_PORT', '5432')
    db_name = os.environ.get('PSQL_DATABASE', 'default_db')
    return f"postgresql://{user}:{password}@{ip}:{port}/{db_name}"


engine = create_engine(url=configure_postgresql())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


