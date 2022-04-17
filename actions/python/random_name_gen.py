

def gen_random_name(length=8):
    import string
    import random
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

{1} = gen_random_name({0})
