import sf

images = {}

def load_sprite(filename, flip = ''):
    if not(filename in images.keys()):
        images[filename] = sf.Image.load_from_file(filename)
    s = sf.Sprite(images[filename])
    if flip == 'flip':
        s.flip_x(True)
    return s