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

def get_api_key(keyfile = "api_keys/key.txt"):
    '''
    Extract the API key string from the first line of the give text file
    '''
    with open(keyfile, "r") as f:
        keys = []
        for line in f:
            keys.append(line.strip())
    return(keys[0])

def html_df_table(df, max_rows = 10):
    '''
    Return HTML
    '''
    return(
    html.Table(
    # Header
    [html.Tr([html.Th(col) for col in df.columns])] +

    # Body
    [html.Tr([
        html.Td(df.iloc[i][col]) for col in df.columns
    ]) for i in range(min(len(df), max_rows))]
    )
    )
