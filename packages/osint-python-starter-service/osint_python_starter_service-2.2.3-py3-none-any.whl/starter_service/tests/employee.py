import json
from typing import Optional

from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    age: int
    from_: int
    to_: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {
            k[:-1] if k.endswith("_") else k: v for k, v in self.__dict__.items()
        }

    def json(self, *args, **kwargs):
        return json.dumps(self.dict(), *args, **kwargs)


main_class = Employee

if __name__ == '__main__':
    e = Employee(name="John", age=42, from_=1, to_=2)
    print(e.json())
    print(e.dict())
