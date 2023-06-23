from cryptography.fernet import Fernet

class SimpleEnDecrypt :
    def __init__(self, key=None) :
        if key is None :
            key = Fernet.generate_key()
        self.key = key
        self.fernet   = Fernet(self.key)
    
    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.fernet.encrypt(data) # 바이트형태이면 바로 암호화
        else:
            ou = self.fernet.encrypt(data.encode('utf-8')) # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.fernet.decrypt(data) # 바이트형태이면 바로 복호화
        else:
            ou = self.fernet.decrypt(data.encode('utf-8')) # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou



simpleEnDecrypt = SimpleEnDecrypt()

print()
print(f'대칭키 출력 : {simpleEnDecrypt.key}')
print()

plain_text = 'hello crypto world'
print(f'암호화할 텍스트 : {plain_text}')
print()

encrypt_text = simpleEnDecrypt.encrypt(plain_text)
print(f'암호화된 텍스트 : {encrypt_text}')
print()

decrypt_text = simpleEnDecrypt.decrypt(encrypt_text)
print(f'복호화된 텍스트 : {decrypt_text}')