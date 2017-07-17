
# Script that should be executed once before the Spawner spawns the jupyter-notebook
# for one user for the first time.

c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapScriptRunner"

# If there's something weird, in your neighborhood...
# Either ignore the errors and just spawn the server, or raise an exception
c.Bootstrap.ignore_errors=True

# Make sure your Bootstrap-Script can be executed again and again.
c.BootstrapScriptRunner.script = "./examples/bootstrap-script/bootstrap.sh"

# Timeout in seconds for script. Defaults to 120 seconds
c.BootstrapScriptRunner.execution_timeout = 60
