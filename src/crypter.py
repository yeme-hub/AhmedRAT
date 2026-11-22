import random

def xor_encrypt_hex(data, key):
    # تحويل كل حرف إلى Hex بعد عمل XOR
    return ''.join(format(ord(c) ^ key, '02x') for c in data)

def encrypt_strings(token, chat):
    key = random.randint(1, 255)
    enc_token = xor_encrypt_hex(token, key)
    enc_chat = xor_encrypt_hex(chat, key)
    return enc_token, enc_chat, key

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        t, c, k = encrypt_strings(sys.argv[1], sys.argv[2])
        print(f"TOKEN:{t}\nCHAT:{c}\nKEY:{k}")
