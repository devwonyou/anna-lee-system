from pydantic import BaseModel
from sqlmodel import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder

from scraper.models import (
	PKModel, 
	CreatorLink, CreatorLinkCreate, CreatorLinkUpdate,
	Creator, CreatorCreate, CreatorUpdate
) 

ModelType = TypeVar("ModelType", bound=PKModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	def __init__(self, model: Type[ModelType]):
		"""
		CRUD object with default methods to Create, Read, Update, Delete (CRUD).

		**Parameters**

		* `model`: A SQLAlchemy model class
		* `schema`: A Pydantic model (schema) class
		"""
		self.model = model

	def get(self, db: Session, id: Any) -> Optional[ModelType]:
		query = db.query(self.model).filter(self.model.id == id).first()
		return query

	def get_multi(
		self, db: Session, *, skip: int = 0, limit: int = 100
	) -> List[ModelType]:
		return db.query(self.model).offset(skip).limit(limit).all()

	def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
		obj_in_data = jsonable_encoder(obj_in)
		db_obj = self.model(**obj_in_data)  # type: ignore
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def update(
		self,
		db: Session,
		*,
		db_obj: ModelType,
		obj_in: Union[UpdateSchemaType, Dict[str, Any]]
	) -> ModelType:
		obj_data = jsonable_encoder(db_obj)
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		# NOTE (awaiting developer updates): exclude_unset does not work in SQLModels but does work in Pydantic Models
		# https://github.com/tiangolo/sqlmodel/issues/87
		update_data = {k: v for k, v in update_data.items() if v is not None}
		for field in obj_data:
			if field in update_data: 
				setattr(db_obj, field, update_data[field])
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def remove(self, db: Session, *, id: int) -> ModelType:
		obj = db.query(self.model).get(id)
		db.delete(obj)
		db.commit()
		return obj

class CRUDCreatorLink(CRUDBase[CreatorLink, CreatorLinkCreate, CreatorLinkUpdate]):
	def get(
		self, 
		db: Session, 
		follower_id: int,
		followed_id: int
	) -> Optional[CreatorLink]:
		query = ( 
			db.query(CreatorLink)
			.filter(
				CreatorLink.follower_id == follower_id,
				CreatorLink.followed_id == followed_id
				)
			.first()
		)
		return query

class CRUDCreator(CRUDBase[Creator, CreatorCreate, CreatorUpdate]):
	def get_by_username(self, db: Session, username: str) -> Optional[Creator]:
		return db.query(Creator).filter(Creator.username == username).first()
		

creator_link = CRUDCreatorLink(CreatorLink)
creator = CRUDCreator(Creator)