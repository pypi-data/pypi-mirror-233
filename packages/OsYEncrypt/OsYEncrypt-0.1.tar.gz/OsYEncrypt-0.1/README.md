
**1. Installing the Library:**
   First and foremost, users need to install the library using `pip`. They can do this by using the following command in the terminal:

   ```
   pip install OsYEncyption
   ```

**2. Usage:**
   ```python
   from OsYEncyption import osy_encode, osy_decode

   # The text the user wants to encrypt
   text_to_encode = "Hello, World!"
   # The key to be used for encryption
   key = 3

   # Encrypting the text
   encrypted_text = osy_encode(text_to_encode, key)
   print("Encrypted Text:", encrypted_text)

   # Decrypting the encrypted text
   decrypted_text = osy_decode(encrypted_text, key)
   print("Decrypted Text:", decrypted_text)
   ```

In this example, the `osy_encode` and `osy_decode` functions are imported and used for encrypting and decrypting the text. You can change `text_to_encode` and `key` according to your specific requirements.