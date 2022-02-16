#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import os
import yaml

TEMPLATE_DIR='templates'
OUTPUT_DIR='static'
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
CONF = yaml.safe_load(open('plugins/backends/spidsaml2_backend.yaml', 'r'))

for f in os.listdir(TEMPLATE_DIR):
    if not f.startswith('_'):
        print(f)
        file = open(f'{OUTPUT_DIR}/{f}', 'w')
        file.write(env.get_template(f).render(CONF))
        file.close()

