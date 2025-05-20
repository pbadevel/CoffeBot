import segno, io
from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from settings import config

import hashlib
import os
import base64











def encode_phrase(data: str) -> str:
    # Генерируем ключ из SECRET_TOKEN
    key = hashlib.sha256(config.SECRET_TOKEN.encode()).digest()
    # Генерируем случайный вектор инициализации (IV)
    iv = os.urandom(16)
    # Настраиваем шифр
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Добавляем padding к данным
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    # Шифруем данные
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Объединяем IV с зашифрованными данными и кодируем в base64
    combined = iv + encrypted_data
    return base64.b64encode(combined).decode('utf-8')


def decode_phrase(encoded_data: str) -> str:
    # Декодируем из base64
    combined = base64.b64decode(encoded_data)
    # Извлекаем IV и зашифрованные данные
    iv = combined[:16]
    encrypted_data = combined[16:]
    
    # Генерируем ключ из SECRET_TOKEN
    key = hashlib.sha256(config.SECRET_TOKEN.encode()).digest()
    
    # Настраиваем дешифратор
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Дешифруем данные
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Удаляем padding
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8')





async def generate_qrcode(payload: str, format: str = "PNG") -> types.BufferedInputFile:
    qrcode = segno.make_qr(content=payload, error="H")
    buffer = io.BytesIO()
    # qrcode.save('qr.png', kind=format, scale=10)

    with buffer as f:     
        qrcode.save(f, kind=format, scale=10)
        buffer.seek(0)
        
        return types.BufferedInputFile(buffer.read(), filename='image.png')



def create_media_group(list_media_id: list[str], caption: str):
    '''
    list_media: ["p!123-abcd", "v!321-abcd"]
    '''
    use_caption = True
    
    media_builder = MediaGroupBuilder()
    for media in list_media_id:
        media_type, file_id = media.split('!')
        
        if media_type == 'p':
            if use_caption:
                media_builder.add_photo(media=file_id, caption=caption)
                use_caption=False
            else:
                media_builder.add_photo(media=file_id)
            
        

        elif media_type == 'v':
            if use_caption:
                media_builder.add_video(media=file_id, caption=caption)
                use_caption=False
            else:        
                media_builder.add_video(media=file_id)


    return media_builder.build()
