import schema

from . import scala


"""
    Simple Console Application with Logging, Yaml Configuration and Argparse
"""
class Scalyca(scala.Scala):
    app_name = 'Scalyca'
    description = "Simple Configurable Application with Logging, Yaml file Configuration and Argparse"
    # Config validation schema, or None to skip validation
    schema = None

    def add_default_arguments(self):
        super().add_default_arguments()
        self.argparser.add_argument('config', type=argparse.FileType('r'), help="main configuration file")

    def initialize(self):
        super().initialize()
        try:
            self.load_config()
            self.override_config()
            self.lock_config()
            self.debug_config()
            self.validate_config()

        except exceptions.FatalError:
            log.critical(f"{c.script(self.app_name)} aborting during configuration")
            sys.exit(-1)

    def load_config(self):
        raw = configuration.load_YAML(self.args.config)
        self.config = dotmap.DotMap(raw, _dynamic=True)
        log.info(f"Configuration read from {c.filename(self.args.config)}")

    def lock_config(self):
        configuration.make_static(self.config)

    def override_with_warning(self, parameter, new_value):
        log.warning(f"Overriding {c.param(parameter)} ({c.over(self.config[parameter])} -> {c.over(new_value)})")
        self.config['parameter'] = new_value

    def debug_config(self):
        if self.args.debug:
            log.debug("Full config is")
            self.config.pprint()

    def validate_config(self):
        if self.schema is None:
            log.debug("No config validation schema provided, skipping validation")
        else:
            schema.validate(self.config, self.schema)
