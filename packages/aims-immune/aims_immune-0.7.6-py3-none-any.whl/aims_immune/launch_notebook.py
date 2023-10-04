import jupyterlab
# Kind of a wild thing but this will be a nice way 
# to be able to launch the notebook automatically without
# our users having to search for it... maybe.
from jupyterlab import labapp

def launchit():
    labapp.main()