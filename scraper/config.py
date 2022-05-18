from dotenv import load_dotenv
from os import environ

load_dotenv()

# added want_check_browser parameter, see https://github.com/InstaPy/instapy-quickstart/issues/118
INSTAPY_SESSION = {
	"username": environ['USER'], 
	"password": environ['PASS'], 
	"headless_browser": True, 
	"want_check_browser": False
}
QUOTA_SUPERVISOR = {
	"enabled": True,
	"sleep_after": ["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
	"sleepyhead": True,
	"stochastic_flow": True,
	"notify_me": True,
	"peak_server_calls_hourly": None,
	"peak_server_calls_daily": 4700
}