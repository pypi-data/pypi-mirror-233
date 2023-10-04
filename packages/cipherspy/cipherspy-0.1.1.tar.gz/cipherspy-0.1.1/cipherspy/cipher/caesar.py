class CaesarCipher:
    def __init__(self, shift):
        self._shift_amount = shift

    @property
    def shift_amount(self):
        return self._shift_amount

    def _shift_char(self, char):
        if char.isalpha():
            shift_amount = self._shift_amount % 26
            if char.islower():
                shifted = ord(char) + shift_amount
                if shifted > ord('z'):
                    shifted -= 26
                return chr(shifted)
            elif char.isupper():
                shifted = ord(char) + shift_amount
                if shifted > ord('Z'):
                    shifted -= 26
                return chr(shifted)
        return char

    def encrypt(self, plaintext):
        encrypted_text = ''.join([self._shift_char(char) for char in plaintext])
        return encrypted_text

    def decrypt(self, ciphertext):
        self._shift_amount = -self._shift_amount
        decrypted_text = ''.join([self._shift_char(char) for char in ciphertext])
        self._shift_amount = -self._shift_amount
        return decrypted_text


# Example usage:
if __name__ == "__main__":
    shift = 3
    message = "hello world"
    playfair = CaesarCipher(shift)
    encrypted_message = playfair.encrypt(message)
    decrypted_message = playfair.decrypt(encrypted_message)

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)
