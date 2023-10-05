import os, json, re

def return_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def home():
	path = os.path.join(os.path.expanduser('~'), 'gl2f')
	return return_dir(path)

def refdir(path):
	return return_dir(os.path.join(home(), path))

def refdir_untouch(path):
	p = os.path.join(home(), path)
	return p if os.path.exists(p) else False

def listdir(path):
	p = refdir_untouch(path)
	if p:
		li = os.listdir(p)
		if '.DS_Store' in li:
			li.remove('.DS_Store')
		return li
	else:
		return []


def load_content(i):
	with open(os.path.join(refdir('contents'), i, f'{i}.json'), encoding='utf-8') as f:
		return json.load(f)

def search_media(mediaId, contentId=None):
	directory = refdir_untouch('cache')
	if directory:
		cache = os.path.join(directory, mediaId)
		if os.path.isfile(cache):
			return cache


	if not contentId:
		import glob
		cand = glob.iglob(f'contents/*/{mediaId}*', root_dir=home())
		try:
			return os.path.join(home(), next(cand))
		except:
			return None


	directory = refdir_untouch(f'contents/{contentId}')
	if not directory:
		return None

	pattern = re.compile(rf'{mediaId}.*')
	li = filter(pattern.match, os.listdir(directory))

	try:
		return os.path.join(directory, next(li))
	except:
		return None

def stat():
	return {os.path.basename(p): {
		'count': len(os.listdir(p)),
		'size': sum(sum( os.path.getsize(os.path.join(d,_f)) for _f in f ) for d,_,f in os.walk(p))
	} for p in filter(lambda x:x, map(refdir_untouch, ['contents', 'cache']))}

def package_data(f=''):
	import gl2f
	d, _ = os.path.split(gl2f.__file__)
	return os.path.join(d, 'data', f)


import subprocess
repo = os.path.abspath(os.path.join(os.path.split(__file__)[0], '../../.git'))
git = subprocess.run(f'git --git-dir {repo} log  -n1 --pretty=%h'.split(),
	stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL, shell=(os.name == 'nt'))
commit = git.stdout.rstrip('\n') if git.returncode == 0 else '-'*7

def log(message):
	from . import local
	from datetime import datetime
	with open(os.path.join(local.home(), 'log'), 'a') as f:
		f.write(f'{datetime.now()} {commit} {message}\n')
