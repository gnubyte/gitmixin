# Getting Started

A quick guide to using gitmixin

## Installation

First install gitmixin with pip

`pip install gitmixin`

or 

`pip3 install gitmixin`

***


## What does GitMixin do?

Gitmixin, once enabled, per field in the database will track changes to a text field automatically. For example if you have a string field, and you make an update or a new write to a row in the database, per record for that database table, the changes will be tracked, and the version number will increment. 

For example, lets say we have table 'blog posts' for a database model that looks roughly like so in the database:

```
BLOGPOSTS:
 - id :int
 - post: str

```


Now we add Gitmixin and track the post field:

```
BLOGPOSTS:
 - id: int
 - posts: str
 - posts_commitmsg: str
 - posts_tag: str
 - posts_commit_hash: str
```


We can see three new fields were added to this database model dynamically with the prefix of the field name and a suffix of commitmsg, tag, and commit_hash. These will be used to fetch the current commit message, the current commit hash, and finally the current commit tag, starting at tag 1.0. This means we are at the first version of this database record.

Lets say we add a record:

```
post='I went to the beach this summer'
commitmsg='initial commit'

```

Our tag would become version `1.0` as the first version of this post, and our commit message would save to that tag + commit hash. After the record is written to the database, the commit hash would be autopopulated and be representative to tag `1.0`.



Now lets update that same database table record:

```
post='I went to a beach in Hawaii this summer and it was great!'
commitmsg='specified what beach in blogpost'
```

Our tag would automatically become `2.0` for this post, and the commit message field would contain the new message. The previous git commit message for `1.0` would be contained in git on disc.



## Must have Requirements

It stands to reason the system must have these requirements to use this library as of GitMixin v0.1.0:
 - python 3.x and up
 - Git installed on the OS or environment
 - **WARNING:** the field you are tracking at this time must be a string
 - **WARNING:** the model you have must have a field linearly called 'id' at this time (gitmixin 0.1.0)




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