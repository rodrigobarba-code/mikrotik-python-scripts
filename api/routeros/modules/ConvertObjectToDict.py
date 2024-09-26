class ConvertObjectToDict:
    def __init__(self, obj):
        self.obj = obj

    def convert(self):
        if isinstance(self.obj, dict):
            return self.obj
        else:
            return self.obj.__dict__
