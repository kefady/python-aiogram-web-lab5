import os
from random import randint

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import FileNotDecryptedError

from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.reply_keyboards import main_keyboard, pdf_keyboard, encrypt_decrypt_keyboard, merge_keyboard

from utils.states import ExtractText, EncryptDecryptPDF, MergePDF, CompressPDF

bot = Bot(token=os.getenv('BOT_TOKEN'))
router = Router()


async def download_file(message: Message) -> str | None:
    await message.answer(text='Завантаження файлу...')
    file_info = await bot.get_file(file_id=message.document.file_id)
    file_path = f'./data/pdf/{randint(0, 999999999)}_{file_info.file_path.split("/")[-1]}'
    await bot.download_file(file_info.file_path, file_path)
    if os.path.exists(file_path):
        return file_path
    else:
        return None


def extract_text_from_pdf(file_path) -> str:
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        extracted_text = '\n'.join(page.extract_text() for page in reader.pages)
    return extracted_text


@router.message(F.text.lower() == 'назад 🔙')
async def cmd_back_handle(message: Message):
    await message.answer(text='Що ви хочете зробити?', reply_markup=main_keyboard)


@router.message(F.text.lower() == 'вилучити текст 📄')
async def cmd_extract_text_handle(message: Message, state: FSMContext):
    await state.set_state(ExtractText.file_path)
    await message.answer(text='Відправте PDF-файл.')


@router.message(ExtractText.file_path)
async def pdf_file_handle(message: Message, state: FSMContext):
    if message.document and message.document.file_name.lower().endswith('.pdf'):
        # Download the PDF file
        file_path = await download_file(message=message)
        if file_path is None:
            await message.answer(text='Не вдалося завантажити файл. Будь ласка, спробуйте ще раз.')
            return

        # Extract the text from the PDF
        extracted_text = extract_text_from_pdf(file_path=file_path)
        if extracted_text == ' \n' or extracted_text == '':
            await message.answer(text='В PDF-файлі немає тексту.')
        else:
            await message.answer(text=f'Текст файлу:\n\n {extracted_text}')

        os.remove(file_path)
        await state.clear()
    else:
        await message.answer(text='Будь ласка, відправте коректний PDF-файл.')


@router.message(F.text.lower() == 'шифрування та дешифрування pdf файлу 🔐')
async def cmd_encrypt_decrypt_handle(message: Message, state: FSMContext):
    await state.set_state(EncryptDecryptPDF.action)
    await message.answer(text='Оберіть дію', reply_markup=encrypt_decrypt_keyboard)


@router.message(EncryptDecryptPDF.action)
async def encrypt_decrypt_action_handle(message: Message, state: FSMContext):
    if message.text.lower() == 'зашифрувати 🔐':
        await state.update_data({'action': 'encrypt'})
    elif message.text.lower() == 'дешифрувати 🔓':
        await state.update_data({'action': 'decrypt'})
    else:
        await message.answer(text='Оберіть дію', reply_markup=encrypt_decrypt_keyboard)

    await state.set_state(EncryptDecryptPDF.file_path)
    await message.answer(text='Відправте PDF-файл.')


@router.message(EncryptDecryptPDF.file_path)
async def pdf_file_handle(message: Message, state: FSMContext):
    if message.document and message.document.file_name.lower().endswith('.pdf'):
        file_path = await download_file(message=message)
        if file_path is None:
            await message.answer(text='Не вдалося завантажити файл. Будь ласка, спробуйте ще раз.')
            return
        await state.update_data({'file_path': file_path})
        await state.update_data({'file_name': message.document.file_name})
        await state.set_state(EncryptDecryptPDF.password)
        await message.answer(text='Введіть пароль.')
    else:
        await message.answer(text='Будь ласка, відправте коректний PDF-файл.')


@router.message(EncryptDecryptPDF.password)
async def pdf_password_handle(message: Message, state: FSMContext):
    await state.update_data({'password': message.text})
    data = await state.get_data()
    action = data.get('action')
    file_path = data.get('file_path')
    file_name = data.get('file_name')
    password = data.get('password')

    reader = PdfReader(file_path)
    writer = PdfWriter()

    if action == 'encrypt':
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)

    if action == 'decrypt':
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except FileNotDecryptedError:
                await message.answer(text='Невірний пароль. Будь ласка, спробуйте ще раз.')
                return
        for page in reader.pages:
            writer.add_page(page)

    with open(file_path, "wb") as f:
        writer.write(f)

    document = FSInputFile(file_path)
    document.filename = file_name.split('.')[0] + ('_encrypted.pdf' if action == 'encrypt' else '_decrypted.pdf')
    caption = 'Зашифрований файл' if action == 'encrypt' else 'Дешифрований файл'

    await message.answer_document(document=document, caption=caption, reply_markup=pdf_keyboard)

    os.remove(file_path)
    await state.clear()


@router.message(F.text.lower() == 'зменшення розміру pdf 📦')
async def cmd_compress_handle(message: Message, state: FSMContext):
    await state.set_state(CompressPDF.file_path)
    await message.answer(text='Відправте PDF-файл.')


@router.message(CompressPDF.file_path)
async def compress_file_handle(message: Message, state: FSMContext):
    if message.document and message.document.file_name.lower().endswith('.pdf'):
        file_path = await download_file(message=message)
        file_name = message.document.file_name.split('.')[0]
        if file_path is None:
            await message.answer(text='Не вдалося завантажити файл. Будь ласка, спробуйте ще раз.')
            return

        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        with open(file_path, "wb") as f:
            writer.write(f)

        document = FSInputFile(file_path)
        document.filename = file_name + '_compressed.pdf'

        await message.answer_document(document=document, caption='Оптимізований файл.')

        os.remove(file_path)
        await state.clear()
    else:
        await message.answer(text='Будь ласка, відправте коректний PDF-файл.')


@router.message(F.text.lower() == 'об\'єднання pdf 🔄')
async def cmd_merge_handle(message: Message, state: FSMContext):
    await state.set_state(MergePDF.file_paths)
    await message.answer(text='Відправте перший PDF-файл.')


@router.message(MergePDF.file_paths)
async def merge_file_handle(message: Message, state: FSMContext):
    if message.text is not None and message.text.lower() == 'об\'єднати pdf файли 🔄':
        data = await state.get_data()
        file_paths = data.get('file_paths', [])
        output_file_path = file_paths[0].replace('.pdf', '') + '_merged.pdf'

        merger = PdfWriter()
        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                merger.append(fileobj=file)

        with open(output_file_path, 'wb') as output:
            merger.write(output)

        document = FSInputFile(output_file_path)
        await message.answer_document(document=document, caption='Об\'єднаний файл.', reply_markup=pdf_keyboard)

        os.remove(output_file_path)
        for file_path in file_paths:
            os.remove(file_path)

        await state.clear()
    else:
        if message.document and message.document.file_name.lower().endswith('.pdf'):
            file_path = await download_file(message=message)
            if file_path is None:
                await message.answer(text='Не вдалося завантажити файл. Будь ласка, спробуйте ще раз.')
                return

            data = await state.get_data()
            file_paths = data.get('file_paths', [])
            file_paths.append(file_path)
            await state.update_data({'file_paths': file_paths})

            await message.answer(text='Відправте наступний PDF-файл.', reply_markup=merge_keyboard)
        else:
            await message.answer(text='Будь ласка, відправте коректний PDF-файл.', reply_markup=merge_keyboard)
