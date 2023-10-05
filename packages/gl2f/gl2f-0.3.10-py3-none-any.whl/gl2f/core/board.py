def table():
	return [
		# blogs
		{
			'id': '271474317252887717',
			'key': 'blogs/girls2',
			'group': 'girls2',
			'page': 'blogs',
		},

		{
			'id': '436708526618837819',
			'key': 'blogs/lovely2',
			'group': 'lovely2',
			'page': 'lovely2blogs',
		},

		{
			'id': '540071536506176315',
			'key': 'blogs/lucky2',
			'group': 'lucky2',
			'page': 'lucky2blogs',
		},

		# news
		{
			'id': '540067120025699131',
			'key': 'news/family',
			'page': 'familyNews',
		},

		{
			'id': '270441012457899173',
			'key': 'news/girls2',
			'group': 'girls2',
			'page': 'news',
		},

		{
			'id': '415001844964656065',
			'key': 'news/lovely2',
			'group': 'lovely2',
			'page': 'lovely2news',
		},
		{
			'id': '540071356465677115',
			'key': 'news/lucky2',
			'group': 'lucky2',
			'page': 'lucky2news',
		},

		{
			'id': '270810062216233612',
			'key': 'news/mirage2',
			'group': 'mirage2',
			'page': 'mirage2news',
		},

		# radio
		{
			'id': '455630760846558145',
			'key': 'radio/girls2',
			'group': 'girls2',
			'page': 'girls2radio',
		},

		{
			'id': '540071136604455739',
			'key': 'radio/lucky2',
			'group': 'lucky2',
			'page': 'lucky2radio',
		},

		# gtube
		{
			'id': '270809837141492901',
			'key': 'gtube',
			'page': 'gtube',
		},

		# commercial movie
		{
			'id': '504468501197489089',
			'key': 'cm',
			'page': 'commercialmovie',
		},


		{
			'id': '297314731440473169',
			'key': 'others',
			'page': 'others',
		},

		# Shangri-la
		{
			'id': '689409591506633568',
			'key': 'shangrila',
			'page': 'ShangrilaPG',
		},

		# Brand New World!
		{
			'id': '666819802651689824',
			'key': 'brandnewworld/cheer',
			'page': 'FirstLiveCheerForL2',
		},

		{
			'id': '664746725843403713',
			'key': 'brandnewworld/photo',
			'page': 'Lucky2FirstLivePG',
		},

		# daijoubu
		{
			'id': '660050132594590761',
			'key': 'daijoubu/photo',
			'page': '3rdAnnivPG',
		},

		{
			'id': '653506325782725569',
			'key': 'daijoubu/cheer',
			'page': '3rdAnnivCheerForG2',
		},

		# CL special live
		{
			'id': '639636551948567355',
			'key': 'cl',
			'page': 'CLsplivepg',
		},

		# fan meeting
		{
			'id': '613606146413953985',
			'key': 'fm/girls2-2022',
			'group': 'girls2',
			'page': 'G2fcmeetingpg',
		},

		{
			'id': '613607790937637825',
			'key': 'fm/lucky2-2022',
			'group': 'lucky2',
			'page': 'L2fcmeetingpg',
		},

		{
			'id': '770515521794737285',
			'key': 'fm/girls2-2023',
			'group': 'girls2',
			'page': 'G2FanMeetingPG2',
		},

		{
			'id': '750275859142673638',
			'key': 'fm/lucky2-2023',
			'group': 'lucky2',
			'page': 'L2FanMeetingPG2'
		},


		# enjoy the good days
		{
			'id': '558593359405384641',
			'key': 'enjoythegooddays',
			'group': 'girls2',
			'page': 'EnjoyTheGoodDaysBackstage',
		},

		# famitok
		{
			'id': '550521936032039739',
			'key': 'famitok/girls2',
			'group': 'girls2',
			'page': 'Girls2famitok',
		},

		{
			'id': '550521867736187707',
			'key': 'famitok/lucky2',
			'group': 'lucky2',
			'page': 'Lucky2famitok',
		},

		# lovely2 special live
		{
			'id': '527414639852520385',
			'key': 'lovely2live',
			'page': 'lovely2Live2021Diary',
		},

		# garugaku live
		{
			'id': '499846974107812667',
			'key': 'garugakulive',
			'page': 'garugakuliveDiary',
		},

		# chuwapane
		{
			'id': '357805845389509857',
			'key': 'chuwapane',
			'page': 'chuwapaneDiary',
		},

		# onlinelive
		{
			'id': '449506330521109545',
			'key': 'onlinelive2020',
			'page': 'onlineliveDiary',
		},

		# wallpaper
		{
			'id': '516921408022905897',
			'key': 'wallpaper',
			'page': 'wallpaper'
		},

		# ticket
		{
			'id': '335268051140216033',
			'key': 'ticket',
			'page': 'ticket',
		},

		# history
		{
			'id': '801380069393040517',
			'key': 'history/girls2',
			'page': 'Girls2history',
		},

		# Happy Summer
		{
			'id': '809652098881814530',
			'key': 'happysummer/pg',
			'page': 'HappySummerPG',
		},

		# activate
		{
			'id': '836873836174508033',
			'key': 'activate/pg',
			'page': 'activatePG',
		},
	]


def get(k, v):
	try:
		return next(x for x in table() if x[k] == v)
	except StopIteration:
		return None

def content_url(item):
	page = get('id', item['boardId'])['page']
	content = item['contentId']
	return f'https://girls2-fc.jp/page/{page}/{content}'


def tree():
	from . import member

	keys = [i['key'] for i in table()]

	first = {k.split('/')[0] for k in keys} | {'today'}
	tree = {
		f:{k.split('/')[1] for k in filter(lambda i:i.startswith(f'{f}/'), keys)}
		for f in first
	}

	mem_G2 = member.of_group('girls2').keys()
	mem_L2 = member.of_group('lucky2').keys()
	mem_l2 = member.of_group('lovely2').keys()

	tree['news'] |= {'today'}
	tree['blogs'] |= (mem_G2 | mem_L2 | mem_l2 | {'today'})
	tree['radio'] |= (mem_G2 | mem_L2)

	return tree

def active():
	return [
		'blogs/girls2',
		'blogs/lucky2',
		'news/family',
		'radio/girls2',
		'radio/lucky2',
		'gtube',
		'cm',
		'wallpaper',
	]