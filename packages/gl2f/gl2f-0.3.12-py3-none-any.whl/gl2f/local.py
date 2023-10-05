import re
import os, json
from .core import pretty, local
from .core.config import config


def ls(args):
	items = [local.load_content(i) for i in sorted(local.listdir('contents'))]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	if not 'page' in args.format:
		args.format = 'page:' + args.format

	fm = pretty.from_args(args, items)
	for i in items:
		fm.print(i, encoding=args.encoding)


def clear_cache():
	if d:=local.refdir_untouch('cache'):
		for i in os.listdir(d):
			os.remove(os.path.join(d, i))


def install_to(dst):
	import shutil, socket

	src = local.package_data('site')

	if os.path.exists(dst):
		print(f'reinstalling {dst} that already exists')
		rm = shutil.rmtree if os.path.isdir(dst) else os.remove
		rm(dst)

	cp = shutil.copytree if os.path.isdir(src) else shutil.copyfile
	cp(src, dst)

	os.symlink(local.refdir('contents'), os.path.join(dst, 'contents'))

	index.main(site=dst, full=True)

	with open(os.path.join(dst, 'constants.js'), 'w', encoding='utf-8') as f:
		f.write(f'const hostname = "{(config["host-name"])}";')

	print(f'installed site into {dst}')


class index:
	@staticmethod
	def load():
		try:
			path = os.path.join(local.refdir_untouch('site'), 'index.js')
			with open(path, encoding='utf-8') as f:
				raw = f.read()
			return json.loads(re.sub(r'^.+?=', '', raw))

		except:
			return {}


	@staticmethod
	def value(i):
		from .core import board, article

		item = local.load_content(i)
		media = [i for i, _ in article.ptn_media.findall(item['values']['body'])]
		return {
			'title': item['values']['title'],
			'board': board.get('id', item['boardId'])['page'],
			'author': item.get('category', {'name':''})['name'],
			'date': item['openingAt'],
			'media': [''.join(x) for x in sorted(
				filter(lambda x:x[0] in media,
					(os.path.splitext(i) for i in local.listdir(os.path.join('contents', i)))
				),
				key=lambda x:media.index(x[0])
			)],
			'expired': item.get('closingAt', None),
			'body': build_body(item)
		}


	@staticmethod
	def create_table(contents):
		from concurrent.futures import ThreadPoolExecutor
		with ThreadPoolExecutor() as e:
			values = e.map(index.value, contents)
		return {k:v for k, v in zip(contents, values)}


	@staticmethod
	def main(site=None, full=False):
		if not site:
			site = local.refdir_untouch('site')

		if not site:
			print('site not installed. return')
			return

		if full:
			table = index.create_table(local.listdir('contents'))
		else:
			prev = index.load()
			contents = list(set(local.listdir('contents')).difference(prev.keys()))
			table = prev | index.create_table(contents)

		out = os.path.join(site, 'index.js')
		with open(out, 'w', encoding='utf-8') as f:
			print(f'const table={json.dumps(table, separators=(",", ":"), ensure_ascii=False)}', file=f)

		print(f'saved {out}')


def open_site():
	import webbrowser

	html = os.path.join(local.home(), 'site', 'index.html')

	if not os.path.exists(html):
		if 'n' != input('site not installed. install now? (Y/n)').lower():
			install_to(os.path.join(local.home(), 'site'))
		else:
			return
	else:
		index.main()

	webbrowser.open(f'file://{html}')

def build_body(item):
	from .core import article

	i = item['contentId']
	media_list = local.listdir(f'contents/{i}')

	def up(match):
		m, t = match.groups()
		try:
			p = next(p for p in media_list if p.startswith(m))
		except:
			return ''

		if t == 'image':
			return f'<img src=../contents/{i}/{p}></img>'
		elif t == 'video':
			return f'<video controls autoplay muted loop src=../contents/{i}/{p}></video>'
		else:
			return ''

	return article.ptn_media.sub(up, item['values']['body'])


