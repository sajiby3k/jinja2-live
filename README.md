# Jinja2 live parser with database

A Jinja2 live parser based on the live parser written by Antonin Bourguignon (http://github.com:abourguignon/jinja2-live-parser) with :
- a database for saving templates and data
- a copy to clipboard button
- import of all netaddr filters as they are available in ansible
- support of json_query filter built over jmespath (same as ansible)


All you need is Python and preferably [pip](https://pypi.python.org/pypi/pip). Can parse JSON and YAML inputs.


## Install

### Clone + pip + init database

    $ git clone https://github.com/PJO2/jinja2-live
    $ pip3 install -r requirements.txt
    $ python3 init_database.py
    $ python3 parser.py


## Usage
edit config.py, customize listen address and port.
You are all set, go to `http://localhost:8080/` and have fun.  
You can also add custom filters by creating a new file and adding its name to the list CUSTOM_MODULES in parser.py.


## Preview

![preview](preview.png)
![preview function list](preview-list.png)

