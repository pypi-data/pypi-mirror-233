__all__ = ['XOne', 'XNumber']

class XOne():
    
    def __init__(self):
        pass
    
    def send_msg(self):
        return 'message_sent'
    
class XNumber(object):

    def __init__(self, n):
        self.value = n

    def val(self):
        return self.value

    def add(self, n2):
        self.value += n2.val()

    def __add__(self, n2):
        return self.__class__(self.value + n2.val())

    def __str__(self):
        return str(self.val())

    @classmethod
    def addall(cls, number_obj_iter):
        cls(sum(n.val() for n in number_obj_iter))
    