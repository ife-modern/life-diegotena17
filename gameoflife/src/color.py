class Color(dict):
    def __init__(self):
        super(Color, self).__init__({
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'cyan': (0, 255, 255),
            'yellow': (255, 255, 0),
            'pink': (255, 0, 255),
            'orange': (255, 130, 0),
            'brown': (150, 100, 0),
            'white': (255, 255, 255),
            'gray_light': (186, 186, 186),
            'gray': (127, 127, 126),
            'gray_dark': (76, 76, 76)
        })

    # Make dictionary keys available as attributes
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def __delattr__(self, key):
        del self[key]
