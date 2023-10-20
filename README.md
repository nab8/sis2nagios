# Overview
This is a basic proof-of-concept for fetching devices from SIS via the API and creating Nagios configuration files for them.
## Config

### SIS Settings
* api_key - this is your SIS API key, see https://anss-sis.scsn.org/sis/api/v1/docs/#about-token-auth for instructions
* env - should either be sis (production) or sistest (testing)
* page_size - must be 500 or less; this is a tradeoff between the number of API calls and memory usage

### API Filters
* ownercode - used as the ownercode for equipment lookups and netcode for site-epoch lookups
* modelname - should be a python list of which models you wish to check for; example [ "CENTAUR", "AIRLINK RV55", "TITAN SMA"]

### Nagios Settings
* nagios_path - path to store config files on disk

## Running
The script is designed to silently run so you can easily use it within a cron job.  To get started you'll want to copy config.sample.py to config.py and populate the settings.  Once that is done you can simply run the script either via ./sis2nagios.py or python3 sis2nagios.py  Note that it does not manage the Nagios daemon restarts.

## Notes
* Only devices with IP addresses are imported.  If there are multiple addresses it will prefer a routable address over a non-routable (RFC1918) address
* If a config file already exists it will only overwrite settings that this script creates; this allows you to add additional settings or overrides without them being clobbered
* You will want to create MODEL-template templates for each model you wish to import.  This allows you to specify which services apply to which models. 
* Host variables for equipment ID, model, latitude, & longitude are automatically created.  This allows you to use them via the Nagios API if desired