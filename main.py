import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, event, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
from sqlalchemy.orm import declarative_mixin, relationship, sessionmaker
from sqlalchemy.schema import Table

# Custom Imports
from gitsimply import gitHandler





@declarative_mixin
class GitMixin(object):
    '''conducts version tracking per field
        1 DB field == 1 git repo
    '''
    
    @declared_attr
    def git_commit_msg(cls):
        if (hasattr(cls, "__trackedfields__")):
            print('test')
            trackedFields = cls.__trackedfields__
            allCreatedFields = []
            for field in trackedFields:
                allCreatedFields.append(Column(field+"_commitmsg",String(250), nullable=True))
                allCreatedFields.append(Column(field+"_tag",String(60), nullable=True))
                allCreatedFields.append(Column(field+"_commit_hash",String(60), nullable=True))
            return allCreatedFields


    def git_track_and_update( mappedClass, mapper, objInstance):
        if (hasattr(objInstance, "id") == False):
            raise Exception("This instance of an SQLAlchemy record does not have an ID and cannot be git tracked until it does.")
        for trackedField in objInstance.__trackedfields__:
            gh = gitHandler(git_repo_name=objInstance.__tablename__+"_"+trackedField+"_"+objInstance.id)
            gh.pack_string_into_file(filename=trackedField, filecontent=objInstance[trackedField])
            gh.stage_and_commit_all_changes(commitMsg="Test commit msg")


    @classmethod
    def __declare_first__(cls):
        #print('declare first')
        pass


    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        event.listen(cls, 'after_insert', cls.git_track_and_update) # Initial git commit
        
    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        fields = []
        for iterable in arg:
            fields.append(iterable.name)
        if 'id' not in fields:
            raise Exception('To use GitMixin with a table, there must be a field in the versioned table with label `id` ')
        return Table(
            name,
            metadata, *arg, **kw
        )
 

# for testing purposes
if __name__ == "__main__":
    Base = declarative_base()
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