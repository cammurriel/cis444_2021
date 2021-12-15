import bcrypt

def salt_pass(user_password):
    password_to_salt = user_password
    salted = bcrypt.hashpw( bytes(password_to_salt,  'utf-8' ) , bcrypt.gensalt(10))
    print('NEW USER SALTED PASS ',salted)
    return salted

