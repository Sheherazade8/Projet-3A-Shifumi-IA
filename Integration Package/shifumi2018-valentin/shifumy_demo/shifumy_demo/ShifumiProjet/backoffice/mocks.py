
class Model():
    Model = [
        {'id': 1, 'titre': "SVM", 'WinRank': "58%"},
        {'id': 2, 'titre': "Tree", 'WinRank': "53%"},
        {'id': 3, 'titre': "Neutwork Neuronal", 'WinRank': "78%"},

    ]

    @classmethod
    def all(cls):
        return cls.Model


    def findById(cls,id):
        return cls.Model[id]


