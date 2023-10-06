from typing import Union, List

from database import Database, db_helper
from fastapi import Depends, HTTPException
from models import User, RoleNameEnum

from .service import auth_service
from .exception import PermissionException


class RolePermissions:
	def __init__(self, roles: List[RoleNameEnum]):
		self.roles = roles

	def get_permissions(self,
        db: Database = Depends(db_helper.session_dependency),
        token: str = Depends(auth_service.oauth2_scheme)
	) -> Union[bool, PermissionException]:
		try:
			current_user: User = auth_service.get_user_by_token(db, token)
			for role in self.roles:
				for user_role in current_user.roles:
					if role.value == user_role.name:
						return True
			else:
				raise PermissionException(message=f'Permission denied', role=self.roles)
		except PermissionException as err:
			raise HTTPException(status_code=404, detail=str(err))

		except Exception as err:
			raise HTTPException(status_code=404, detail="Permission denied")


