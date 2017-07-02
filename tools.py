'''
General utility functions to use in the app
'''
import dash_html_components as html

import logging
logger = logging.getLogger(__name__)

def my_debugger(vars):
    '''
    Starts interactive Python terminal at location in script
    call with
    my_debugger(globals().copy())
    anywhere in your script
    or call
    my_debugger(locals().copy())
    from anywhere within this package
    '''
    import readline # optional, will allow Up/Down/History in the console
    import code
    # vars = globals().copy() # in python "global" variables are actually module-level
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

def log_setup(config_yaml, logger_name):
    '''
    Set up the logger for the script
    config = path to YAML config file
    '''
    import yaml
    import logging
    import logging.config
    # Config file relative to this file
    loggingConf = open(config_yaml, 'r')
    logging.config.dictConfig(yaml.load(loggingConf))
    loggingConf.close()
    return(logging.getLogger(logger_name))

def load_json(input_file):
    '''
    Load JSON from a file
    '''
    import json
    logger.debug("Loading data from JSON")
    with open(input_file,"r") as f:
        my_item = json.load(f)
    return(my_item)
