# Goodshare initialization stuff
# Get debug mode option, sure there's a better way of doing this but since i'm running this from import...
import utils
debugging = raw_input("Run Goodshare in debug mode? (y / n)")
if debugging == 'y' or debugging == 'yes':
  utils.debugging = True
elif debugging == 'n' or debugging == 'no':
  utils.debugging = False
else:
  print "Not a valid response, assuming no."
  utils.debugging = False

utils.debug("Goodshare starting...")
from goodreads import client
import os
import sys


#Set up configuration stuff.
from secureconfig import SecureConfigParser
confkey = 'goodshare.key'
conffile = 'goodshare.conf'
#Checking if we have the key to open up our configuration file and extract sensitive values
utils.debug("Checking if key file exists")
if os.path.isfile(confkey)==False:
  #A key file isn't in current directory
  print "Error! No keyfile found in current directory! This means you won't be able to decrypt needed authorization information to access web services."
  sys.exit()
utils.debug("Keyfile exists.")
#Enstantiate a config parser object with our key
config = SecureConfigParser.from_file(confkey)
utils.debug("loaded secure config parsing object with keyfile %s" % (confkey))

# Check if we've got a config file
if os.path.isfile(conffile)==False:
  # No configuration files in current directory.
  print "Error! No configuration file found in current directory. Necessary API and access keys are not available. Exeting."
  sys.exit()
else: # Since it exists, load it
  config.read(conffile)
  utils.debug("Loaded configuration file, %s." % (conffile))
# Check if we've got app API keys for Goodshare and Goodreads:
if config.get('APIKeys', 'gkey') and config.get('APIKeys', 'gsecret'):
  utils.debug("Goodshare's API keys for bookshare are present in configuration.")
  #proceed
  utils.debug("Initializing goodreads class with provided API keys...")
  gc = client.GoodreadsClient(config.get('APIKeys', 'gkey'), config.get('APIKeys', 'gsecret')) # initialize our goodreads class with app tokens
else:
  print "Error! Necessary API keys are not present in configuration file. Goodshare can't authenticate to Goodreads."
  sys.exit()

if gc:
  utils.debug("Goodreads class enstantiation completed.")
else:
  utils.debug("Goodreads class failed to be created.")

# Check if we've got user spesific access tokens for Goodshare and Goodreads:
if config.get('APIKeys', 'g_token') and config.get('APIKeys', 'g_token_secret'):
  utils.debug("Goodshare's user spesific app tokens exist.")
  print "Authenticating to Goodreads."
  gc.authenticate(config.get('APIKeys', 'g_token'), config.get('APIKeys', 'g_token_secret'))
else: # we don't have app spesific tokens, we need to authorize with Goodreads to get them
  print "No user spesific goodreads access tokens available."
  result = raw_input("Do you want to obtain them? This should only have to be done once, and is required to use goodreads with Goodshare. (y/n)")
  if result == 'y' or result == 'yes':
    authorize()
print "Logged into Goodreads as: %s!" %(gc.auth_user())

#Functions

def authorize():
  utils.debug("Passing auth request to goodreads wrapper")
  gc.authenticate() #Pass the request to authorize off to the goodreads wrapper
  #Convert the returned token strings from unicode to ascii
  if gc.session.access_token and gc.session.access_token_secret:
    utils.debug("Token values were returned.")
  gc.session.access_token = gc.session.access_token.encode('ascii','ignore')
  gc.session.access_token_secret = gc.session.access_token_secret.encode('ascii','ignore')
  # Encrypt and save the resulting tokens in our config file:
  config.set('APIKeys', 'g_token', gc.session.access_token, encrypt=True)
  config.set('APIKeys', 'g_token_secret', gc.session.access_token_secret, encrypt=True)
  if config.get('APIKeys', 'g_token') and config.get('APIKeys', 'g_token_secret'): # If values exist in our keyfile
    if config.get('APIKeys', 'g_token') == gc.session.access_token and config.get('APIKeys', 'g_token_secret') == gc.session.access_token_secret: # if those values match our tokens
      print "Retrieved and saved you're Goodreads access tokens!"
    else:
      print "Error, tokens saved in config do not match those that were just saved!"
  else:
    print "Error in retrieving Goodreads access tokens, please try again."
