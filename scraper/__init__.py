import click
import logging
from instapy import InstaPy
from pprint import pformat

from scraper import config, crud, session

logging.basicConfig(filename="logs.txt", level=logging.INFO)

def get_instapy_session():
	ig_session = InstaPy(**config.INSTAPY_SESSION)
	ig_session.login()
	ig_session.set_quota_supervisor(**config.QUOTA_SUPERVISOR)
	yield ig_session

	ig_session.end()

@click.command
@click.argument('username')
def store_following(username):
	"""Get following of a given user"""

	for db in session.get_session():
		for ig_session in get_instapy_session():
			following_list = ig_session.grab_following(
				username=username,
				amount="full",
				live_match=True,
				store_locally=False #originally True
			)

			creator = crud.creator.get_by_username(db, username=username)
			if not creator:
				creator_in = models.CreatorCreate(username=username, is_manually_added=True)
				creator = crud.creator.create(db, obj_in=creator_in)

			for username in following_list:
				following = crud.creator.get_by_username(db, username=username)
				if not following:
					following_in = models.CreatorCreate(username=username)
					following = crud.creator.create(db, obj_in=following_in)
				link = crud.creator_link.get(
					db, follower_id=creator.id, followed_id=following.id
				)
				if not link:
					link_in = models.CreatorLinkCreate(
						follower_id=creator.id, followed_id=following.id
					)
					link = crud.creator_link.create(db, obj_in=link_in)

@click.command
def test(username):
	"""Testing"""
	for db in session.get_session():
		creator = crud.creator.get_by_username(db, username=username)
		logging.info(f"{pformat(creator.following_list)}")

@click.group
def cli():
	pass

cli.add_command(session.init_db)
cli.add_command(store_following)
cli.add_command(test)