import random
import string

from django.db import models

from .models import School

#generator for genertating a unique code for a new school that cannot be changed later
def CodeGen():
    # choose from all lowercase letter
    main_str = ''
    for i in range(3):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(4))
        if len(main_str) > 0:
            main_str = main_str + '-' + result_str
        else:
            main_str = result_str
    if School.objects.filter(code=main_str):
        CodeGen()
    else:
        return main_str