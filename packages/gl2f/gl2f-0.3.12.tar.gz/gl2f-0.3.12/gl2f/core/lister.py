import requests
from . import board, member, auth, util
import os, json, re
from datetime import datetime


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, dump=False, xauth=None):
	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/texts/{boardId}/contents',
		params={
			'size': str(size),
			'page': str(page),
			'order': str(order),
			'categoryId': categoryId
		},
		cookies={},
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
		})

	if not response.ok:
		print(response)
		print(response.reason)
		return

	data = response.json()

	if dump:
		name = board.get('id', boardId)['page']
		if categoryId:
			name += f'-{member.from_id(categoryId)[0]}'
		util.dump(dump, name, data)

	return data

def fetch_content(url, dump=False, xauth=None):
	page, contentId = re.search(
		r'https://girls2-fc\.jp/page/(?P<page>.+)/(?P<contentId>.+)',
		url
	).groups()
	boardId = board.get('page', page)['id']

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/texts/{boardId}/contents/{contentId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
		})

	if not response.ok:
		print(response)
		print(response.reason)
		return

	data = response.json()

	if dump:
		util.dump(dump, f'{page}-{contentId}', data)

	return data


def list_multiple_boards(boardId, args):
	# only returns the 'list' value of boards.
	# category id is fixed to None.
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	f = partial(fetch, size=10, page=1, xauth=auth.update(auth.load()), dump=args.dump)
	with ThreadPoolExecutor() as executor:
		results = executor.map(f, boardId)

	return sum((r['list'] for r in results), [])


def get_IDs(domain, m, g):
	data = member.get()[m]
	group_list = data['group']
	group = g if g in group_list else group_list[0]
	return board.get('key', f'{domain}/{group}')['id'], data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('board', type=str,
		help='board and group or member name')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--order', type=str, default='reservedAt:desc',
		help='order. {reservedAt, name} × {asc, desc}. default = reservedAt:desc.')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')

	parser.add_argument('--dump', type=str, nargs='?', const='.',
		help='dump response from server as ./response.json')


def in24h(i):
	return (datetime.now() - util.to_datetime(i['openingAt'])).total_seconds() < 24*3600

def list_contents(args):
	if args.board.startswith('blogs/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('blogs', sub, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

		elif sub == 'today':
			return list(filter(in24h, list_multiple_boards(
				[board.get('key', f'blogs/{g}')['id'] for g in ['girls2', 'lucky2']],
				args
			)))


	elif args.board.startswith('radio/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('radio', sub, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']


	elif args.board.startswith('news/'):
		sub = args.board.split('/')[1]
		if sub == 'today':
			boardId = board.get('key', 'news/family')['id']
			return list(filter(in24h, fetch(boardId, size=10, page=1, dump=args.dump)['list']))

		else:
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


	elif args.board == 'today':
		ret = list_multiple_boards([board.get('key', x)['id'] for x in board.active()], args)
		return sorted(filter(in24h, ret), key=lambda i:i['openingAt'], reverse=True)

	elif b := board.get('key', args.board):
		return fetch(b['id'], args.number, args.page, args.order, dump=args.dump)['list']


	elif os.path.isfile(args.board):
		with open(args.board, encoding='utf-8') as f:
			return json.load(f)['list']
