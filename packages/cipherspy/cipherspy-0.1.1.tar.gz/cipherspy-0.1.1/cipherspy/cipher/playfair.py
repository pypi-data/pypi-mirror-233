class PlayfairCipher:
    def __init__(self, key: str):
        self._key = self._prepare_key(key)
        self._matrix = self._generate_matrix()

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key: str):
        self._key = key

    @property
    def matrix(self):
        return self._matrix

    def _prepare_key(self, key):
        key = key.lower().replace("j", "i")
        unique_chars = []
        for char in key:
            if char not in unique_chars:
                unique_chars.append(char)
        alphabet = "abcdefghiklmnopqrstuvwxyz"
        for char in alphabet:
            if char not in unique_chars:
                unique_chars.append(char)
        return "".join(unique_chars)

    def _generate_matrix(self):
        matrix = [['' for _ in range(5)] for _ in range(5)]
        k = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = self._key[k]
                k += 1
        return matrix

    def _get_coordinates(self, char):
        for i, row in enumerate(self._matrix):
            if char in row:
                return i, row.index(char)
        return -1, -1

    def _encrypt_pair(self, pair):
        row1, col1 = self._get_coordinates(pair[0])
        row2, col2 = self._get_coordinates(pair[1])
        if row1 == row2:
            return self._matrix[row1][(col1 + 1) % 5] + self._matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            return self._matrix[(row1 + 1) % 5][col1] + self._matrix[(row2 + 1) % 5][col2]
        else:
            return self._matrix[row1][col2] + self._matrix[row2][col1]

    def _decrypt_pair(self, pair):
        row1, col1 = self._get_coordinates(pair[0])
        row2, col2 = self._get_coordinates(pair[1])
        if row1 == row2:
            return self._matrix[row1][(col1 - 1) % 5] + self._matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            return self._matrix[(row1 - 1) % 5][col1] + self._matrix[(row2 - 1) % 5][col2]
        else:
            return self._matrix[row1][col2] + self._matrix[row2][col1]

    def encrypt(self, plaintext):
        plaintext = plaintext.lower().replace("J", "I")
        plaintext = ''.join(filter(str.isalpha, plaintext))
        for i in range(1, len(plaintext)):
            if plaintext[i] == plaintext[i - 1] and plaintext[i].isalpha():
                plaintext = plaintext[:i] + "X" + plaintext[i:]
        ciphertext = ''
        i = 0
        while i < len(plaintext):
            pair = plaintext[i:i+2]
            if len(pair) == 1:
                pair += 'X'
                i += 1
            ciphertext += self._encrypt_pair(pair)
            i += 2
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.lower()
        plaintext = ''
        i = 0
        while i < len(ciphertext):
            pair = ciphertext[i:i+2]
            plaintext += self._decrypt_pair(pair)
            i += 2
        return plaintext


# Example usage:
if __name__ == "__main__":
    key = "secret"
    message = "hello world"
    playfair = PlayfairCipher(key)
    encrypted_message = playfair.encrypt(message)
    decrypted_message = playfair.decrypt(encrypted_message)

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)
