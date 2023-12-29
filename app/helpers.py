import random
import string

from .models import School, Course

#generator for genertating a unique code for a new school that cannot be changed later
def accessCodeGen(type=None):
    # choose from all lowercase letter
    if type == None:
        return None
    elif type == 'course':
        #initalize string
        code = ''
        code = random.randint(00000, 99999)

        #check if code matches other course codes
        print(code)
        try:
            Course.objecs.filter(code=code)
            accessCodeGen(type)
        except:
            return code

    elif type == 'school':
        #initalize string
        code = ''
        #loop 3 times to generate a 3 block 4 character unique code
        for i in range(3):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(4))
        
            #check if this is the first iteration
            if len(code) > 0:
                code = code + '-' + result_str
            else:
                code = result_str
            
        print(code)

        #check if generated code matches any other schools codes for admins, teachers and parents
        if School.objects.filter(admin_code=code):
            accessCodeGen(type)
        if School.objects.filter(teacher_code=code):
            accessCodeGen(type)
        if School.objects.filter(parent_code=code):
            accessCodeGen(type)
        return code
        