from pydantic import BaseModel, EmailStr, HttpUrl




class UserSchema(BaseModel):
    first_name: str
    last_name: str
    username:str
    email: EmailStr
    address: str
    profile_pic: HttpUrl 
    

    class Config:
        from_attributes = True


class CreateUser(UserSchema):
    password: str

 

    