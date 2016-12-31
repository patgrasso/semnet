
ALL = "__all"

class Observable(object):

    def __init__(self):
        self.__observers = {}
        self.__observers[ALL] = []

    def register(self, observer, event=ALL):
        event = ALL if event is None else event
        if event not in self.__observers:
            self.__observers[event] = []
        self.__observers[event].append(observer)
        return self

    def emit(self, event, *args, **kwargs):
        if event in self.__observers:
            for observer in self.__observers[event]:
                observer.notify(self, event, *args, **kwargs)
        for observer in self.__observers[ALL]:
            observer.notify(self, event, *args, **kwargs)
        return self

