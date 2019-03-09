class Game:
    def __init__(self):
        self.week = Week()


class Week:
    def __init__(self):
        self.days = [Day()]*7 #This makes 7 copies of the same Day Object?
        #TODO Make sure this works.

class Day:
    def __init__(self):
        self.events = [Event()]*5 ## TODO

class Event:
    def __init__(self):
        self.name = ''
        self.poll = Poll()

class Poll:
    def __init__(self):
        self.poll_text = ''
        self.poll_options = [PollOptions()] *3 #Same copy pattern need to validate

class PollOptions:
    def __init__(self):
        self.option_text = ''
        self.outcome = PollOutcome()

class PollOutcome:
    def __init__(self):
        #Fundamental Game Resources
        self.socialness = 0
        self.sprintness = 0
        self.funocity = 0
        self.careernosity = 0
        #Text tweeted if poll option is chosen.
        self.payoff_text = ''

#Source: https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """
    str = ''
    int = 1
    dict = {}
    types = [type(str),type(int),type(dict)]
    if type(obj) in types:
        return obj
    #  Populate the dictionary with object meta data
    if type(obj) == type([]):
        obj_dict = serialize(obj)
    else:
        obj_dict =  {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
        }

    #  Populate the dictionary with object properties
        obj_dict.update(serialize(obj))

    return obj_dict

def serialize(obj):
    types = [type(''),type(0),type({})]
    if type(obj) in types:
        return obj
    elif type(obj) == type([]):
        serialized_list = []
        for object in obj:
            serialized_list.append(convert_to_dict(object))
        return serialized_list

    else:
        serialized_object = obj.__dict__
        for key in serialized_object:
            serialized_object[key] = convert_to_dict(serialized_object[key])
        return serialized_object


game = Game()
dict = convert_to_dict(game)
print(dict)
