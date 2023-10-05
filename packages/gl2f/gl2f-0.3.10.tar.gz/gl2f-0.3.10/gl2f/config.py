from .core import config
import os

def view():
	import json
	path = config.filepath()
	if not os.path.isfile(path):
		print('file does not exist.')
		return

	with open(path, encoding='utf-8') as f:
		print(f.read())

def create():
	path = config.filepath()
	if os.path.isfile(path):
		print('file already exits. abort.')
		return

	config.save(config.default())
	print(f'created "{path}".')

def path():
	path = config.filepath()
	print(path if os.path.isfile(path) else 'file does not exist')

def edit():
	from .ayame import terminal as term
	from .core import config_editors

	editors = config_editors.get()
	data = config.load()

	keys = list(editors.keys())
	selected = term.select([f'{k}: {data.get(k, f"{str(config.config[k])} (default)")}' for k in keys])

	for key in [k for k, s in zip(keys, selected) if s]:
		try:
			data[key] = editors[key]()
		except Exception as e:
			print(term.mod('error', term.color('red')), e)

	config.save(data)

def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('create').set_defaults(handler=lambda _:create())
	sub.add_parser('path').set_defaults(handler=lambda _:path())
	sub.add_parser('view').set_defaults(handler=lambda _:view())
	sub.add_parser('edit').set_defaults(handler=lambda _:edit())