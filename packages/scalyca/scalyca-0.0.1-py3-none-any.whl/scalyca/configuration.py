import dotmap
import yaml
import logging

import exceptions
import colour as c

log = logging.getLogger('root')


def load_YAML(file_object):
    try:
        config = yaml.safe_load(file_object)
    except yaml.composer.ComposerError as e:
        log.error(f"YAML composer error {e}")
        raise exceptions.ConfigurationError(e) from e
    except yaml.scanner.ScannerError as e:
        log.error(f"YAML scanner error {e}")
        raise exceptions.ConfigurationError(e) from e

    return dotmap.DotMap(config, _dynamic=True)


def make_static(dm):
    for k in dm._map:
        if isinstance(dm[k], dotmap.DotMap):
            make_static(dm[k])
        if isinstance(dm[k], list):
            for item in dm[k]:
                make_static(item)
        dm._dynamic = False
