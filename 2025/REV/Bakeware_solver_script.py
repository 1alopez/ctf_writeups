from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Read the ciphertext from file
with open("Grandmas_Secret_Baking_Family_Recipe.enc", "rb") as f:
	ciphertext = f.read()

# Known values
key = b'OTHellOTotallyStealGoodRecipes!!'  # 32 bytes for AES-256
iv = b'1234567890123456'  # 16-byte IV

# Decrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)

# Try PKCS#7 unpadding first
try:
    plaintext = unpad(decrypted, 16)
    print("✅ Decrypted and unpadded (PKCS#7):", plaintext.decode())
except ValueError:
    # If padding fails, try stripping nulls
    print("⚠️ PKCS#7 padding failed. Trying null-stripping.")
    plaintext = decrypted.rstrip(b'\x00')
    try:
        print("Decrypted (null-stripped):", plaintext.decode())
    except:
        print("Could not decode plaintext.")
