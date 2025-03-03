from database.model import User, Test, UserAnswers,  async_session
from sqlalchemy import select


async def createUser(tg_id: int, name:str, fam:str, phone:str):
    async with async_session() as session:
        user = User(tg_id=tg_id, name=name, fam=fam, phone=phone)
        session.add(user)
        await session.commit()
        return True
    
async def findUserByTG_ID(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if not user:
            return False
        return user
async def setAdminMethod(tg_id:int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if not user:
            return False
        user.usertype = "admin"
        await session.commit()
        return True
    
async def createTest(file_id: str, code_test: str, answers:str ):
    async with async_session() as session:
        test = await session.scalar(select(Test).where(Test.code_test == code_test))
        if test:
            return "error"
        newtest = Test(file_id=file_id, code_test=code_test, answers=answers)
        session.add(newtest)
        await session.commit()
        return "ok"
    
async def getAllTest():
    async with async_session() as session:
        tests = await session.execute(select(Test))
        return tests.scalars().all()
    
async def getTestByCode(code: int):
    async with async_session() as session:
        test = await session.scalar(select(Test).where(Test.code_test == code))
        return test
    
async def editTestHolati(code_test:int, holat: str):
    async with async_session() as session:
        test = await session.scalar(select(Test).where(Test.code_test == code_test) ) 
        if not test:
            return False
        test.test_holati = holat 
        await session.commit()
        return True
    
async def createUserAnswers(test_id: int, user_id: int, true_answers:int, false_answers: int, user_answers: str, score: str):
    async with async_session() as session:
        tekshiruv=await session.scalar(select(UserAnswers).where(UserAnswers.test_id==test_id, UserAnswers.user_id==user_id))
        if tekshiruv:
            return "ishlangan"
        useranswer = UserAnswers(
            test_id=test_id,
            user_id=user_id,
            true_answers = true_answers,
            false_answers=false_answers,
            user_answers=user_answers,
            score=score
        )
        session.add(useranswer)
        await session.commit()
        return "ishladi"

async def getUserAnswers(user_id: int):
    async with async_session() as session:
        query = (
            select(UserAnswers, Test).join(Test, Test.id == UserAnswers.test_id).where(UserAnswers.user_id==user_id)
        )
        testlar = await session.execute(query)
        if not testlar:
            return False
        return testlar
    
async def findUserAnswersUserList(test_id: int):
    async with async_session() as session:
        # testlar = await session.scalars(
        #     select( User.name, User.fam, UserAnswers.true_answers)
        #     .join(User, User.id == UserAnswers.user_id)
        #     .where(UserAnswers.test_id == test_id)
        # )
        # if not testlar:
        #     return False
        # for i in testlar:
        #     print(i)
        # return testlar.all()

        # ###############
        stm = (
            select(User, UserAnswers)
            .join(User, User.id == UserAnswers.user_id)
            .where(UserAnswers.test_id == test_id)  
        )
        result = await session.execute(stm)
        if not result:
            return False
        
        return result
    

async def getAllUsers():
    async with async_session() as session:
        users = await session.execute(select(User).where(User.usertype != "admin"))
        if not users:
            return False
        return users.scalars().all()