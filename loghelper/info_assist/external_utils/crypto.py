from cryptography.fernet import Fernet
from loghelper.settings._base import CRYPTO_KEY

cipher = Fernet(CRYPTO_KEY)

# Пример бинарных данных
data = b"Это пример бинарных данных."

# Шифрованим
encrypted_data = cipher.encrypt(data)
print(f"Зашифрованные данные: {encrypted_data}")

# Расшифрование
decrypted_data = cipher.decrypt(encrypted_data)
# print(f"Расшифрованные данные: {decrypted_data.decode()}")
