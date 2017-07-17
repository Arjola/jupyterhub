# Bootstrap Process

Before spawning a notebook to the user, it could be useful to 
do some preparation work in a bootstrapping process.

One common use case is at follows:

* You are using an LDAPAuthenticator and have no "home"-Directory for your user on the host
* You are using a DockerSpawner and would like to mount a volume, but as no directory exists, docker will create one.
However, as the docker daemon is running as root, the on-the-fly generated directory for the volume mount will not be
writeable by user jovyan inside of the container

Another use case could be that every newly spawned notebook should come with initial content that you'd like to 
copy into the user's space.

**Here's the bootstrap process to the rescue!**

## BootstrapNone

This is the default bootstrap implementation which does nothing at all. 

    # This is the default value
    c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapNone"

## BootstrapScriptRunner

You can specify a plain ole' shell script (or any other executable) to be run 
by the bootstrap process.

The first and only parameter passed to your executable script is the name of the user.

    # Select BootstrapScriptRunner and specify which script to run as bootstrap process
    c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapScriptRunner"
    c.BootstrapScriptRunner.script = "./myscripts/bootstrap-jupyter.sh"

Make sure that the script is *idempotent*. It will be executed every time 
a notebook server is spawned to the user. That means you should somehow 
make sure that things that should run only once are not run again and again.

For example, before you create a directory, check if it exists.
 
The Bootstrap process will not wait forever. Specify a timeout or live with the default
value of 120 seconds:

    # Timeout in seconds for script. Defaults to 120 seconds
    c.BootstrapScriptRunner.execution_timeout = 60

Here's an example on what you could do in your shell script. See also 
/examples/bootstrap-script/

    #!/bin/bash
    
    # Bootstrap example script
    # Copyright (c) Jupyter Development Team.
    # Distributed under the terms of the Modified BSD License.
    
    # Do not change the following:
    # - The first parameter for the Bootstrap Script is the USER.
    USER=$1
    if [$USER == ""]; then
        exit 1
    fi
    # ----------------------------------------------------------------------------
    
    
    # This example script will do the following:
    # - create one directory for the user $USER in a BASE_DIRECTORY (see below)
    # - create a "tutorials" directory within and download and unzip the PythonDataScienceHandbook from GitHub
    
    # Start the Bootstrap Process
    echo "bootstrap process running for user $USER ..."
    
    # Base Directory: All Directories for the user will be below this point
    BASE_DIRECTORY=/volumes/jupyterhub/
    
    # User Directory: That's the private directory for the user to be created, if none exists
    USER_DIRECTORY=$BASE_DIRECTORY/$USER
    
    if [ -d "$USER_DIRECTORY" ]; then
        echo "...directory for user already exists. skipped"
        exit 0 # all good. nothing to do.
    else
        echo "...creating a directory for the user: $USER_DIRECTORY"
        mkdir $USER_DIRECTORY
    
        echo "...initial content loading for user ..."
        mkdir $USER_DIRECTORY/tutorials
        cd $USER_DIRECTORY/tutorials
        wget https://github.com/jakevdp/PythonDataScienceHandbook/archive/master.zip
        unzip master.zip
        rm master.zip
    fi
    
    exit 0
