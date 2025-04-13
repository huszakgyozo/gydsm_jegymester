from app.extensions import db
from app.blueprints.userrole.schemas import (
    UserroleResponseSchema,
    UserroleListSchema,
    UserroleRequestSchema,
    UserroleUpdateSchema
)
from app.models.userrole import UserRole
from sqlalchemy import select


class UserroleService:
    @staticmethod
    def userrole_list_all():
        userroles = db.session.execute(select(UserRole)).scalars()
        return True, UserroleListSchema().dump(userroles, many=True)

    @staticmethod
    def userrole_get_item(id):
        userrole = db.session.get(UserRole, id)
        if not userrole:
            return False, "A userrole nem található!"
        return True, UserroleListSchema().dump(userrole)

    @staticmethod
    def userrole_update(olduser_id, oldrole_id, request):
        try:
            userrole = db.session.get(UserRole, (olduser_id, oldrole_id))
            if userrole:
                userrole.role_id = request["newrole_id"]
                db.session.commit()
            else:
                return False, "A userrole nem található!"
        except Exception as ex:
            return False, "userrole_update() hiba!"+str(ex)
        return True, UserroleResponseSchema().dump(userrole)

    @staticmethod
    def userrole_delete(userid, roleid):
        try:
            userrole = db.session.get(UserRole, (userid, roleid))
            if not userrole:
                return False, "Userrole nem található!"
            db.session.delete(userrole)
            db.session.commit()
            return True, "Az adott userrole törölve."
        except Exception as ex:
            return False, "userrole_delete() hiba!"+str(ex)

    @staticmethod
    def userrole_add(request):
        try:
            userrole = UserRole(
                user_id=request["user_id"],
                role_id=request["role_id"]
            )
            db.session.add(userrole)
            db.session.commit()
        except Exception as ex:
            return False, "userrole_add() hiba!"+str(ex)
        return True, UserroleResponseSchema().dump(userrole)