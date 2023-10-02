from sqlalchemy import Column, ForeignKey, Integer, String

from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Groups(BaseTable):
    __tablename__ = "profile_groups"

    title = Column(String)


@mapper_registry.mapped
class Role(BaseTable):
    __tablename__ = "profile_roles"

    title = Column(String)
    permissions = Column(String, ForeignKey("profile_permissions.key"))


@mapper_registry.mapped
class User:
    __tablename__ = "profile_users"

    phone = Column(Integer, index=True, primary_key=True)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    father_name = Column(String)
    fks_id = Column(String)
    gender = Column(String)

    family_id = Column(String)
    group_id = Column(String)
    role_id = Column(String)
    permissions = Column(String)


@mapper_registry.mapped
class Permissions:
    __tablename__ = "profile_permissions"

    key = Column(String, index=True, primary_key=True)


@mapper_registry.mapped
class Families(BaseTable):
    __tablename__ = "profile_families"

    title = Column(String)


@mapper_registry.mapped
class Horses(BaseTable):
    __tablename__ = "profile_horses"

    name = Column(String)
    fks_id = Column(String)
    gender = Column(String)
    breed = Column(String)
    color = Column(String)
    personality = Column(String)
    owner_id = Column(String)
