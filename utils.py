#Utility functions for goodshare
def debug(debugmessage):
  """Small function to handle debugging.
  The debugging variable gets set to False here, set utils.debugging to true in any modules that use this one, and call utils.debug("message")  in other modules."""
  if debugging == True:
    print "debug: %s" % (debugmessage)
debugging = False #Assume no debugging

def saveconfig(filename, configclass):
  """Function to open, save a config to, and then close a file. (Probably doesn't work)"""
  fh = open(filename, 'w')
  configclass.write(filename)
  fh.close()

def authorize():
  debug("Passing auth request to goodreads wrapper")
  gc.authenticate() #Pass the request to authorize off to the goodreads wrapper
  #Convert the returned token strings from unicode to ascii
  if gc.session.access_token and gc.session.access_token_secret:
    debug("Token values were returned.")
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
