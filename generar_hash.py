from werkzeug.security import generate_password_hash

password = 'ayman2004'
hash_result = generate_password_hash(password)
print(f"Hash para '{password}':")
print(hash_result)