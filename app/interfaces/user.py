from pydantic import BaseModel
from datetime import datetime
import bcrypt


class User(BaseModel):
    email: str
    password: str
    name: str

    def to_model(self):
        return {
            'email': self.email,
            'password': bcrypt.hashpw(
                password=bytes(self.password, 'utf-8'),
                salt=bcrypt.gensalt(),
            ),
            'name': self.name,
            'date': datetime.utcnow(),
        }


class UserUpdate(BaseModel):
    method: str
    data: str
