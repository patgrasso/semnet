
import pickle
from semnet.observer import Observer

class PickleStore(Observer):

    def __init__(self, semnet, save_file):
        super(PickleStore, self).__init__(semnet)
        self.semnet = semnet
        self.save_file = save_file

    def notify(self, semnet, event, *args, **kwargs):
        self.dump(self.save_file)

    def dump(self, f):
        if type(f) == str:
            f = open(f, "wb")
            pickle.dump(self.semnet, f)
            f.close()
        else:
            pickle.dump(self.semnet, f)

    @staticmethod
    def load(f):
        if type(f) == str:
            f = open(f, "rb")
            semnet = pickle.load(f)
            semnet._Observable__observers = {}
            f.close()
            return semnet
        semnet = pickle.load(f)
        semnet._Observable__observers = {}
        return semnet




