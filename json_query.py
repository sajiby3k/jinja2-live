# From lib/ansible/plugins/filter/json_query.py
#
# add json_query filters to jinja2-live parser

from jinja2 import Environment, meta, exceptions


try:
    import jmespath
except:
    raise ValueError('python-jmespath package is not installed')


# ---- export function json_query ----

def json_query(data, expr):
	"""Query data into json record using jmespath query language"""
	return jmespath.search(expr, data)

