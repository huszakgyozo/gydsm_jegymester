# from app.extensions import db
# from app.blueprints.userrole.schemas import *

# from app.models.userrole import UserRole 

# from sqlalchemy import null, select, and_

# from jegymester.app.blueprints.userrole.schemas import UserroleResponseSchema, UserroleListSchema, UserroleRequestSchema, UserroleUpdateSchema


# class UserroleService:
#     @staticmethod
#     def userrole_list_all():
#         userrole = db.session.execute(select(UserRole)).scalars().all()
#         return True, UserroleListSchema().dump(userrole, many=True)

   
#     @staticmethod
#     def userrole_get_item(id):
#         userrole = db.session.get(UserRole, id)
#         if not userrole:
#             return False, "A userrole nem található!"
#         return True, UserroleResponseSchema().dump(userrole)

#     @staticmethod
#     def userrole_add(request):
#         try:
#             userrole = UserRole(**request)
#             db.session.add(userrole)
#             db.session.commit()

#         except Exception as ex:
#             return False, "userrole_add() hiba!"
#         return True, UserroleResponseSchema().dump(userrole)

#     @staticmethod
#     def userrole_update(id, request):
#         try:
#             userrole = db.session.get(UserRole, id)
#             if userrole:
#                 userrole.role_id = request["role_id"]
#                 db.session.commit()

#         except Exception as ex:
#             return False, "userrole_update() hiba!"
#         return True, UserroleResponseSchema().dump(userrole)

#     @staticmethod
#     def userrole_delete(id):
#         try:
#             userrole = db.session.get(UserRole, id)
#             if not userrole:
#                 return False, "Userrole nem található!"
#             elif userrole:
#                 userrole.deleted = 1
#                 db.session.commit()
#                 return True, "Az adott userrole törölve."

#         except Exception as ex:
#             return False, "userrole_delete() hiba!"
#         return True, "OK"

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
        return True, UserroleResponseSchema().dump(userrole)


    @staticmethod
    def userrole_update(id, request):
        try:
            userrole = db.session.get(UserRole, id)
            if userrole:
                userrole.role_id = request.get("role_id", userrole.role_id)
                # Ha további mezők frissítése szükséges, itt adhatóak hozzá
                db.session.commit()
            else:
                return False, "A userrole nem található!"
        except Exception as ex:
            return False, "userrole_update() hiba!"
        return True, UserroleResponseSchema().dump(userrole)

    @staticmethod
    def userrole_delete(id):
        try:
            userrole = db.session.get(UserRole, id)
            if not userrole:
                return False, "Userrole nem található!"
            userrole.deleted = 1
            db.session.commit()
            return True, "Az adott userrole törölve."
        except Exception as ex:
            return False, "userrole_delete() hiba!"
