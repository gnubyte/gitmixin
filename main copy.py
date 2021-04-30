import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, event, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import declarative_mixin, relationship, sessionmaker
from sqlalchemy.schema import Table

# Custom Imports
#from gitsimply import gitHandler

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

    def test_print():
        print('test of after commit event')

    @staticmethod
    def create_time(mapper, connection, target):
        #target.created = time()
        print('123abc')

    @classmethod
    def register(cls):
        event.listen(cls, 'after_commit', cls.create_time)

    @classmethod
    def after_commit(cls, session):
        # this works
        event.listen(cls, 'after_commit', cls.test_print)
        f = open("demofile2.txt", "a")
        f.write("Now the file has more content!")
        f.close()

    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        event.listen(cls, 'before_insert', cls.create_time)

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        # REPL to see what is available to us
        print('cls')
        print(dir(cls));
        print('name')
        print(name)
        print('metadata')
        print(dir(metadata))
        print('args')
        print(arg)
        print('kwargs')
        for key, word, in kw.items():
            print(key)
            print(word)
        return Table(
            name,
            metadata, *arg, **kw
        )
        '''        
        cls
        ['__abstract__', '__class__', '__declare_last__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table_cls__', '__tablename__', '__trackedfields__', '__weakref__', '_sa_class_manager', '_sa_registry', 'after_commit', 'create_time', 'git_change_version', 'git_commit', 'git_stage', 'id', 'metadata', 'name', 'register', 'registry', 'test_print']
        -------
        name
        person
        -------
        metadata
        ['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__visit_name__', '__weakref__', '_add_table', '_bind', '_bind_to', '_compiler_dispatch', '_fk_memos', '_init_items', '_original_compiler_dispatch', '_remove_table', '_schema_item_copy', '_schemas', '_sequences', '_set_parent', '_set_parent_with_dispatch', '_use_schema_map', 'bind', 'clear', 'create_all', 'create_drop_stringify_dialect', 'dispatch', 'drop_all', 'info', 'is_bound', 'naming_convention', 'reflect', 'remove', 'schema', 'sorted_tables', 'tables']
        -------
        args
        (Column('id', Integer(), table=None, primary_key=True, nullable=False), Column('name', String(length=250), table=None, nullable=False))
        -------
        kwargs
        123abc
        -------
        '''


 
 
 
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