from pydantic import BaseModel, Field

class GuardResponse(BaseModel):
    safe: bool = Field(

        description="Whether the prompt is safe."
        
    )
    category:str= Field(
        description="Category of the field"
    )
    reason: str=Field(
        description="Explanation"
    )
