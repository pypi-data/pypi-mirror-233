import argparse
import dotmap
import logging
import yaml
import sys

from abc import abstractmethod

from . import colour as c
from . import exceptions
from . import logger
from . import configuration

log = logger.setupLog('root')


"""
    Scala: Simple Console Application with Logging and Argparse
"""
class Scala():
    app_name = "Default Scala"
    description = "Simple Configurable Application with Logging and Argparse"

    def __init__(self, **kwargs):
        """ Optionally override the application name and description """
        self.ok = True
        self.description = kwargs.get('description', self.description)
        self.app_name = kwargs.get('app_name', self.app_name)

    def initialize(self):
        self.create_argparser()
        self.add_default_arguments()
        self.add_arguments()

        self.args = self.argparser.parse_args()
        self.override_configuration()
        self.ok = False

    def create_argparser(self):
        self.argparser = argparse.ArgumentParser(self.description)

    def add_default_arguments(self):
        self.argparser.add_argument('-l', '--logfile', type=argparse.FileType('w'), help="Write log to file", default=sys.stdout)
        self.argparser.add_argument('-d', '--debug', action='store_true', help="Turn on verbose logging")

    @abstractmethod
    def add_arguments(self):
        pass

    def main(self):
        pass

    def run(self):
        try:
            self.initialize()
            self.main()
            self.finalize()
        except exceptions.PrerequisiteError as e:
            log.error(f"Terminating due to missing prerequisites: {e}")
        except exceptions.ConfigurationError as e:
            log.error(f"Terminating due to a configuration error: {e}")
        finally:
            if not self.ok:
                log.critical(f"{c.script(self.app_name)} aborted during runtime")

    def finalize(self):
        self.ok = True

    def override_configuration(self):
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)

        if self.args.debug:
            log.warning(f"Debug output is {c.over('active')}")

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.debug(f"Added log output {c.path(self.args.logfile.name)}")

    def override_warning(self, parameter, old, new):
        log.warning(f"Overriding {c.param(parameter)} ({c.over(old)} -> {c.over(new)})")

