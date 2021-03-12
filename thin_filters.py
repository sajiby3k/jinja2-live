# --------------------------------------------------------------------------------------------------
# jinja2-live: thin custom filters
#
# To create new custom filters: 
#  just add the function code and docstring in this file
#  parser.py will import this file and add the function names and explanation into the HTML output
# --------------------------------------------------------------------------------------------------


# functions provided :
#   - combine:     a poor man ansible combine filter replacement
#   - flatten:     a poor man ansible faltten filter replacement
#   - get_keys:    filter to get the keys from a dictionary 
#   - get_values:  filter to get the values from a dictionary 
#   - get_items:   filter to get the key/value pairs from a dictionary 

def flatten(value):
   """ flatten a list """
   return [item for sublist in value for item in sublist]

def combine(value, dict):
   """  merge two dictionaries """
   result = {}
   result.update (value)
   result.update (dict)
   return result
   
def get_keys(dict):
   """ extract the keys from a dictionary """
   return dict.keys()

def get_values(dict):
   """ extract the values from a dictionary """
   return dict.values()

def get_items(dict):
   """ extract the key/value pairs from a dictionary """
   return zip (dict.keys(), dict.values())


