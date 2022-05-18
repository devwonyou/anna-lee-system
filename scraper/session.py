import click
import logging
from sqlmodel import Session, SQLModel, create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(
	'sqlite:///data.db',
	connect_args={'check_same_thread': False}
)

def create_db_and_tables():
	SQLModel.metadata.create_all(engine)

def drop_db():
	SQLModel.metadata.drop_all(engine)
	
def get_session():
	with Session(engine) as session:
		yield session

@click.command()
def init_db():
	"""Drops existing database (data.db) and initializes a new one"""

	res = input("This will delete existing data (data.db), continue? (y/n)")
	if res != 'y':
		return

	logger.info("Dropping tables")
	drop_db()

	logger.info("Creating initial data")
	create_db_and_tables()

	logger.info("Initial data created")

create_db_and_tables()