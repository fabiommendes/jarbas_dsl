class Namespace:
    """
    Wraps a mapping into a namespace object.
    """

    def __init__(self, data=None):
        self.__data = {} if data is None else data

    def __getattr__(self, attr):
        try:
            return self.__data[attr]
        except KeyError:
            raise AttributeError(attr)
    
    # def __setattr__(self, attr, value):
    #     self.__data[attr] = value

    def __delattr__(self, attr):
        try:
            del self.__data[attr]
        except KeyError:
            raise AttributeError('attribute %s does not exist!' % attr)


    def get_value(self, keys):
        d = self.__data
        for key in keys:
            d = d[key]
        return d

    def set_value(self, path, value):
        keys = path.split('.')
        d = self.get_value(keys[:-1])
        d[keys[-1]] = value

    def get_attr(self, path):
        keys = path.split('.')
        d = self.__data
        for key in keys:
            d = d[key]
        return d
   