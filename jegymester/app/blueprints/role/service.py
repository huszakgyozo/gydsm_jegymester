import json
import re
from flask import Request
from app.extensions import db
from app.blueprints.role.schemas import *

from app.models.role import Role
from sqlalchemy import delete, null, select, and_
from app.models.user import User
from app.models.userrole import UserRole
# ma


class RoleService:
    @staticmethod
    def role_list_all():
        role = db.session.execute(select(Role)).scalars()
        return True, RoleListSchema().dump(role, many=True)

    @staticmethod
    def role_add(request):
        try:
            db.session.add(Role(rolename=request["rolename"]))
            db.session.commit()

        except Exception as ex:
            return False, "role_add() hiba!"+str(ex)
        return True, request["rolename"] + " hozzáadva!"

    @staticmethod
    def role_update(id, request):
        try:
            role = db.session.get(Role, id)
            if role:
                role.rolename = request["rolename"]
                db.session.commit()
                return True, role
            else:
                return False, "Nincs ilyen role"
        except Exception as ex:
            return False, "role_update() hiba!"+str(ex)
        return True, RoleResponseSchema().dump(role)

    @staticmethod
    def role_delete(id):
        try:
            role = db.session.get(Role, id)
            if not role:
                return False, "A role nem található!"
            elif role:
                db.session.delete(role)
                db.session.commit()
                return True, f"Az adott role {role.rolename} törölve."

        except Exception as ex:
            return False, "role_delete() hiba!"+str(ex)
        return True, "OK"

    @staticmethod
    def list_user_roles(user_id):
        try:
            user: User = db.session.get(User, user_id)
            roles: Role = [role for role in user.roles]
            return True, roles
        except Exception as ex:
            return False, "user_list_user_roles() hiba!"+str(ex)
