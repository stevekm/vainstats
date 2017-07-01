'''
General utility functions to use in the app
'''

def load_json(input_file):
    '''
    Load JSON from a file
    '''
    import json
    with open(input_file,"r") as f:
        my_item = json.load(f)
    return(my_item)