def colored_diff_lines(left, right):
	import difflib
	from .ayame import terminal as term

	try:
		with open(left, encoding='utf-8') as l, open(right, encoding='utf-8') as r:
			return map(lambda l:
					term.mod(l, term.color('green')) if l.startswith('+')
					else term.mod(l, term.color('red')) if l.startswith('-')
					else l,
				difflib.unified_diff(l.readlines(), r.readlines(), fromfile=left, tofile=right)
			)
	except UnicodeDecodeError:
		return [
			'Not text files\n',
			term.mod(f'- {left}\n', term.color('red')),
			term.mod(f'+ {right}\n', term.color('green')),
		]

class ImportChecker:
	def __init__(self, left, right):
		from filecmp import dircmp, cmpfiles

		self.items = os.listdir(right)

		self.common = [i for i in self.items if os.path.isdir(os.path.join(left, i))]
		self.right_only = [i for i in self.items if i not in self.common]
		self.compare = {i:dircmp(os.path.join(left, i), os.path.join(right, i)) for i in self.common}

		self.identical = [k for k, v in self.compare.items() if not v.diff_files]
		self.diff_files = {k:v.diff_files for k, v in self.compare.items() if v.diff_files}
		self.right_only_files = {k: list(filter(
			lambda f: os.path.isfile(os.path.join(right, k, f)),
			v.right_only))
			for k, v in self.compare.items()
		}
		self.unknown = {k: list(filter(
			lambda i:os.path.isdir(os.path.join(right, k, i)),
			v.right_list))
			for k, v in self.compare.items()
		}

	def report(self):
		print(f'{len(self.items)} total contents')
		print('\t', ' '.join(self.items))

		print(f'{len(self.identical)} same contents')
		print('\t', ' '.join(self.identical))

		print(f'{len(self.right_only)} new contents')
		print(' '.join(self.right_only))

		print(f'{sum(map(len, self.right_only_files.values()))} new files')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.right_only_files.items() if v))

		print(f'{sum(map(len, self.diff_files.values()))} diff files')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.diff_files.items() if v))

		print(f'{sum(map(len, self.unknown.values()))} unchecked subdirs')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.unknown.items() if v))

	def all_diff_files(self):
		from itertools import chain
		return chain.from_iterable((os.path.join(c, f) for f in fs) for c, fs in self.diff_files.items())

	def new_files(self):
		from itertools import chain
		return chain.from_iterable((os.path.join(k, i) for i in v) for k, v in self.right_only_files.items())


def import_contents(src):
	import shutil, tempfile
	from .ayame import terminal as term

	left = local.refdir('contents')
	tempdir = tempfile.TemporaryDirectory()
	right = tempdir.name

	print(f'extracting archive ({os.path.getsize(src)/1024**3:.2f} GB).')
	shutil.unpack_archive(src, extract_dir=right)

	checker = ImportChecker(left, right)
	checker.report()

	def view():
		fm = pretty.Formatter(f='id:date-p:author:title', fd='%m/%d')
		for i in os.listdir(right):
			filepath = os.path.join(right, i, f'{i}.json')
			with open(filepath, encoding='utf-8') as f:
				fm.print(json.load(f))

	def copy_new_contents():
		for i in checker.right_only:
			shutil.copytree(os.path.join(right, i), os.path.join(left, i))
			print(f'copied: {i}')
		print()

	def copy_new_files():
		for file in checker.new_files():
			_left = os.path.join(left, file)
			if os.path.exists(_left):
				print(term.mod(f'file already exists {_left}', term.color('red')))
				continue
			shutil.copy2(os.path.join(right, file), _left)
			print(f'copied: {file}')
		print()

	def show_diff():
		nonlocal src
		diffs = [''.join(colored_diff_lines(os.path.join(left, f), os.path.join(right, f))) for f in checker.all_diff_files()]
		for diff in diffs:
			print(diff)

		if 'n' != input('Freeze conflicting files? (Y/n)').lower():
			default = os.path.splitext(f'diff-{os.path.basename(src)}')[0]
			o = input(f'Enter output directory name ({default})')
			if not o:
				o = default

			os.makedirs(o, exist_ok=True)

			with open(os.path.join(o, 'diff'), 'w', encoding='utf-8') as f:
				f.write(term.declip('\n'.join(diffs)))

			for file in checker.all_diff_files():
				src = os.path.join(right, file)
				dst = os.path.join(o, file)
				os.makedirs(os.path.dirname(dst), exist_ok=True)
				shutil.copy(src, dst)

	operations = list(filter(lambda x: x[2](), [
		('view all contents', view, lambda: True),
		('copy new contents', copy_new_contents, lambda: len(checker.right_only)),
		('copy new files', copy_new_files, lambda: any(checker.new_files())),
		('show diff', show_diff, lambda: len(checker.diff_files))
	]))
	selection = term.select([k for k, _, _ in operations])
	for s, (_, o, _) in zip(selection, operations):
		if s: o()

