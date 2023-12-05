from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Довідка ℹ️')
        ],
        [
            KeyboardButton(text='Операції з PDF-файлами 📄')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Чим я можу допомогти?'
)

pdf_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вилучити текст 📄'),
            KeyboardButton(text='Об\'єднання PDF 🔄')
        ],
        [
            KeyboardButton(text='Шифрування та дешифрування PDF файлу 🔐')
        ],
        [
            KeyboardButton(text='Зменшення розміру PDF 📦'),
            KeyboardButton(text='Назад 🔙')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Що саме ви хочете зробити?'
)

encrypt_decrypt_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зашифрувати 🔐'),
            KeyboardButton(text='Дешифрувати 🔓')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Що саме ви хочете зробити?',
)

merge_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Об\'єднати PDF файли 🔄'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Уже закінчити завантаження файлів?'
)
