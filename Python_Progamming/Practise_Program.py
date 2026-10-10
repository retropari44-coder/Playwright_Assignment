class Parent1:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def add(self):
        sum = self.a + self.b
        print(sum)

class Parent2():
    def __init__(self, name, subj):
        self.name = name
        self.subj = subj

    def print_details(self):
        print(f"Student name is {self.name}")
        sum = 0
        for i in self.subj:
            sum += i
        print(f'Total Marks: {sum}')

class Child(Parent1, Parent2):
    def __init__(self, a, b, name, subj):
        Parent1.__init__(self,a,b)
        Parent2.__init__(self,name,subj)

object1 = Child(1,2,'Prithvi',[3,5,6])
object1.add()
object1.print_details()