def export_contents(out):
	import shutil
	from datetime import datetime

	contents = local.refdir_untouch('contents')
	if not contents:
		print('contents not found')
		return

	out = os.path.abspath(out)
	if os.path.isdir(out):
		now = datetime.now().strftime("%Y%m%d%H%M%S")
		base = os.path.join(out, f'gl2f-contents-{now}')
	else:
		par, chi = os.path.split(out)
		if not os.path.isdir(par):
			print(f'{par} is not a directory')
			return

		base = out

	sizeInGb = local.stat()["contents"]["size"]/1024**3
	print(f'zipping contents into {base}.zip ({sizeInGb:.2f} GB)')
	shutil.make_archive(base, 'zip', root_dir=contents)

def get_local_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('8.8.8.8', 80))
		return s.getsockname()[0]
	except:
		return 'localhost'
	finally:
		s.close()

def serve(port, browse=False):
	import http.server, socketserver, socket, threading
	import webbrowser
	import tempfile

	with tempfile.TemporaryDirectory() as tmp:
		site = os.path.join(tmp, 'site')
		print(site)
		install_to(site)

		class Handler(http.server.SimpleHTTPRequestHandler):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, directory=site, **kwargs)

			def end_headers(self):
				self.send_header('Accept-Ranges', 'bytes')
				super().end_headers()

		url = f'http://{get_local_ip()}:{port}'
		with socketserver.ThreadingTCPServer(('0.0.0.0', port), Handler) as httpd:
			print(f'serving at {url}')

			server_thread = threading.Thread(target=httpd.serve_forever)
			server_thread.daemon = True
			server_thread.start()

			try:
				if browse:
					webbrowser.open(url)
				server_thread.join()
			except  KeyboardInterrupt:
				pass


def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('clear-cache').set_defaults(handler=lambda _:clear_cache())
	sub.add_parser('dir').set_defaults(handler=lambda _:print(local.home()))

	p = sub.add_parser('export')
	p.add_argument('-o', default='.')
	p.set_defaults(handler=lambda args:export_contents(args.o))

	p = sub.add_parser('import')
	p.add_argument('archive')
	p.set_defaults(handler=lambda args:import_contents(args.archive))

	sub.add_parser('index').set_defaults(handler = lambda _:index.main(full=True))
	sub.add_parser('install').set_defaults(handler=lambda _:install_to(os.path.join(local.home(), 'site')))

	p = sub.add_parser('ls')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.add_argument('--encoding')
	p.set_defaults(handler=ls, format='author:title')

	sub.add_parser('open').set_defaults(handler=lambda _:open_site())
	sub.add_parser('stat').set_defaults(handler=lambda _:print('\n'.join(f'{k:10} items: {v["count"]}, size: {v["size"]/(1024**3):,.2f} GB' for k, v in local.stat().items())))
	p = sub.add_parser('serve')
	p.add_argument('-p', '--port', type=int,  default=config['serve-port'])
	p.add_argument('--open', action='store_true')
	p.set_defaults(handler=lambda args:serve(args.port, args.open))
