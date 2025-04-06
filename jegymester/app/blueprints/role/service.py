from app.extensions import db
from app.blueprints.role.schemas import *

from app.models.role import Role
from sqlalchemy import delete, null, select, and_
#ma
class RoleService:
    @staticmethod
    def role_list_all():
        role = db.session.execute(select(Role)).scalars()
        return True, RoleListSchema().dump(role, many=True)

    @staticmethod
    def role_get_item(id):
        role = db.session.get(role, id)
        if not role:
            return False, "A szerepkör nem található!"
        return True, RoleResponseSchema().dump(role)

    @staticmethod
    def role_add(request):
        try:
            role = Role(**request)
            db.session.add(role)
            db.session.commit()

        except Exception as ex:
            return False, "role_add() hiba!"
        return True, RoleResponseSchema().dump()

    @staticmethod
    def role_update(id, request):
        try:
            role = db.session.get(Role, id)
            if role:
                role_name = request.get("role name")

                
                role.role_name = StatusEnum.validate(role_name)

                role.deleted = request.get("deleted")

                db.session.commit()
                return True, role
            else:
                return False, "Nincs ilyen role"
        except Exception as ex:
            return False, "role_update() hiba!"
        return True, RoleResponseSchema().dump(role)
            
    @staticmethod
    def role_delete(id):
        try:
            role = db.session.get(Role, id)
            if not role:
                return False, "A role nem található!"
            elif role:
                role.deleted=1
                db.session.commit()
                return True, "Az adott role törölve."

        except Exception as ex:
            return False, "role_delete() hiba!"
        return True, "OK"
    
