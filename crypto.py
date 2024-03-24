import argparse
from cryptography.fernet import Fernet, InvalidToken
import pyperclip

def generate_or_load_key(key_file):
    try:
        with open(key_file, 'rb') as f:
            key = f.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    return key

def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    try:
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message
    except InvalidToken:
        return "Error: Invalid or corrupted message"

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt messages using cryptography")
    parser.add_argument("-k", "--key-file", default="key.txt", help="File to store/load encryption key")
    parser.add_argument("-e", "--encrypt", help="Encrypt a message")
    parser.add_argument("-d", "--decrypt", help="Decrypt a message")
    args = parser.parse_args()

    key = generate_or_load_key(args.key_file)

    if args.encrypt:
        message = args.encrypt
        encrypted_message = encrypt_message(message, key)
        encrypted_message_str = encrypted_message.decode()
        pyperclip.copy(encrypted_message_str)
        print("Encrypted message copied to clipboard:", encrypted_message_str)
    elif args.decrypt:
        encrypted_message_str = args.decrypt
        encrypted_message = encrypted_message_str.encode()
        decrypted_message = decrypt_message(encrypted_message, key)
        print("Decrypted message:", decrypted_message)
    else:
        print("Error: Please specify either -e to encrypt or -d to decrypt a message.")

if __name__ == "__main__":
    main()
