import traceback
from config import Config


class Base(object):

    def __init__(self, driver):
        self.driver = driver


class Location(object):

    def __init__(self, name, value, method="css"):
        self.name = name
        self.value = value
        self.method = Config.location.get(method.lower(), "CSS_SELECTOR")
        self.file = self.get_file_name()

    def get_file_name(self):
        for x in traceback.extract_stack():
            if x[-1] is not None:
                if self.__class__.__name__ in x[-1]:
                    return x[0].replace("\\", "/")

    def __repr__(self):
        return self.name.__str__()




