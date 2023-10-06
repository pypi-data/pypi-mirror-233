from models import Role, Role

from database import Database


def create_role_initial(db: Database):
	for role_name in Role:
		is_role_exist = db.query(Role).filter_by(name=role_name.value).first() is not None
		if not is_role_exist:
			role = Role(name=role_name.value)
			db.add(role)
			db.commit()
