# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template, request, redirect, url_for, Response
from jinja2 import Environment, meta, exceptions
from random import choice
from inspect import getmembers, isfunction
from cgi import escape
import logging
import logging.handlers
import json
import yaml
import config
import sqlite3
import os
import csv
import tempfile


SQL_FILE = 'jinja_db.sqlite'
app = Flask(__name__)


# ---------------
# utilities: get custom filters and read nested yaml file
# ---------------
def get_custom_filters():
    import filters
    custom_filters = {}
    for m in getmembers(filters):
        if m[0].startswith('filter_') and isfunction(m[1]):
            filter_name = m[0][7:]
            custom_filters[filter_name] = m[1]

    return custom_filters

def sqlite2csv(csv_file):
    rc = False
    try:
        conn = sqlite3.connect(SQL_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templates")
        with open(csv_file, 'w+') as f:
           writer = csv.writer(f)
           print(csv_file)
           writer.writerow(['name', 'template', 'params', 'timestamp'])
           for row in cursor:
               print(row[0])
               writer.writerow(row)
        rc = True
    except:
        rc=False

    conn.commit()
    conn.close()
    return rc



# ---------------
# home page: display a demo pattern
# ---------------
@app.route("/")
def home():
    return render_template('index.html', flavour="index", custom_filters=get_custom_filters())

# ---------------
# SQL delete entry in template table
# ---------------
@app.route('/delete/<sql_template_name>')
def delete(sql_template_name):
    print("delete:", sql_template_name)
    try:
        conn = sqlite3.connect(SQL_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM templates WHERE name=?", (sql_template_name,))
        conn.commit()
        conn.close()
        return name_list()
    except sqlite3.Error as er:
        print( 'er:', er.message)
        return "Syntax error in SQL"

# ---------------
# SQL rename entry
# ---------------
@app.route('/rename_to', methods=['POST'])
def renameto():
     print("rename from :", request.form['from'], "to", request.form['to'])
     try:
         conn = sqlite3.connect(SQL_FILE)
         c = conn.cursor()
         c.execute("UPDATE templates SET name=? WHERE name=?", 
                       (request.form['to'], request.form['from']))
         conn.commit()
         conn.close()
         return name_list()
     except sqlite3.Error as er:
         print( 'er:', er.message)
         return "Syntax error in SQL"



# ---------------
# load: read an entry and display it
# ---------------
@app.route('/load/<sql_template_name>')
def load(sql_template_name):
    print("load:", sql_template_name)
    try:
        conn = sqlite3.connect(SQL_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM templates WHERE name=?", (sql_template_name,))
        row = c.fetchone()
        # found ? 
        if row is None:
           return render_template('not_found.html', key=sql_template_name)
        # assign variables to row
        (sql_template_name, template, values, dummytime) = row
        # print(sql_template_name, template, values, dummytime)
        conn.commit()
        conn.close()
        return render_template('load.html', 
                                flavour="load",
                                template=template, 
                                values=values, 
                                sql_template_name=sql_template_name,
                                link = request.base_url,
                                custom_filters=get_custom_filters())
    except sqlite3.Error as er:
        print( 'er:', er.message)
        return "Syntax error in SQL"


# ---------------
# list: display table template content
# ---------------
@app.route('/list', methods=['GET', 'POST'])
def name_list():
    print("list")
    try:
        conn = sqlite3.connect(SQL_FILE)
        c = conn.cursor()
        c.execute("SELECT name,timestamp FROM templates ORDER BY name")
        rows = c.fetchall()
        # print(rows)
        conn.commit()
        conn.close()
        return render_template('list.html', nb=len(rows), rows=rows, root=request.url_root)
    except:
        return ('<html><body><h2>Internal Error</h2></body></html>')


# ---------------
# csv: save database in csv format
# ---------------
@app.route('/csv', methods=['GET', 'POST'])
def send_csv():
    tmp_file = tempfile.gettempdir() + "/db.csv"
    print(tmp_file)
    if  sqlite2csv(tmp_file):
        with open(tmp_file) as fp:
            csv = fp.read()
        return Response(
                          csv,
                          mimetype="text/csv",
                          headers={"Content-disposition" : "attachment; filename=jinja2_templates.csv"})
         # os.remove(tmp_file)
    else:
        # os.remove(tmp_file)
        return ('<html><body><h2>Internal Error</h2></body></html>')
         
    



# ---------------
# save: record entry into table template
# ---------------
@app.route('/save', methods=['GET', 'POST'])
def save():
    print("save into", SQL_FILE)
    try:
        db_key = request.form['sql_template_name']
        conn = sqlite3.connect(SQL_FILE)
        c = conn.cursor()
        # update the SQL entry 
        c.execute("INSERT OR REPLACE INTO templates (name, template, params) VALUES (?, ?, ?)", 
                  (request.form['sql_template_name'], request.form['template'], request.form['values']))
        conn.commit()
        conn.close()
        print("entry {} updated".format(db_key))
        # display the same page
        return load(db_key)
    except sqlite3.Error as er:
        print( 'er:', er.message)
        return "Syntax error in SQL"


# ---------------
# convert: render template
# ---------------
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    jinja2_env = Environment()

    # Load custom filters
    custom_filters = get_custom_filters()
    # app.logger.debug('Add the following customer filters to Jinja environment: %s' % ', '.join(custom_filters.keys()))
    jinja2_env.filters.update(custom_filters)

    # Load the template
    try:
        jinja2_tpl = jinja2_env.from_string(request.form['template'])
    except (exceptions.TemplateSyntaxError, exceptions.TemplateError) as e:
        return "Syntax error in jinja2 template: {0}".format(e)


    values = {}
    # Check JSON for errors
    if request.form['input_type'] == "json":
            try:
                values = json.loads(request.form['values'])
            except ValueError as e:
                return "Value error in JSON: {0}".format(e)
    # Check YAML for errors
    elif request.form['input_type'] == "yaml":
            try:
                values = yaml.load(request.form['values'])
            except (ValueError, yaml.parser.ParserError, TypeError) as e:
                return "Value error in YAML: {0}".format(e)
    else:
            return "Undefined input_type: {0}".format(request.form['input_type'])

    # If ve have empty var array or other errors we need to catch it and show
    try:
        rendered_jinja2_tpl = jinja2_tpl.render(values)
    except (exceptions.TemplateRuntimeError, ValueError, TypeError) as e:
        return "Error in your values input filed: {0}".format(e)

    # Replace whitespaces with a visible character (using unicode character)
    if bool(int(request.form['showwhitespaces'])):
        rendered_jinja2_tpl = rendered_jinja2_tpl.replace(' ', u'\u02d9')

    return escape(rendered_jinja2_tpl)


if __name__ == "__main__":
    # Set up logging
    app.logger.setLevel(logging.__getattribute__(config.LOGGING_LEVEL))
    file_handler = logging.handlers.RotatingFileHandler(filename=config.LOGGING_LOCATION, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter(config.LOGGING_FORMAT))
    file_handler.setLevel(logging.__getattribute__(config.LOGGING_LEVEL))
    app.logger.addHandler(file_handler)

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )

