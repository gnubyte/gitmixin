# Gitmixin

An SQLALchemy mixin that can track individual fields and turn them into git repos with simple advance forward, rewind back mechanisms.

[![Docs](https://img.shields.io/badge/gitmixin-docs-blue)](https://gitmixin.readthedocs.io/en/latest/?)
[![PyPI Version](https://img.shields.io/badge/gitmixin-PyPI-green)](https://pypi.org/project/gitmixin/)
[![Github](https://img.shields.io/github/forks/gnubyte/gitmixin?style=social)](https://github.com/gnubyte/gitmixin)


## Docs

Documentation on how to use the project as well as development for it can be found here. Check the projects section on Github speciifcally for the roadmap.

[Checkout our read the docs!](https://gitmixin.readthedocs.io/en/latest/?)

## Testing

Run tests: 

`python3 tests/test_githandler.py`


## Getting started with GitMixin

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


Finally in the model, add a new private attribute trackedfields, and let it equal a list of strings that you intend to track. The strings inside this list should be names of fields you want to track.

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