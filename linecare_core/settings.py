from os import path
from split_settings.tools import optional, include

if path.isfile("/home/ubuntu/linecare/envars/local"):
    include("settings_collection/local.py")
elif path.isfile("/home/ubuntu/linecare/envars/testing"):
    include("settings_collection/testing.py")
elif path.isfile("/home/ubuntu/linecare/envars/beta"):
    include("settings_collection/beta.py")
else:
    include("settings_collection/production.py")
