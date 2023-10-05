import re, html, os
from . import local
from ..ayame import sixel, terminal as term
from . import auth
from .config import config


ptn_paragraph = re.compile(r'<p.*?>(.*?)</p>')
ptn_media = re.compile(r'<fns-media.*?media-id="(.+?)".*?type="(.+?)".*?></fns-media>')
ptn_break = re.compile(r'<br>')
ptn_link = re.compile(r'<a href="(.+?)".*?>.+?</a>')
ptn_strong = re.compile(r'<strong.*?>(.*?)</strong>')
ptn_span = re.compile(r'<span.*?>(.*?)</span>')
ptn_http = re.compile(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))')


class MediaRep:
	def __init__(self, style, contentId, boardId, max_size=None):
		if style == 'type':
			self.rep = self.rep_type

		elif style == 'sixel' and sixel.init():
			from functools import partial

			local.refdir('cache')
			self.contentId = contentId
			self.dl = partial(dl_medium, boardId, self.contentId, xauth=auth.update(auth.load()))
			self.rep = self.rep_sixel
			self.max_size = max_size if max_size else config.get('max-image-size', (1000, 1000))

		elif style == 'none':
			self.rep = self.rep_none

		else:
			self.rep = self.rep_type_id

	def rep_none(self, p):
		return ptn_media.sub('', p)

	def rep_type(self, p):
		return ptn_media.sub(term.mod('[\\2]', term.dim()), p)

	def rep_type_id(self, p):
		return ptn_media.sub(term.mod('[\\2](\\1)', term.dim()), p)

	def rep_sixel(self, p):
		from io import BytesIO
		from PIL import Image

		match = ptn_media.search(p)
		if not match:
			return p
		i, t = match.group(1, 2)
		if t != 'image':
			return self.rep_type_id(p)

		if file:=local.search_media(i, self.contentId):
			image = Image.open(file)
		else:
			_, data = self.dl(mediaId=i)
			if data.ok:
				with open(os.path.join(local.refdir('cache'), i), 'wb') as f:
					f.write(data.content)
			image = Image.open(BytesIO(data.content))

		image = sixel.limit(image, self.max_size)
		ret = sixel.to_sixel(image)
		return ret


def line_kernel(p, mediarep):
	p = mediarep.rep(p)
	p = ptn_strong.sub(term.mod('\\1', term.color('white', 'fl'), term.bold(), term.underline()), p)
	p = ptn_link.sub(r'\1 ', p)
	p = ptn_span.sub(r'\1', p)
	p = ptn_break.sub('', p)

	# after processing tags
	p = html.unescape(p)
	p = ptn_http.sub(term.mod(r' \1 ', term.color('blue', 'fl')), p)

	return p


def lines(item, style, use_sixel, max_size=None):
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	f = partial(line_kernel, mediarep=MediaRep({
		'full': 'sixel' if use_sixel else 'type_id',
		'compact': 'sixel' if use_sixel else 'type_id',
		'compressed': 'type',
		'plain': 'none'
	}[style], item['contentId'], item['boardId'], max_size))

	with ThreadPoolExecutor(max_workers=5) as e:
		results = e.map(f, (p.group(1) for p in ptn_paragraph.finditer(item['values']['body'])))

		if style == 'full':
			yield from (f'{r}\n' for r in results)

		elif style == 'compact':
			yield from (f'{r}\n' for r in results if len(r))

		elif style == 'compressed':
			yield from (f'{r} ' for r in results if len(r))
			yield '\n'

		elif style == 'plain':
			yield from results


def dl_medium(boardId, contentId, mediaId, head=False, stream=False, streamfile=False, xauth=None):
	import requests

	class bad_response:
		ok = False

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/boards/{boardId}/contents/{contentId}/medias/{mediaId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
			'x-from': 'https://girls2-fc.jp',
		})

	if not response.ok:
		return response, bad_response

	meta = response.json()
	url = meta['accessUrl'] if streamfile else meta.get('originalUrl', meta['accessUrl'])

	if head:
		return meta, requests.head(url)
	else:
		return meta, requests.get(url, stream=stream)

def media_stat(body):
	types = [t for _, t in  ptn_media.findall(body)]
	return {key: types.count(key) for key in ['image', 'video']}
