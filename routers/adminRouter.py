from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import os
# connect db

from database.sorovlar import createTest, getAllTest, getTestByCode, editTestHolati, findUserAnswersUserList, getAllUsers

# buttons
from helpers.buttons import test_button

# pdf 
from helpers.generaterPDF import createPDFUserAndUserAnswers, createPdfAllUser

adminrouter = Router()

class CrTest(StatesGroup):
    file_id = State()
    code_test = State()
    answers = State()

# 1 A
# 2 B
# 3 C


@adminrouter.message(F.text == "Test yaratish")
async def createtest(msg:Message, state: FSMContext):
    await msg.answer("Test faylingizni kiriting: ")
    await state.set_state(CrTest.file_id)

@adminrouter.message(CrTest.file_id)
async def getFile(msg: Message, state: FSMContext):
    if not msg.document:
        await msg.answer("Iltimos faylni yuboring: ")
        await state.set_state(CrTest.file_id)
        return
    
    if (msg.document.mime_type != "application/pdf") and (msg.document.mime_type != "application/msword"):
        await msg.answer("Iltimos Pdf yoki word faylni kiriting: ")
        await state.set_state(CrTest.file_id)
        return
    file_id = msg.document.file_id
    # fayl turi
    await state.update_data(file_id=file_id)
    await msg.answer("Testga maxsus kod bering")
    await state.set_state(CrTest.code_test)
@adminrouter.message(CrTest.code_test)
async def getTestCode(msg:Message, state: FSMContext):
    code = msg.text
    if len(code) == 0:
        await msg.answer("Iltimos testga kodni kiriting: ")
        await state.set_state(CrTest.code_test)
        return
    await state.update_data(code_test = code)
    await msg.answer("Tesning javoblarini kiriting: ")
    text = """
    1 A
    2 B
    3 C
"""
    await msg.answer(f"Javoblar quyidagi formatda yoziladi \n{text} ")
    await state.set_state(CrTest.answers)

@adminrouter.message(CrTest.answers)
async def getTestCode(msg:Message, state: FSMContext):
    code = msg.text
    if len(code) == 0:
        await msg.answer("Iltimos testga javoblarni kiriting: ")
        await msg.answer("Tesning javoblarini kiriting: ")
        text = """
    1 A
    2 B
    3 C
"""
        await msg.answer(f"Javoblar quyidagi formatda yoziladi \n{text} ")
        await state.set_state(CrTest.answers)
        return
    await state.update_data(answers = code)
    
    data = await state.get_data()    
    file_id = data.get("file_id")
    code_test = data.get("code_test")
    test = await createTest(file_id=file_id, code_test=code_test, answers=code)
    await msg.answer("Test yaratildi")
    await state.clear()


# test korish
# class ViewTest(StatesGroup):
#     code_test = State()



@adminrouter.message(F.text == "Testlar ro'yxati")
async def viewtests(msg:Message):
    # bazadan testni olish 
    allTests = await getAllTest()
    if not allTests and (len(allTests) == 0):
        await msg.answer("Testlar mavjud emas")
        return
    # botga yuborish]
    textmatni = []
    for text in allTests:
        textmatni.append(f"Test kodi: {text.code_test}\nTestning holati: {text.test_holati}\nTest /test_{text.code_test}\n")
    await msg.answer("\n".join(textmatni))


@adminrouter.message(F.text.startswith("/test_"))
async def testKorish(msg:Message):
    code_test = msg.text.split("_")[1]
    # bazadan testni olish
    test = await getTestByCode(int(code_test))
    if not test:
        await msg.answer("Siz tanlagan id dagi test mavjud emas")
        return
    await msg.answer("Siz tanlagan test quyidagicha: ")
    await msg.answer_document(test.file_id, caption=f"Holati: {test.test_holati}", reply_markup=await test_button(int(code_test)))

@adminrouter.callback_query(F.data.startswith("test_"))
async def queryData(callback: CallbackQuery):
    holat = callback.data.split("_")[1]
    inline_message_id = callback.inline_message_id
    code_test = callback.data.split("_")[2]
    if holat == "yaratildi":
        test = await editTestHolati(int(code_test), holat="yaratildi")
        if not test:
            await callback.answer("Hatolik yuzaga kelid")
            await callback.message.answer("Hatolik yuzaga kelid")
            return
        await callback.answer("Ok. Siz testni yaratish knopkasini bosdingiz.")
        await callback.message.edit_caption(inline_message_id=inline_message_id, caption="Holati yaratildi", reply_markup=await test_button(int(code_test)))
        return
    elif holat == "aktivate":
        test = await editTestHolati(int(code_test), holat="aktivate")
        if not test:
            await callback.answer("Hatolik yuzaga kelid")
            await callback.message.answer("Hatolik yuzaga kelid")
            return
        await callback.answer("Ok. Siz testni aktivatsiya qilish knopkasini bosdingiz.")
        await callback.message.edit_caption(inline_message_id=inline_message_id, caption="Holati aktive", reply_markup=await test_button(int(code_test)))
        return
    elif holat == "finish":
        test = await editTestHolati(int(code_test), holat="finished")
        if not test:
            await callback.answer("Hatolik yuzaga kelid")
            await callback.message.answer("Hatolik yuzaga kelid")
            return
        await callback.answer("Ok. Siz testni tugatish knopkasini bosdingiz.")
        await callback.message.edit_caption(inline_message_id=inline_message_id, caption="Holati tugatildi",  reply_markup=await test_button(int(code_test)))
        return
    elif holat == "users":
        await callback.answer("Ok. Siz testni ishtirokchilarini ko'rish knopkasini bosdingiz.")
        test = await getTestByCode(code=int(code_test))
        if not test:
            await callback.message.answer("Test mavjud emas")
            return
        
        usersandtest = await findUserAnswersUserList(test_id=test.id)
        if not usersandtest:
            await callback.message.answer("Testda ishtirokchilar mavjud emas")
            return
        
        pdf_path =await createPDFUserAndUserAnswers("Test ishtirokchilari ro'yxati", usersandtest, code_test)
        pdf = FSInputFile(pdf_path)
        await callback.message.answer_document(document=pdf, caption="Test ishtirokchilari ro'yxati")
        os.remove(pdf_path)
        return
    else:
        await callback.message.answer("Hatolik bo'ldi")

@adminrouter.message(F.text == "O'quvchilar ro'yxati (botdan ro'yxatdan o'tganlar)")
async def ishtirokchilarruyxati(msg: Message):
    allUsers = await getAllUsers()
    if not allUsers:
        await msg.answer("Ishtirokchilar mavjud emas")
        return
    pdf_path = await createPdfAllUser(alluser=allUsers) 
    pdf = FSInputFile(pdf_path)
    await msg.answer_document(document=pdf, caption="Ishtirokchilar ro'yxati")  
    try:
        os.remove(pdf_path)
    except:
        pass