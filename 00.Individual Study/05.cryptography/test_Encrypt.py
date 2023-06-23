from cryptography.fernet import Fernet

key = Fernet.generate_key()
key = b"0rKTqtZ4GQJlecUE8zRfU1B-metwX61_2Iz6B66B5eo=" # 43개 문자, 맨 뒤에 '='

print(f'대칭키 : {key}')
print()

fernet = Fernet(key)

encrypt_str = fernet.encrypt(b'1234')
print("암호화된 문자열 : ", encrypt_str)
print()

decrypt_str = fernet.decrypt(encrypt_str)
print("복호화된 문자열 : ", decrypt_str)
print()