'''
Functions to set up the app logger
'''
import yaml
import logging
import logging.config
import os

def logpath(scriptdir, logfile = 'log.txt'):
    '''
    Return the path to the main log file; needed by the logging.yml
    use this for dynamic output log file paths & names
    '''
    log_file = os.path.join(scriptdir, logfile)
    return(logging.FileHandler(log_file))

def log_setup(config_yaml, logger_name):
    '''
    Set up the logger for the script
    config = path to YAML config file
    '''
    # Config file relative to this file
    loggingConf = open(config_yaml, 'r')
    logging.config.dictConfig(yaml.load(loggingConf))
    loggingConf.close()
    return(logging.getLogger(logger_name))
