key = 2
salt = '3gjr8'

def encrypt(password):
    temp = ''
    for char in password:
        temp += chr(ord(char)+key)
    return temp + salt

def decrypt(password):
    temp = ''
    for char in password[:-len(salt)]:
        temp += chr(ord(char)-key)
    return temp