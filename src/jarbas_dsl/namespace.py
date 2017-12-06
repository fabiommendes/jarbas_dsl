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

    def get_attr_with_path(self, path):
        try:
            split_path = path.split('.')
            attr = self.__data[split_path[0]]

            for var in split_path[1:]:
                attr = attr.get(var, None)

            return attr
        except KeyError:
            raise AttributeError(path)
        