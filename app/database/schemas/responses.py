from pydantic import BaseModel
from typing import List

class SuccessResponse(BaseModel):
	message: str

class ErrorResponse(BaseModel):
	errors: List[str]