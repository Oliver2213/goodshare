# Goodshare initialization stuff
from goodreads import client
import sys

def saveconfig(filename, configclass):
  """Function to open, save a config to, and then close a file."""
  fh = open(filename, 'w')
  configclass.write(filename)
  fh.close()

#Set up configuration stuff.
from secureconfig import SecureConfigParser
confkey = 'goodshare.key'
conffile = 'goodshare.conf'
#Checking if we have the key to open up our configuration file and extract sensitive values
if os.path.isfile(confkey)==False:
  #A key file isn't in current directory
  print "Error! No keyfile found in current directory! This means you won't be able to decrypt needed authorization information to access web services."
  sys.exit()

#Enstantiate a config parser object with our key
config = SecureConfigParser.from_file(confkey)

# Check if we've got a config file
if os.path.isfile(conffile)==False:
  # No configuration files in current directory.
  print "Error! No configuration file found in current directory. Necessary API and access keys are not available. Exeting."
  sys.exit()
else # Since it exists, load it
  config.read(conffile)
# Check if we've got app API keys for Goodshare and Goodreads:
if config.get('APIKeys', 'gkey') and config.get('APIKeys', 'gsecret'):
  #proceed
  gc = client.GoodreadsClient(config.get('APIKeys', 'gkey'), config.get('APIKeys', 'gsecret')) # initialize our goodreads class with app tokens

# Check if we've got user spesific access tokens for Goodshare and Goodreads:
if config.get('APIKeys', 'g_token') and config.get('APIKeys', 'g_token_secret'):
  print "Authenticating to Goodreads."
  gc.authenticate(config.get('APIKeys', 'g_token'), config.get('APIKeys', 'g_token_secret'))
else # we don't have app spesific tokens, we need to authorize with Goodreads to get them
  print "No user spesific goodreads access tokens available. Redirecting you so they can be obtained..."
  gc.authenticate()
  # Encrypt and save the resulting tokens in our config file:
  config.set('APIKeys', 'g_token', gc.session.access_token, encrypt=True)
  config.set('APIKeys', 'g_token_secret', gc.session.access_token_secret, encrypt=true)
  if config.get('APIKeys', 'g_token') and config.get('APIKeys', 'g_token_secret'):
    print "Retrieved You're Goodreads access tokens!"
  else
    print "Error in retrieving Goodreads access tokens, please try again."
print Logged into Goodreads as:" gc.auth_user()+"!"