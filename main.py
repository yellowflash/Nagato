import sys;

class ConsCell:
    def __init__(self,car,cdr):
        self.car = car
        self.cdr = cdr
    
    def as_tuple(self):
        if self.cdr:
            return (self.car,) + self.cdr.as_tuple()
        return (self.car,)

    def __str__(self):
        return '(%s,%s)'%(str(self.car),str(self.cdr))

class Bindings:
    def __init__(self,bindings):
        self.bindings = bindings
    
    def find(self,var):
        if var in self.bindings:
            return self.bindings[var]

    def __str__(self):
        return "Bindings<%s>"%self.bindings

    @classmethod
    def of(cls,var,cons_cell):
        if cons_cell == None:
            print "%s Unbound"%var
            exit(1)
        if(var in cons_cell.car.bindings):
            return cons_cell.car.find(var);
        return Bindings.of(var,cons_cell.cdr)
    
    @classmethod
    def add(cls,bindings,name,value):
        bindings.car.bindings[name] = value

    @classmethod
    def add_to_root(cls,bindings,name,value):
        if bindings.cdr:
            Bindings.add_to_root(bindings.cdr,name,value)
        Bindings.add(bindings,name,value)

class Var:
    def __init__(self,name):
        self.name = name

    def apply(self,bindings,arguments):
        return Bindings.of(self.name,bindings)
    
    def __str__(self):
        return 'Var<%s>'%self.name

class Value:
    def __init__(self,value):
        self.value = value
    
    def apply(self,bindings,arguments):
        return self.value
    
    def __str__(self):
        return 'Value<%s>'%self.value

class Listing:
    @classmethod
    def parse(cls,program):
        stack = []
        current = []
        for item in program:
            if item[0] == '(':
                stack.append(current)
                current = [];
            elif item[0] == ')':
                tmp,stack = stack[-1],stack[:-1]              
                tmp.append(current)
                current = tmp
            else:
                current.append(item);
        return current;

class Form:
    def __init__(self,cell):
        self.cell = cell;
        
    @classmethod
    def create(cls,tree):
        if isinstance(tree,list):
            cell = None;
            for element in reversed(tree):
                cell = ConsCell(Form.create(element),cell)
            return Form(cell)
        if(tree.isdigit()): # I can be sure if its not list it should be a string
            return Value(int(tree))
        return Var(tree)
    
    def apply(self,bindings,arguments):
        return self.cell.car.apply(bindings,None).apply(bindings,self.cell.cdr);

    def __str__(self):
        return 'Form<%s>'%str(self.cell)

class Progn:
    def apply(self,binding,arguments):
        result = None
        result = arguments.car.apply(binding,arguments)
        if(arguments.cdr != None):
            result = self.apply(binding,arguments.cdr);
        return result
            
    @classmethod
    def execute(cls,tree,binding):
        print tree
        for form in tree:
            Form.create(form).apply(binding,None);


class Addition:
    def apply(self,bindings,arguments):
        result = 0
        current = arguments
        while current:
            value = current.car.apply(bindings,arguments)
            result += value;
            current = current.cdr
        return result


class Subtraction:
    def apply(self,bindings,arguments):
        result = 0
        current = arguments
        while current:
            result -= current.car.apply(bindings,arguments)
            current = current.cdr
        return result


class Multiplication:
    def apply(self,bindings,arguments):
        result = 1
        current = arguments
        while current != None:
            result *= current.car.apply(bindings,arguments)
            current = current.cdr
        return result


class Print:
    def apply(self,bindings,arguments):
        current = arguments
        while current != None:
            print current.car.apply(bindings,arguments),
            current = current.cdr
        print 

class DefineFunction:
    def apply(self,bindings,arguments):
        # Have to type check them before adding. 
        # name is a Var
        # arguments are Form
        # body is a form
        name = arguments.car.name 
        functionarguments = arguments.cdr.car.cell
        body = arguments.cdr.cdr.car
        return Bindings.add_to_root(bindings,name,Function(functionarguments,body,bindings));

class AnonymousFunction:
    def apply(self,bindings,arguments):
        functionarguments = arguments.car.cell
        body = arguments.cdr.car
        return Function(functionarguments,body,bindings);

class IfCondition:
    def apply(self,bindings,arguments):
        then_clause = arguments.cdr.car
        else_clause = arguments.cdr.cdr
        #they can be Var/Value/Form
        if(isinstance(then_clause,ConsCell)):
            then_clause = then_clause.car
        if(isinstance(else_clause,ConsCell)):
            else_clause = else_clause.car
        if(arguments.car.apply(bindings,arguments) != 0):
            return then_clause.apply(bindings,arguments);
        return else_clause.apply(bindings,arguments);

class Function:
    def __init__(self,arguments,body,bindings):
        self.parameters = arguments.as_tuple()
        self.body = body
        self.definition_bindings = bindings

    def apply(self,bindings,arguments):
        new_bindings = ConsCell(Bindings({}),self.definition_bindings)
        arguments = arguments.as_tuple()
        for i in xrange(len(arguments)):
            Bindings.add(new_bindings,self.parameters[i].name,arguments[i].apply(bindings,[]))
        return self.body.apply(new_bindings,None)
            
class List:
    def apply(self,bindings,arguments):
        current = None
        if(arguments != None):
            for item in reversed(arguments.as_tuple()):
                current = ConsCell(item.apply(bindings,arguments),current)
        return current;

class Car:
    def apply(self,bindings,arguments):
        return arguments.car.apply(bindings,arguments).car

class Cdr:
    def apply(self,bindings,arguments):
        return arguments.car.apply(bindings,arguments).cdr

class Cons:
    def apply(self,bindings,arguments):
        return ConsCell(arguments.car.apply(bindings,arguments),\
arguments.cdr.car.apply(bindings,arguments))

class Nil:
    def apply(self,bindings,arguments):
        return arguments.car.apply(bindings,arguments) == None

if __name__ == '__main__':
    program = open(sys.argv[1],'r').read();
    #Have to check why i cant chain the replace
    parsed = program.replace('(',' ( ')
    parsed = parsed.replace(')',' ) ')
    tree =  Listing.parse(parsed.split())
    root_bindings = ConsCell(Bindings({}),None)
    Bindings.add(root_bindings,'+',Addition())
    Bindings.add(root_bindings,'-',Subtraction())
    Bindings.add(root_bindings,'*',Multiplication())
    Bindings.add(root_bindings,'print',Print())
    Bindings.add(root_bindings,'defn',DefineFunction())
    Bindings.add(root_bindings,'fn', AnonymousFunction())
    Bindings.add(root_bindings,'progn',Progn())
    Bindings.add(root_bindings,'if',IfCondition())
    Bindings.add(root_bindings,'list',List())
    Bindings.add(root_bindings,'car',Car())
    Bindings.add(root_bindings,'cdr',Cdr())
    Bindings.add(root_bindings,'cons',Cons())
    Bindings.add(root_bindings,'nil?',Nil())
    Progn.execute(tree,root_bindings)
