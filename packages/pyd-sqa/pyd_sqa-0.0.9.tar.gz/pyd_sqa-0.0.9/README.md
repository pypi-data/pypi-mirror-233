# pyd-sqa
Pydantic-SQLAlchemy

<a href="https://github.com/selobu/sqlalchemy-pydantic/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/seloby/sqlalchemy-pydantic/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/selobu/pyd-sqa/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/selobu/sqlalchemy-pydantic/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://codecov.io/gh/selobu/sqlalchemy-pydantic" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/selobu/sqlalchemy-pydantic?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/selobu/pyd-sqa" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyd-sqa?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

Tools to generate Pydantic models from SQLAlchemy models, forked from pydantic-sqlalchemy

Still experimental.

## How to use

Quick example:

```Python
from typing import List

from pyd_sqa import pyd_sqa
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")


PydanticUser = pyd_sqa(User)
PydanticAddress = pyd_sqa(Address)


class PydanticUserWithAddresses(PydanticUser):
    addresses: List[PydanticAddress] = []


Base.metadata.create_all(engine)


LocalSession = sessionmaker(bind=engine)

db: Session = LocalSession()

ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")

address = Address(email_address="ed@example.com")
address2 = Address(email_address="eddy@example.com")
ed_user.addresses = [address, address2]
db.add(ed_user)
db.commit()


def test_pyd_sqa():
    user = db.query(User).first()
    pydantic_user = PydanticUser.from_orm(user)
    data = pydantic_user.dict()
    assert data == {
        "fullname": "Ed Jones",
        "id": 1,
        "name": "ed",
        "nickname": "edsnickname",
    }
    pydantic_user_with_addresses = PydanticUserWithAddresses.from_orm(user)
    data = pydantic_user_with_addresses.dict()
    assert data == {
        "fullname": "Ed Jones",
        "id": 1,
        "name": "ed",
        "nickname": "edsnickname",
        "addresses": [
            {"email_address": "ed@example.com", "id": 1, "user_id": 1},
            {"email_address": "eddy@example.com", "id": 2, "user_id": 1},
        ],
    }
```
