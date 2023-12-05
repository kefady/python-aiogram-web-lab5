from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.reply_keyboards import main_keyboard, pdf_keyboard

START_MESSAGE = ('Вітаю у світі PDFCraftBot! 🤖✨\n'
                 'Я готовий допомагати тобі з управлінням та редагуванням твоїх PDF-документів. '
                 'Якщо у тебе є які-небудь запитання або завдання, просто скажи мені, '
                 'і ми разом зробимо це легко та ефективно! 🚀')

HELP_MESSAGE = ('<b>Довідка по використанню PDFCraftBot:</b>\n\n'
                '🔹 <b>Витягнути текст з PDF 📖</b>: витягнення текстової інформації з PDF-документа.\n\n'
                '🔸 <b>Шифрування та дешифрування PDF файлу 🔐</b>: захист та розшифрування PDF-файлів.\n\n'
                '🔹 <b>Об\'єднання PDF 🔄</b>: об\'єднання кількох PDF-файлів в один документ.\n\n'
                '🔸 <b>Зменшення розміру PDF 💽</b>: оптимізація розміру PDF-файлу.\n\n'
                'Якщо у вас виникли питання чи потреба в допомозі, не соромтеся питати! 🤖✨')

router = Router()


@router.message(CommandStart())
async def cmd_start_handle(message: Message):
    await message.answer(text=START_MESSAGE, reply_markup=main_keyboard)


@router.message(F.text.lower() == 'довідка ℹ️')
async def cmd_help_handle(message: Message):
    await message.answer(text=HELP_MESSAGE, reply_markup=main_keyboard)


@router.message(F.text.lower() == 'операції з pdf-файлами 📄')
async def cmd_pdf_handle(message: Message):
    await message.answer(text='Оберіть дію з переліку.', reply_markup=pdf_keyboard)
