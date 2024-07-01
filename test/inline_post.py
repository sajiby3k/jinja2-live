from __future__ import absolute_import, print_function

import os
import argparse
import requests

if __name__ == "__main__":
   """Main for inline: usage : """
   parser = argparse.ArgumentParser(description='Inline jinja2 rendering')
   parser.add_argument('template', help='template name')
   parser.add_argument('values', help='data file)')
   parser.add_argument('-t', '--type', choices=['json', 'yaml'], help='data type (json/yaml))')
   args = parser.parse_args()

   headers = {'User-Agent': 'Ark/5.0'}
   payload = {}

   with open(args.template) as x: 
       payload['template'] = x.read()
   with open(args.values) as x: 
       payload['values']   = x.read()
   payload['input_type'] = args.type
   payload['showwhitespaces'] = 0
   # print (payload)
   session = requests.Session()
   answer = session.post('http://127.0.0.1/convert',headers=headers,data=payload)
   print (answer.text)



