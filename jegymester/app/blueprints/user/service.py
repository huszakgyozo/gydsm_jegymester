from flask import request_tearing_down
from app.extensions import db
from app.blueprints.user.schemas import UserListSchema, UserResponseSchema

from app.models.user import User
from app.models.role import Role
from sqlalchemy import delete, null, select, and_
#ma
class UserService:

    @staticmethod

    def user_registrate(request):
        try:
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "E-mail already exist!"
            user = User(**request)
            user.set_password(user.password_hash)
            user.roles.append(
                db.session.execute(select(Role).filter_by(rolename="User")).scalar_one()           
                )
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            return False, "Incorrect User data!"
        return True, UserResponseSchema().dump(user)
    @staticmethod

    def user_login(request):
        try:
           user = db.session.execute(select(User).filter_by(email=request["email"])).scalar_one()
           if not user.check_password(request["password_hash"]):
            return False, "Incorrect e-mail or password!"
        except Exception as ex:
            return False, "Incorrect Login data!"
        return True, UserResponseSchema().dump(user)
    @staticmethod
    def user_list_all():
        user = db.session.execute(select(User)).scalars()
        return True, UserListSchema().dump(user, many=True)

