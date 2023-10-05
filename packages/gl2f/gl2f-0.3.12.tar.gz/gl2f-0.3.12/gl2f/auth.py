from .core import auth

def set_token(token=None):
	if token == None:
		token = input('enter token:')

	if auth.update(token):
		print('success')
		auth.save(token)


def update_cli():
	before = auth.load()
	if not before:
		return
	after = auth.update(before)

	if after == '':
		pass
	elif before == after:
		print('up to date')
	else:
		print('token updated')


def login(email, password):
	if not email:
		email = input('email: ')

	if not password:
		password = input('password: ')

	if auth.login(email, password):
		print('success')


def add_args(parser):
	sub = parser.add_subparsers()

	p = sub.add_parser('login')
	p.add_argument('-u', '--email', type=str, default=None)
	p.add_argument('-p', '--password', type=str, default=None)
	p.set_defaults(handler=lambda args: login(args.email, args.password))

	sub.add_parser('remove').set_defaults(handler=lambda _:auth.remove())

	p = sub.add_parser('set-token')
	p.add_argument('token', nargs='?', type=str)
	p.set_defaults(handler=lambda args:set_token(args.token))

	sub.add_parser('update').set_defaults(handler=lambda _:update_cli())
