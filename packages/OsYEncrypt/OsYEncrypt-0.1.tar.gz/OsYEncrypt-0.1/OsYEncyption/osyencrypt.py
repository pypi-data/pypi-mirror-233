def osy_encode(text, key):
    encrypted_text = ''
    for char in text:
        ascii_value = ord(char)
        # تطبيق العملية على القيمة العشرية
        encrypted_value = ascii_value + key
        # تحويل القيمة المشفرة إلى النظام السداسي عشري
        hex_value = format(encrypted_value, 'x')
        # إضافة القيمة المشفرة إلى النص المشفر
        encrypted_text += hex_value
    return encrypted_text

# فك تشفير
def osy_decode(encrypted_text, key):
    decrypted_text = ''
    for i in range(0, len(encrypted_text), 2):
        hex_value = encrypted_text[i:i+2]
        # تحويل القيمة السداسية إلى العشرية
        encrypted_value = int(hex_value, 16)
        # تطبيق العملية المعكوسة على القيمة المشفرة
        decrypted_value = encrypted_value - key
        # تحويل القيمة المفكوكة إلى حرف
        decrypted_char = chr(decrypted_value)
        # إضافة الحرف المفكوك إلى النص المفكوك
        decrypted_text += decrypted_char
    return decrypted_text