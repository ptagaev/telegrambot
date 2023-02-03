from sqlalchemy import Column, Integer, Date, ForeignKey, BIGINT, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import null
from sqlalchemy.orm import relationship
from database import Session

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, unique=True)
    username = Column(Text, nullable=True)

    @classmethod
    def user_exist(cls, user_id):
        session = Session()
        user = session.query(User).filter(User.user_id == user_id).first()
        session.close()
        return user


    @classmethod
    def add_user_to_database(cls, user_id, username):
        if not User.user_exist(user_id = user_id):
            session = Session()
            user = User(user_id = user_id, username = username)
            session.add(user)
            session.commit()
            session.close()

    @classmethod
    def users_to_txt(cls):
        session = Session()
        users = session.query(User).all()
        with open("users.txt", 'w', encoding="utf-8") as file:
            for user in users:
                file.write(f'{user.user_id} {user.username} \n')
                print(user.user_id, user.username)
        session.close()


    @classmethod
    def get_all(cls):
        session = Session()
        users = session.query(User.user_id).all()
        session.close()
        return [x[0] for x in users]
