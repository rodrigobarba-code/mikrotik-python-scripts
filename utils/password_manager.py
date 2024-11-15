import os
import base64
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, key_path='utils/.cypher.key') -> None:
        """Initializes the PasswordManager and loads or generates an encryption key."""
        self.key_path = key_path
        self.load_or_generate_key()

    def load_or_generate_key(self):
        """Loads the encryption key from a file or generates a new one if the file does not exist."""
        if os.path.exists(self.key_path):
            try:
                with open(self.key_path, 'rb') as keyfile:
                    self.key = keyfile.read()
                self.cipher_suite = Fernet(self.key)
                print(f"Key loaded from '{self.key_path}'")
            except Exception as e:
                print(f"Error loading key from file: {e}")
                raise
        else:
            print(f"File '{self.key_path}' not found, generating a new key.")
            self.generate_encryption_key()

    def encrypt_password(self, password: str) -> str:
        """Encrypts the password and returns it as a base64 encoded string."""
        try:
            encrypted_password = self.cipher_suite.encrypt(password.encode('utf-8'))
            return base64.b64encode(encrypted_password).decode('utf-8')
        except Exception as e:
            print(f"Error encrypting password: {e}")
            raise

    def decrypt_password(self, encrypted_password_base64: str) -> str:
        """Decrypts a base64 encoded encrypted password and returns the original password."""
        try:
            encrypted_password = base64.b64decode(encrypted_password_base64.encode('utf-8'))
            return self.cipher_suite.decrypt(encrypted_password).decode('utf-8')
        except Exception as e:
            print(f"Error decrypting password: {e}")
            raise

    def get_key(self) -> bytes:
        """Returns the encryption key."""
        return self.key

    def set_key(self, key: bytes) -> None:
        """Sets a new encryption key and updates the cipher suite."""
        self.key = key
        self.cipher_suite = Fernet(self.key)

    @staticmethod
    def generate_encryption_key(key_path='utils/.cypher.key') -> None:
        """Generates a new encryption key and saves it to the specified path if it does not exist."""
        try:
            # Check if the key file already exists
            if os.path.exists(key_path):
                print(f"Key already exists at '{key_path}'")
            else:
                # Generate and save a new key if the file is not found
                key = Fernet.generate_key()
                with open(key_path, 'wb') as key_file:
                    key_file.write(key)
                print(f"Key generated and saved to '{key_path}'")
        except Exception as e:
            print(f"Error generating or saving the key: {e}")
            raise
