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
