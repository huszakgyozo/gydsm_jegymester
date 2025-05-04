from flask import request_tearing_down
from app.extensions import db
from app.blueprints.user.schemas import UserListSchema, UserResponseSchema, PayloadSchema, RoleSchema
from datetime import datetime, timedelta
from authlib.jose import jwt, JoseError
from flask import current_app
from app.models.user import User
from app.models.role import Role
from sqlalchemy import delete, null, select, and_

class UserService:

    @staticmethod
    def user_registrate(request):
        try:
            message="E-mail already exist!",db.session.execute(select(User.id).filter_by(email=request["email"])).scalar()
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, message,
            user = User(**request)
            user.set_password(user.password_hash)
            user.roles.append(
                db.session.execute(select(Role).filter_by(
                    rolename="User")).scalar_one()
            )
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            return False, "Incorrect User data!"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(User).filter_by(
                email=request["email"])).scalar_one()
            user_schema = UserResponseSchema().dump(user)
            user_schema["token"] = UserService.token_generate(user)
            if not user.check_password(request["password_hash"]):
                return False, "Incorrect e-mail or password!"
        except Exception as ex:
            return False, "Incorrect Login data!"
        return True, user_schema

    @staticmethod
    def user_list_all():
        user = db.session.execute(select(User)).scalars()
        return True, UserListSchema().dump(user, many=True)

    @staticmethod
    def token_generate(user: User):
        payload = PayloadSchema()
        payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
        payload.id = user.id
        payload.email= user.email
        payload.roles = RoleSchema().dump(obj=user.roles, many=True)
        return jwt.encode({'alg': 'RS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()

    @staticmethod
    def user_update(request):
       try:
            print("asd" ,request["id"])
            user = db.session.get(User, request["id"])
            if user:
                user.email = request["email"]
                user.phone = request["phone"]
                db.session.commit()
       except Exception as ex:
            return False, "User_update() hiba!"+str(ex)
       return True, UserResponseSchema().dump(user)