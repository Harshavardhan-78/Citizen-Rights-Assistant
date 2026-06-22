from pydantic import BaseModel,Field
from typing import List
class LegalResponse(BaseModel):
    answer:str=Field(description="egal explanation for the user query")
    relevant_law: str = Field(description="Law or section relevant to the query")

    source: str = Field(description="Source document name")

    possible_actions: List[str] = Field(description="Possible actions the citizen can take")