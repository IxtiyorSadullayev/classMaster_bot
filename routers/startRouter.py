from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# keyboards
from helpers.buttons import contact_request, user_buttons, admin_buttons


# sorovlar
from database.sorovlar import createUser, findUserByTG_ID, setAdminMethod

startRouter = Router()


class User(StatesGroup):
    name = State()
    fam = State()
    phone = State()



@startRouter.message(F.text == "/start")
async def startFunc(msg:Message, state: FSMContext):
    user = await findUserByTG_ID(tg_id=msg.from_user.id)
    print(user)
    if not user:
        await msg.answer("Ro'yxatdan o'ting. Ismingizni kiriting: ")
        await state.set_state(User.name)
        return
    elif user.usertype == "admin":
        await msg.answer("Admin botga hush kelibsiz", reply_markup=admin_buttons)
        return
    elif user.usertype == "user":
        await msg.answer("User oynasiga xush kelibsiz", reply_markup=user_buttons)

@startRouter.message(User.name)
async def nameUser(msg:Message, state:FSMContext):
    ism = msg.text
    if len(ism) == 0:
        await msg.answer("Ismingizni kiriting: ")
        await state.set_state(User.ism)
        return
    await state.update_data(name = ism)
    await msg.answer("Familiyangizni kiriting: ")
    await state.set_state(User.fam)

@startRouter.message(User.fam)
async def famUser(msg: Message, state:FSMContext):
    fam = msg.text 
    if len(fam) == 0:
        await msg.answer("Familiyangizni kiriting: ")
        await state.set_state(User.fam)
        return
    await state.update_data(fam = fam) 
    await msg.answer("Telefon raqamingizni qoldiring: ", reply_markup=contact_request)
    await state.set_state(User.phone)

@startRouter.message(User.phone)
async def phoneUser(msg:Message, state: FSMContext):
    if not msg.contact:
        await msg.answer("Telefon raqamingizni kiriting: ")
        await state.set_state(User.phone)
        return
    phone = msg.contact.phone_number
    data = await state.get_data()
    name = data.get("name")
    fam = data.get("fam")
    tg_id = msg.from_user.id
    user = await createUser(tg_id=tg_id, name=name, fam=fam, phone=phone)
    print(user)
    await state.update_data(phone=phone)
    await msg.answer("Siz ro'yxatdan o'tdingiz. User oynasiga hush kelibsiz", reply_markup=user_buttons)
    await state.clear()


@startRouter.message(F.text=="admin111222333")
async def adminBulish(msg:Message):
    user = await setAdminMethod(tg_id=msg.from_user.id)
    print(user)
    if user:
        await msg.answer("Siz admin bo'ldingiz", reply_markup=admin_buttons)
        return
    await msg.answer("Hato habar kiritdingiz")


@startRouter.message(F.text =="/help")
async def helpMessage(msg: Message):
    await msg.answer("Ushbu bot test ishlash uchun yaratilgan. Testlar haqida ma'lumotlar guruhlarda taqdim qilingan")