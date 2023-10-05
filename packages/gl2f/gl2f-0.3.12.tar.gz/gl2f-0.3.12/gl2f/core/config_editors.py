def max_image_size():
	w, h = map(int, input('width height (size in pixels): ').replace(',',' ').split(maxsplit=2)[:2])
	return (w, h)

def serve_port():
	return int(input('port: ').split(maxsplit=1)[0])

def host_name():
	return input('host name: ')

def get():
	return {
		'max-image-size': max_image_size,
		'serve-port': serve_port,
		'host-name': host_name,
	}