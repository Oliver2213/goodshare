# Goodshare initialization stuff
from goodreads import client
import sys
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
  config.load(conffile)


gc = client.GoodreadsClient(gkey, gsecret)
