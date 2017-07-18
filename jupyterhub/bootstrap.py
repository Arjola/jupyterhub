
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import Unicode, Bool, Integer
from traitlets.config import LoggingConfigurable


class BootstrapException(Exception):
    pass

class Bootstrap(LoggingConfigurable):
    """
    Base class for implementing a bootstrapping strategy
    before JupyterHub spawns (the first) notebook to the user.

    For example: create a directory for the user, before docker daemon
    creates a directory as root during volume mounting, or get the
    great The Datascience Handbook from github and put it into the Notebook
    Environment for the user etc.
    """

    ignore_errors = Bool(
        True,
        help="""
        If True, ignores errors and just prints a warning.
        If False, errors will disable the spawning process. No notebook will be started for the user.
        """
    ).tag(config=True)

    # Just an idea. run_once flag is not needed if the script that runs itself is idempotent.
    # todo not implemented feature: run_once TRUE/FALSE
    #run_once = Bool(
    #    True,
    #    help="""
    #    If True, will run only for the first time a notebook is spawned for the user.
    #    If False, will run always before a notebook is spawned for the user.
    #    """
    #).tag(config=True)'''

    # Another idea: When you add a bootstrapper for the first time to your config,
    # should all "old" users also run into the bootstrap process?
    # todo not implemented feature: bootstrap_old_users TRUE/FALSE
    #bootstrap_old_users = Bool(
    #    False,
    #    help="""
    #    If False, existing users will not be bootstrapped as soon as you first make use of a Bootstrapper (i. e.
    #    you have an existing user-base which should not be bootstrapped afterwards).
    #    If True, old users will also run through the bootstrap process
    #    """
    #)

    def __init__(self, user, spawner, **kwargs):
        self.user = user
        self.spawner = spawner
        super().__init__(**kwargs)

    def _bootstrap_can_run(self):
        return True

    def run(self):
        if (self._bootstrap_can_run()):
            try:
                self.log.info("bootstrap for user {username}".format(username=self.user.name))
                strapped = self.bootstrap()
                if (not strapped and not self.ignore_errors):
                    raise BootstrapException("bootstrap failed, error cannot be ignored.")

            except Exception as e:
                self.log.error("bootstrap process failed for user {username}".format(username=self.user.name))
                if (not self.ignore_errors):
                    raise BootstrapException("bootstrap failed with exception, cannot be ignored.") from e
                return False
        else:
            return True

    def bootstrap(self):
        raise NotImplementedError()


class BootstrapNone(Bootstrap):
    """
    Default Bootstrapper that actually does nothing special.
    """
    def bootstrap(self):
        return True


from subprocess import Popen

class BootstrapScriptRunner(Bootstrap):
    """
    Run a shell script to bootstrap your users
    """
    script = Unicode(
        'bootstrap.sh',
        help="""
        Path to Script-File to be run as bootstrapper. 
        First argument to script ($1) is the user name
        """
    ).tag(config=True)

    execution_timeout = Integer(
        120,
        help="""
        Timeout in seconds to wait for the script to terminate
        """
    ).tag(config=True)

    def bootstrap(self):
        self.log.debug("starting configured script {scriptname}".format(scriptname=self.script))
        try:
            handle = Popen([self.script, self.user.name])
            handle.wait(timeout=self.execution_timeout)
            return handle.returncode == 0
        except FileNotFoundError as f:
            self.log.error("Configured script file not found for BootstrapScriptRunner.")
            return False
        except Exception as e:
            raise e

        return False