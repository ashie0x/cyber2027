from wordfreq import zipf_frequency
import re
import math

def english_score(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())

    if not words:
        return 0

    scores = [
        zipf_frequency(word, "en")
        for word in words
    ]

    return sum(scores) / len(scores)


def caesar_decrypt(text, key):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - key) % 26 + base)
        else:
            result += char

    return result


def crack_caesar(ciphertext):
    candidates = []

    for key in range(26):
        plaintext = caesar_decrypt(ciphertext, key)
        score = english_score(plaintext)

        candidates.append((score, key, plaintext))

    return max(candidates)


def transposition_decrypt(ciphertext, key):
    num_cols = key
    num_rows = math.ceil(len(ciphertext) / num_cols)

    short_cols = num_cols - (len(ciphertext) % num_cols)

    if len(ciphertext) % num_cols == 0:
        short_cols = 0

    plaintext = [''] * num_rows
    index = 0

    for col in range(num_cols):
        col_length = num_rows - (
            1 if col >= num_cols - short_cols else 0
        )

        for row in range(col_length):
            plaintext[row] += ciphertext[index]
            index += 1

    return ''.join(plaintext)


def crack_transposition(ciphertext):
    candidates = []

    for key in range(2, 20):
        plaintext = transposition_decrypt(ciphertext, key)
        score = english_score(plaintext)

        candidates.append((score, key, plaintext))

    return max(candidates)


caesar_text = (
    "TY ESP LQEPCYZZY ESP HTYO NSLYRPO "
    "OTCPNETZY LYO ESP NWZFOD XZGPO EZHLCO "
    "ESP DPL HSPY ESP WTRSED HPYE ZFE "
    "ESP NSTWOCPY EZWO"
)

transposition_text = (
    "TT TTS OHAEIEAS TWHTMHO BRORTV TEB REEEU TU OYTEWE ETO EERDHDTL EDE IEONC TSIEGH TR EBTN GOW DS EELH TKE  TMIOACNT IEAHSCHSHMLNYUE SB RR AAEEIL  SWFCRLRELUDN "
)


score, key, plaintext = crack_caesar(caesar_text)

print("===== CAESAR CIPHER =====")
print("Key:", key)
print("Plaintext:", plaintext)
print("Score:", score)

score, key, plaintext = crack_transposition(transposition_text)

print("\n===== TRANSPOSITION CIPHER =====")
print("Key:", key)
print("Plaintext:", plaintext)
print("Score:", score)
