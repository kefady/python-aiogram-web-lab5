from aiogram.fsm.state import StatesGroup, State


class ExtractText(StatesGroup):
    file_path = State()


class MergePDF(StatesGroup):
    file_paths = State()


class EncryptDecryptPDF(StatesGroup):
    action = State()
    file_name = State()
    file_path = State()
    password = State()


class CompressPDF(StatesGroup):
    file_path = State()
