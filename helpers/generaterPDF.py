from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.set_font("DejaVu", "", 14)  # ✅ Unicode shriftni ishlatish
        self.cell(0, 10, 'Creator -> Sadullayev Ixtiyor +998937123822', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 14)  # ✅ Unicode shriftni ishlatish
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_body(self, body:str):
        self.set_font("DejaVu", "", 14)  # ✅ Unicode shriftni ishlatish
        self.multi_cell(0, 10, body)
        self.ln()

async def createPDFUserAndUserAnswers(title: str, userandanswers: list, code_test):
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ Shriftni yuklash (faqat bir marta)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)  # ✅ Unicode shriftni o‘rnatish

    pdf.add_page()  # Endi shrift yuklangandan keyin sahifa qo‘shiladi
    pdf.chapter_body(body=f"Test kodi: {code_test}")
    pdf.chapter_body(body="Testda ishtirok etuvchilarning ro'yxati va ularning natijalari: ")
    # i = 1
    # for data in userandanswers:
    #     useranswers = data.UserAnswers.user_answers.split("\n")
    #     text = f"{i}. {data.User.fam} {data.User.name} natija: {data.UserAnswers.true_answers} javoblari: {" ".join(useranswers)}"
    #     print(text)
    #     pdf.chapter_body(body=text)
    #     i += 1
    i=1
    pdf.add_font("DejaVu", "B", "DejaVuSerif-Bold.ttf")
    pdf.set_font_size(size=12)
    with pdf.table(width=190, col_widths=(10, 50, 50,20, 60), cell_fill_color=200, cell_fill_mode="ROWS") as table:
        
        row = table.row()
        row.cell("T/r")
        row.cell("Familiya")    
        row.cell("Ism")
        row.cell("To'g'ri javoblar soni")
        row.cell("Belgilangan Javoblar")
        for data in userandanswers:
            useranswers = data.UserAnswers.user_answers.split("\n")
            row = table.row()
            row.cell(str(i))
            row.cell(str(data.User.fam))
            row.cell(str(data.User.name))
            row.cell(str(data.UserAnswers.true_answers))
            row.cell(" ".join(useranswers))
            i+=1


    pdf.output(f"pdf/{title}.pdf")
    return f"pdf/{title}.pdf"




async def createPdfForUserNatija(testlar: list):
    pdf = PDF()
    pdf.set_left_margin(10) 
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", "", 14)
    pdf.add_page()
    pdf.chapter_body(body="Sizning testlar natijalaringiz: ")
    i = 1
    # pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    # pdf.set_font("DejaVu", "", 12)
    pdf.add_font("DejaVu", "B", "DejaVuSerif-Bold.ttf", uni=True)
    pdf.set_font_size(size=12)
    with pdf.table(width=180, col_widths=(10, 20, 20, 20, 60, 50)) as table:
        row = table.row()
        row.cell("T/r")
        row.cell("Test code")
        row.cell("count true")
        row.cell("count false")
        row.cell("your answers")
        row.cell("created date")
        # table.row("T/r", "Test id", "To'g'ri javoblar soni", "Notog'ri javoblar soni", "Javoblar", "Vaqt")
        for test in testlar:
            # table.row(str(i), str(test.test_id), str(test.true_answers), str(test.false_answers), test.score, test.created)
            row = table.row()
            javoblar = test.UserAnswers.user_answers.split("\n")
            row.cell(str(i))
            row.cell(str(test.Test.code_test))
            row.cell(str(test.UserAnswers.true_answers))
            row.cell(str(test.UserAnswers.false_answers))
            row.cell(" ".join(javoblar))
            row.cell(str(test.UserAnswers.created).split(".")[0])
            i+=1
    
    pdf.output("pdf/natijalar.pdf")
    return "pdf/natijalar.pdf"

async def createPdfAllUser(alluser: list):
    pdf = PDF()
    pdf.set_left_margin(10) 
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", "", 14)
    pdf.add_page()
    pdf.chapter_body(body="Admindan boshqa barcha foydalanuvchilar ro'yxati berilgan")
    pdf.chapter_body(body="Barcha foydalanuvchilar: ")
    i=1
    pdf.add_font("DejaVu", "B", "DejaVuSerif-Bold.ttf", uni=True)
    pdf.set_font_size(size=12)
    with pdf.table(width=190, col_widths=(10, 40, 40, 50, 50)) as table:
        row = table.row()
        row.cell("T/r")
        row.cell("Familiya")
        row.cell("Ism")
        row.cell("Telegram Phone")
        row.cell("Ro'yxatdan o'tgan sana")
        for user in alluser:
            row = table.row()
            row.cell(str(i))
            row.cell(str(user.fam))
            row.cell(str(user.name))
            row.cell(str(user.phone))
            row.cell(str(user.created).split(".")[0])
            i+=1
    pdf.output("pdf/alluser.pdf")
    return "pdf/alluser.pdf"