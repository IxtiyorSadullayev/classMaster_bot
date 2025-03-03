from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


contact_request = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Raqamni qoldiring", request_contact=True)]
    ],
    resize_keyboard=True,
    input_field_placeholder="Telefon raqamni qolding",
    one_time_keyboard=True
)

user_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Test ishlash"), KeyboardButton(text = "Natijalarim")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Kerakli tugmani bosing"
)

admin_buttons = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text="Test yaratish"), KeyboardButton(text="Testlar ro'yxati")],
        [KeyboardButton(text="O'quvchilar ro'yxati (botdan ro'yxatdan o'tganlar)")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Kerakli tugmani bosing"
)

async def test_button(code_test: int):
    test_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yaratildi", callback_data=f"test_yaratildi_{code_test}"),InlineKeyboardButton(text="Aktive qilish", callback_data=f"test_aktivate_{code_test}")],
        [InlineKeyboardButton(text="Tugatish", callback_data=f"test_finish_{code_test}")],
        [InlineKeyboardButton(text="Ishtirokchilar", callback_data=f"test_users_{code_test}")],
    ]
    )
    return test_buttons
