import random

class IDGenerator:
    ''' 
    ID Generator Class
    This provide ID assignment to instance created.
    '''
    def __init__(self,prefix=None):
        self.id = self.generateNewId(prefix)

    # Generate New Employee ID
    def generateNewId(self,prefix):
        try:
            prefix = str(prefix) + '::'
            serial = random.randrange(0,1000)
            pattern = prefix + str(serial)
            return pattern
        except:
            print('Id cannot be generated')
    


# employee_id = IDGenerator()
# employee_id = employee_id.generateNewEmployeeId()
# print(employee_id)