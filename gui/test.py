class Obj:
    def __init__(self):
        self.a = 2
        self.b = 3

class A:
    def __init__(self):
        self.obj = Obj()

    def modify_obj(self):
        self.obj.a = -1

class B:
    def __init__(self, obj):
        self.obj = obj

    def modify_obj(self):
        self.obj.a = 100

a = A()
b = B(a.obj)
print(a.obj.a, b.obj.a)
a.modify_obj()
print(a.obj.a, b.obj.a)
b.modify_obj()
print(a.obj.a, b.obj.a)
