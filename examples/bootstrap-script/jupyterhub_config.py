
# Script that should be executed once before the Spawner spawns the jupyter-notebook
# for one user for the first time.

c.JupyterHub.bootstrap_class = "jupyterhub.bootstrap.BootstrapScriptRunner"

# If there's something weird, in your neighborhood...
c.Bootstrap.ignore_errors=False

# Make sure your Bootstrap-Script can be executed again and again.
c.BootstrapScriptRunner.script = "./examples/bootstrap-script/bootstrap.sh"
