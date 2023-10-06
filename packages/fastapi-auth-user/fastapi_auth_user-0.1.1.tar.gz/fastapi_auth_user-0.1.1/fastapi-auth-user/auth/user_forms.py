import inspect
from fastapi import Form
from pydantic import BaseModel
from typing import Type
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
	new_parameters = []

	for _, model_field in cls.__fields__.items():
		model_field: ModelField

		new_parameters.append(
			inspect.Parameter(
				model_field.alias,
				inspect.Parameter.POSITIONAL_ONLY,
				default=Form(...) if model_field.required else Form(model_field.default),
				annotation=model_field.outer_type_,
			)
		)

	async def as_form_func(**data):
		return cls(**data)

	sig = inspect.signature(as_form_func).replace(parameters=new_parameters)
	as_form_func.__signature__ = sig
	setattr(cls, 'as_form', as_form_func)
	return cls


@as_form
class AuthUserDataForm(BaseModel):
	email: str = Form(...)
	password: str = Form(...)
