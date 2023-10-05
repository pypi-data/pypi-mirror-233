from .core import local, board

def generate():
	with open(local.package_data('completion.bash')) as f:
		source = f.read()

	tree = board.tree()

	source = source\
		.replace('## REPLACE_PAGES_FIRST', f'''
    COMPREPLY=( $(compgen -W "{' '.join({k + ('/' if len(v)>0 else '') for k, v in tree.items()})}" -- ${{cur}}) )
'''
		)\
		.replace('## REPLACE_PAGES_SECOND', ''.join(f'''
      {k})
        COMPREPLY=( $(compgen -W "{' '.join(set(v))}" -P "${{prefix}}/" -- ${{realcur}}) )
        ;;
'''
			for k, v in tree.items() if len(v)>0)
		)

	return source


def add_args(parser):
	parser.set_defaults(handler=lambda _:print(generate()))
