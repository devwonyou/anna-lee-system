from instapy import InstaPy
from dotenv import load_dotenv
from os import environ
from pprint import pprint

load_dotenv()

# added want_check_browser parameter, see https://github.com/InstaPy/instapy-quickstart/issues/118
session = InstaPy(
	username=environ['USER'], 
	password=environ['PASS'], 
	headless_browser=True, 
	want_check_browser=False
)
session.login()

target_following = session.grab_following(
	username=environ['TARGET']
)

