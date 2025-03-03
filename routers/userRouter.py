from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import os

userRouter = Router()
# database
from database.sorovlar import getTestByCode, createUserAnswers, findUserByTG_ID, getUserAnswers

# pdf
from helpers.generaterPDF import createPdfForUserNatija

class UserTestState(StatesGroup):
    code_test = State()
    answers = State()
    db_answers = State()
    test_id = State()


@userRouter.message(F.text=="Test ishlash")
async def userTestWork(msg: Message, state: FSMContext):
    await msg.answer("Hurmatli o'quvchi. O'qituvchi bergan test kodini kiriting.")
    await state.set_state(UserTestState.code_test)

@userRouter.message(UserTestState.code_test)
async def usercodetest(msg: Message, state: FSMContext):
    code_test = msg.text
    if len(code_test)==0:
        await msg.answer("Iltimos o'quvchi testning id raqamini kiriting: ")
        await state.set_state(UserTestState.code_test)
        return
    
    # bazadan testni topish
    test = await getTestByCode(int(code_test))
    if not test:
        await msg.answer("Kechirasiz ushbu koddagi test mavjud emas.")
        await state.clear()
        return
    if test and (test.test_holati == "yaratildi" or test.test_holati == "finished"):
        await msg.answer("Kechirasiz ushbu koddagi test hozir aktive emas.")
        return
    # foydalanuvchiga testni yoborish
    await state.update_data(db_answers = test.answers)
    await state.update_data(test_id=test.id)
    testlarsoni = test.answers.count(" ")
    print(testlarsoni)
    format = """
    1 A
    2 B
    3 C
"""
    await msg.answer_document(test.file_id, caption=f"Testning javoblarini quyidagi formatda kiriting:\n{format}\n\nTestlar soni: {testlarsoni} ta")
    await msg.answer("O'quvchi testni shoshilmay ishlang. Shartlarga amal qiling.")
    await state.set_state(UserTestState.answers)

@userRouter.message(UserTestState.answers)
async def useranswers(msg: Message, state: FSMContext):
    answers = msg.text 
    if len(answers) == 0:
        await msg.answer("Iltmos javoblarni shablon bo'yicha yuboring. ")
        await state.set_state(UserTestState.answers)
        return
    data = await state.get_data()
    db_answers = data.get("db_answers")
    test_id = data.get("test_id")
    user = await findUserByTG_ID(tg_id=int(msg.from_user.id))
    if len(answers) != len(db_answers):
        await msg.answer("Javoblaringiz kam yoki ko'p. Iltimos qaytadan urinib ko'ring")
        await state.set_state(UserTestState.answers)
        return
    javoblar = answers.split("\n")
    for index in range(len(javoblar)):
        if javoblar[index].split(" ")[0] != str(index+1):
            await msg.answer("Hato kod yozmang. Ketma ketlikni buzmang")
            break
            
    db_javoblar = db_answers.split("\n")
    testlar = []
    togri = 0
    notogri = 0
    for index in range(len(javoblar)):
        if javoblar[index].split(" ")[1] == db_javoblar[index].split(" ")[1]:
            testlar.append(f"{index+1} ✅")
            togri +=1
        else:
            testlar.append(f"{index+1} 🚫")
            notogri +=1
    natija = await createUserAnswers(test_id=int(test_id), user_id=user.id, true_answers=togri, false_answers=notogri, user_answers=answers, score="\n".join(testlar))
    if natija == "ishlangan":
        await msg.answer("Siz ushbu testni oldin ishlagansiz. Sizga ushbu testni yangilay olmaymiz.")
    await msg.answer(f"Sizning javoblaringiz: \n{"\n".join(testlar)}")
    await state.clear()

@userRouter.message(F.text == "Natijalarim")
async def usernatijalar(msg: Message):
    # bazadan izlab
    tg_id= msg.from_user.id
    user = await findUserByTG_ID(tg_id=tg_id)
    if not user:
        await msg.answer("Kechirasiz siz hali ro'yxatdan o'tmagansiz. /start kamandasini bosing.")
        return
    testlar = await getUserAnswers(user_id=user.id)
    if not testlar: 
        await msg.answer("Kechirasiz siz hali testlarda qatnashmadingiz.")
        return
    # text = []
    # for test in testlar:
    #     text.append(f"Test id: {test.test_id}\nTog'ri javoblar soni: {test.true_answers}\nNotog'ri javoblar soni: {test.false_answers}\nJavoblar: \n{test.score}\n\n")
    # agar bazada bo'lsa uni ekranga chiqaramiz
    pdf = await createPdfForUserNatija(testlar)
    await msg.answer_document(FSInputFile(pdf), caption="Sizning testlar natijalaringiz")
    os.remove(pdf)
    # await msg.answer(f"Siz jami {len(testlar)} ta testda ishtirok etgansiz.\n{" ".join(text)}")
    # agar bo'lmasa siz hali hech bir testda qatnamashmadingiz
