import argparse
from . import opener, ls, cat, dl, search, completion
import sys, time

def version():
	try:
		from .__version__ import __version__
		return f'gl2f {__version__}'
	except:
		return 'No version info found'

def main():
	from . import auth, local, config
	from .core import lister
	from .ayame import sixel

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser.add_argument('-v', '--version', action='version', version=version())

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)

	config.add_args(subparsers.add_parser('config'))

	local.add_args(subparsers.add_parser('local'))

	subparsers.add_parser('sixel').set_defaults(handler=lambda args:sixel.check())

	completion.add_args(subparsers.add_parser('completion'))

	for cmd in [cat, dl, ls, opener, search]:
		cmd.add_args(subparsers.add_parser(cmd.name()))


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)


if __name__ == '__main__':
	main()