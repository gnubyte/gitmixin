#==========
# EXTRA COPY 4-27-2021 with R&D
# =========

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, event, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import declarative_mixin, relationship, sessionmaker
from sqlalchemy.schema import Table

# Custom Imports
from gitsimply import gitHandler

Base = declarative_base()


# need to be able to read from a directory then repopulate DB from git
@declarative_mixin
class GitMixin(object):

    def git_stage():
        raise NotImplementedError()
 
    def git_commit():
        raise NotImplementedError()
 
    def git_change_version():
        raise NotImplementedError()

    def git_track_and_update( mappedClass, mapper, objInstance):
        print('test of after commit event')
        #print(dir(args))
        print(mappedClass)
        print(dir(mappedClass)) # SQLAlchemy table instance mapping
        print(mapper)
        print('-------\n')
        #objInstance.refresh()
        print(dir(objInstance))
        print(objInstance.name)
        print(objInstance.id)
        print(objInstance.__tablename__)
        print(objInstance.__trackedfields__)

    def init_git_repo():
        # dump latest part of the field to disk
        # initialize the git repo
        pass

    @classmethod
    def after_commit(cls, session):
        # this works
        print(dir(cls))
        print(dir(session))
        session.refresh()
        event.listen(cls, 'after_commit', cls.git_track_and_update)
        f = open("demofile2.txt", "a")
        f.write("Now the file has more content!")
        f.close()

    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        event.listen(cls, 'after_insert', cls.git_track_and_update) # Initial git commit
        #event.listen(cls, 'after_commit', cls.test_print)
        
    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        # Need to check here if we have a primary_key ID field, if not, raise an error
        fields = []
        for iterable in arg:
            fields.append(iterable.name)
        if 'id' not in fields:
            raise Exception('To use GitMixin with a table, there must be a field in the versioned table with label `id` ')
        return Table(
            name,
            metadata, *arg, **kw
        )
 
 
class Person(Base, GitMixin):
    __tablename__ = 'person'
    __trackedfields__ = ['name']
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
db = engine 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)






Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#engine.event.listen(session, 'after_commit', GitMixin.after_commit)
#event.listen(Session, "after_commit", GitMixin.after_commit) #TODO: let the mixin own this
#event.listen(Session, "after_commit", GitMixin.after_commit)

newPerson = Person(name='test1234')
session.add(newPerson)
session.commit()