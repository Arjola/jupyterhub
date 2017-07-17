# Bootstrap Process

Before starting a notebook for the user, it could be useful to 
start some bootstrap process beforehand.

One common use case is at follows:

* You are using an LDAPAuthenticator and have no "home"-Directory for your user on the host
* You are using a DockerSpawner and would like to mount a volume, but as no directory exists, docker will create one.
However, as the docker daemon is running as root, the on-the-fly generated directory for the volume mount will not be
writeable by user jovyan inside of the container

Another use case could be that every newly spawned notebook should come with initial content that you'd like to 
copy into the user's space.

Here's the bootstrap process to the rescue!

## NoBootstrap

This is the default bootstrap impementation which does nothing at all. 

    # This is the default value
    c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapNone"

## BootstrapScriptRunner

Here you can specify a plain old shell script to be executed by the bootstrap process.
The first parameter passed to your script is the name of the user.

    # Specify which script to run as bootstrap process
    c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapScriptRunnter"
    c.BootstrapScriptRunner.script = "./myscripts/bootstrap-jupyter.sh"

