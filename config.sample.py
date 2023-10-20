# SIS Settings
# See https://anss-sis.scsn.org/sis/api/v1/docs/#about-token-auth for instructions on generating your API key
api_key = ""
# env should either be sis (production) or sistest (testing)
env = "sis"
# page_size must be 500 or less; this is a tradeoff between the number of API calls and memory usage
page_size = 500;

# API Filters
# ownercode is used as the ownercode for equipment calls and netcode for site-epochs
ownercode = ""
# modelname should be a python list of which models you wish to check for
# Example modelname = [ "CENTAUR", "AIRLINK RV55", "TITAN SMA"]
modelname = []

# Nagios Settings
# Path to store Nagios config files on disk
# Config files are named as LOOKUPCODE_MODEL.cfg
nagios_path = "/tmp/"
