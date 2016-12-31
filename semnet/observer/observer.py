
class Observer(object):

    def __init__(self, observable, event=None):
        observable.register(self, event)

    def notify(self, observable, event, *args, **kwargs):
        print("Got Event<{}>{}{} From {}".format(
            event, args, kwargs, observable))

