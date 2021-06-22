# Getting started with GitMixin

A quick guide to using gitmixin

## Installation

First install gitmixin with pip

`pip install gitmixin`

or 

`pip3 install gitmixin`

***

## Adding Gitmixin to your project

SQLALchemy projects typically have a database defined in models. In your models.py file or equivalent, import GitMixin near the top of the file.

`from gitmixin import GitMixin`


Then, in your SQLAlchemy class, inherit the GitMixin we just imported to give that model SQLAlchemy methods & allow it to access that models' event hooks.

`class Notes(Base, GitMixin):`


Finally in the model, add a new private attrbiute trackedfields, and let it equal a list of strings that you intend to track. The strings inside this list should be names of fields you want to track.

```
class Notes(Base, GitMixin):
    __tablename__ = 'notes'
    __trackedfields__ = ['notes', 'links']
    id = Column(Integer, primary_key=True)
    notes =  Column(String(200))
    links = Column(String(200))
```





### A finished example



```
# imports
from gitmixin import GitMixin

# SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# ...

Base = declarative_base()


class Notes(Base, GitMixin):
    __tablename__ = 'notes'
    __trackedfields__ = ['notes', 'links']
    id = Column(Integer, primary_key=True)
    notes =  Column(String(200))
    links = Column(String(200))



```