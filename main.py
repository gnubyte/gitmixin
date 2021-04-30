import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, event, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
from sqlalchemy.orm import declarative_mixin, relationship, sessionmaker
from sqlalchemy.schema import Table

# Custom Imports
from gitsimply import gitHandler

Base = declarative_base()



#class BaseMeta(DeclarativeMeta):
#    def __init__(cls, classname, bases, dict_):
#        # add your changes/additions to classes before it go to SQLAlchemy parser
#        # you can make this way multiple table generations from one class, if needed and etc
#        #endings = {'y': lambda x: x[:-1] + "ies", 's': lambda x: x + 'es'}
#        #base_name = cls.__name__.lower()
#        #cls.__tablename__ = endings.get(base_name[-1], lambda x: x + 's')(base_name)
#        #print(dir(cls))
#        #print(dir(classname))
#        #print(classname)
#        #print(bases)
#        #print(dict_)
#        #print(dir(dict_))
#        if (hasattr(cls, "__trackedfields__")):
#            trackedFields = cls.__trackedfields__
#            for field in trackedFields:
#                setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
#                setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
#                setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
#        DeclarativeMeta.__init__(cls, classname, bases, dict_)



# need to be able to read from a directory then repopulate DB from git
@declarative_mixin
class GitMixin(object):
    '''conducts version tracking per field
        1 DB field == 1 git repo
    '''
    # I seem to come back to this often...
    #print(dir(object))
    #print(object)

    #@property
    #def parents123(self):
    #    """
    #        Returns an entity's parent and all parents of parents as a list,
    #        ordered by oldest parent first
    #    """
    #    parents = []
    #    if hasattr(self, "parent"):
    #        if hasattr(self.parent, "parent"):
    #            parents.extend(self.parent.parents)
    #
    #        parents.append(self.parent)
    #
    #    return parents

    #def __new__(cls, *args, **kwargs):
    #    print ("Creating Instance")
    #    print(dir(cls))
    #    if (hasattr(cls, "__trackedfields__")):
    #        trackedFields = cls.__trackedfields__
    #        for field in trackedFields:
    #            #Column(field+"_commit_hash",String(60), nullable=True)
    #            setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
    #            setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
    #            setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
    #    #instance = super(GitMixin, cls).__new__(cls, *args, **kwargs)
    #    #if for trackedfield in cls.__trackedfields__
    #    return object.__new__(cls)

    #def __new__(cls):
    #    print("Creating instance")
    #    #return super(GitMixin, cls).__new__(cls)
    #    return super(GitMixin).__new__(cls)

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
    # this was close but a mess
    #def __new__(cls, *args, **kwargs):
    #    #print(dir(cls))
    #    print(cls.__trackedfields__)
    #    #trackedfields = cls.__trackedfields__
    #    if (hasattr(cls, "__trackedfields__")):
    #        trackedFields = cls.__trackedfields__
    #        for field in trackedFields:
    #            #Column(field+"_commit_hash",String(60), nullable=True)
    #            #setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
    #            setattr(GitMixin, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
    #            #setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
    #            setattr(GitMixin, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
    #            #setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
    #            setattr(GitMixin, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
    #    return super(GitMixin, cls).__new__(cls)

    #def __new__(cls, *args, **kwargs):
    #    for i in cls.__subclasses__():
    #        print(i)
    #        return super().__new__(i)
    #    return super().__new__(GitMixin)

    def git_track_and_update( mappedClass, mapper, objInstance):
        if (hasattr(objInstance, "id") == False):
            raise Exception("This instance of an SQLAlchemy record does not have an ID and cannot be git tracked until it does.")
        #for trackedField in objInstance.__trackedfields__:
        #    gh = gitHandler(git_repo_name=objInstance.__tablename__+"_"+trackedField+"_"+objInstance.id)
        #    gh.pack_string_into_file(filename=trackedField, filecontent=objInstance[trackedField])
        #    gh.stage_and_commit_all_changes(commitMsg="Test commit msg")
        #print(dir(objInstance))
        #print(objInstance.name)
        #print(objInstance.id)
        print('post commit ')
        #print(objInstance.__tablename__)
        #print(objInstance.__trackedfields__)

    def test():
        print('before attach test')

    @classmethod
    def __declare_first__(cls):
        print('declare first')
        #print(cls)
        #print(dir(cls))
        #print(type(cls.parents123))
        #print(cls.parents123)
        #print(dir(cls.parents123))
        #cls.__table__.create(cls, checkfirst=True)
        #if (hasattr(cls, "__trackedfields__")):
        #    trackedFields = cls.__trackedfields__
        #    for field in trackedFields:
        #        #Column(field+"_commit_hash",String(60), nullable=True)
        #        setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
        #        setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
        #        setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
        #print('declare first')
        #print(cls)
        #print(dir(cls))


    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        event.listen(cls, 'after_insert', cls.git_track_and_update) # Initial git commit
        #event.listen(cls, 'before_attach', cls.test) # Initial git commit
        
    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        # Need to check here if we have a primary_key ID field, if not, raise an error
        #extrafields = []
        #allArgs = []
        #for item in arg:
        #    allArgs.append(item)
        #if (hasattr(cls, "__trackedfields__")):
        #    trackedFields = cls.__trackedfields__
        #        #Column(field+"_commit_hash",String(60), nullable=True)
        #    for field in trackedFields:
        #        allArgs.append(Column(field+"_commitmsg",String(250), nullable=True))
        #        allArgs.append(Column(field+"_tag",String(60), nullable=True))
        #        allArgs.append(Column(field+"_commit_hash",String(60), nullable=True))
        #        setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
        #        setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
        #        setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))
        #
        #else:
        #    raise Exception('you must specify the fields you would like to track by adding __trackedfields__=["field1"] to your model')
        fields = []
        for iterable in arg:
            fields.append(iterable.name)
        if 'id' not in fields:
            raise Exception('To use GitMixin with a table, there must be a field in the versioned table with label `id` ')
        #allArgs = tuple(allArgs)
        #print(allArgs)
        #print(arg)
        #print(type(arg))
        return Table(
            name,
            metadata, *arg, **kw
        )
 
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