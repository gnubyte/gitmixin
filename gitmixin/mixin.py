# std
import sys

# Frameworks
from sqlalchemy import Column, ForeignKey, Integer, String, event, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
from sqlalchemy.orm import declarative_mixin, relationship, sessionmaker
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.schema import Table
import semver

# Custom Imports
from . import gitHandler



def is_modified( objInstance, fieldname):
        trackedfield = getattr(objInstance, fieldname, None)
        if trackedfield == None:
            return False
        history = get_history(objInstance, fieldname)
        print(history)
        if len(history.added) > 0:
            return True
        if len(history.deleted) > 0:
            return True
        return False

@declarative_mixin
class GitMixin(object):
    '''conducts version tracking per field
        1 DB field == 1 git repo
    '''
            

    def increment_tag(mappedClass, mapper, objInstance):
        # WARNING: called before commit to modify the instances' current tag
        # check if this is new change
        # if new change, opt to increment the version number
        # before we set a new tag *ON THE OBJECT IN PREP FOR CHANGING TAG*
        for trackedField in objInstance.__trackedfields__:
            if (is_modified(objInstance=objInstance, fieldname=trackedField) == True):
                gh = gitHandler(git_repo_name=objInstance.__tablename__+"_"+trackedField+"_"+str(objInstance.id))
                git_commit_tag = getattr(objInstance, trackedField+"_tag")
                current_tag = gh.get_current_git_tag()
                print('current tag inside inc tag: ' + str(current_tag))
                isThisNewRepo = False
                if (str(current_tag) != '1.0.0' and str(current_tag) == '' ):
                    # this is a brand new repo
                    git_commit_tag = '1.0.0'
                    isThisNewRepo = True 
                if (isThisNewRepo == False and git_commit_tag == '1.0.0'):
                    print('fired off')
                    ver = semver.VersionInfo.parse(git_commit_tag)
                    print(ver)
                    ver = ver.bump_major()
                    git_commit_tag = str(ver)
                    print('tag inside increment fire off: %s' % (git_commit_tag))
                print('about to set objInstance with git commit tag...%s' % (git_commit_tag))
                setattr(objInstance, str(trackedField)+"_tag", git_commit_tag )


    def git_track_and_update( mappedClass, mapper, objInstance):
        print('check if fires off twice')
        if (hasattr(objInstance, "id") == False):
            raise Exception("This instance of an SQLAlchemy record does not have an ID and cannot be git tracked until it does.")
        # ---
        # Determine and 
        for trackedField in objInstance.__trackedfields__:
            if (is_modified(objInstance, trackedField) == True):
                value = getattr(objInstance, trackedField, None) # TODO: need a method here to fetch if this field has been modified
                git_commit_msg = getattr(objInstance, trackedField+"_commitmsg")
                git_commit_tag = getattr(objInstance, trackedField+"_tag")
                print('current commit tag on object:' + git_commit_tag)
                gh = gitHandler(git_repo_name=objInstance.__tablename__+"_"+trackedField+"_"+str(objInstance.id))
                current_tag = gh.get_current_git_tag()
                print('current tag on repo:' + str(current_tag))
                #if ((git_commit_tag == None or git_commit_tag == '') and current_tag != '1.0.0' and current_tag == None):
                #    git_commit_tag = '1.0.0'
                gh.pack_string_into_file(filename=trackedField, filecontent=value)
                sha = gh.stage_and_commit_all_changes(commitMsg=git_commit_msg)
                if (str(current_tag) == git_commit_tag):
                    print(current_tag)
                    print(git_commit_tag)
                    # the repo is already reflecting the correct tag
                    pass
                else:
                    # add the newest tag
                    gh.create_tag(git_commit_tag)


    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        event.listen(cls, 'before_insert', cls.increment_tag) # CREATE # WARNING: has to run before commit to modify the tag data
        event.listen(cls, 'after_insert', cls.git_track_and_update) # CREATE
        event.listen(cls, 'before_update', cls.increment_tag) # UPDATE/DELETE
        event.listen(cls, 'after_update', cls.git_track_and_update) # UPDATE/DELETE
        event.listen(cls, 'before_delete', cls.increment_tag) # DELETE
        event.listen(cls, 'after_delete', cls.git_track_and_update) # DELETE
        
    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):

        extrafields = []
        allArgs = []
        for item in arg:
            allArgs.append(item)
        if (hasattr(cls, "__trackedfields__")):
            trackedFields = cls.__trackedfields__
                #Column(field+"_commit_hash",String(60), nullable=True)
            for field in trackedFields:
                allArgs.append(Column(field+"_commitmsg",String(250), nullable=True))
                allArgs.append(Column(field+"_tag",String(60), nullable=True))
                allArgs.append(Column(field+"_commit_hash",String(60), nullable=True))
                setattr(cls, field+"_commitmsg" ,Column(field+"_commitmsg",String(250), nullable=True))
                setattr(cls, field+"_tag" ,Column(field+"_tag",String(60), nullable=True))
                setattr(cls, field+"_commit_hash" , Column(field+"_commit_hash",String(60), nullable=True))

        fields = []
        for iterable in arg:
            fields.append(iterable.name)
        if 'id' not in fields:
            raise Exception('To use GitMixin with a table, there must be a field in the versioned table with label `id` ')

        allArgs = tuple(allArgs)
        return Table(
            name,
            metadata, *allArgs, **kw
        )
 

# for testing purposes
if __name__ == "__main__":
    import time
    import os
    if (os.path.exists('sqlalchemy_example.db')):
        os.remove('sqlalchemy_example.db')
    if (os.path.exists('version_control')):
        import shutil
        shutil.rmtree('version_control')
    Base = declarative_base()
    class Person(Base, GitMixin):
        __tablename__ = 'person'
        __trackedfields__ = ['name', 'lastname']
        # Here we define columns for the table person
        # Notice that each column is also a normal Python instance attribute.
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        lastname = Column(String(250))
        email = Column(String(250))

        # {TABLENAME}-{FIELDNAME}-{ID}/ - filehere
        #  Person-lastname-1                          / - 
        #  Person-lastname-2                          / - 
        #  Person-lastname-3                          / - 
        #  Person-lastname-10                          / - 
        #  Person-email-1                          / - 
        #  Person-name-3                          / - 

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

    newPerson = Person(name='test1234', name_commitmsg="latest greatest")
    session.add(newPerson)
    session.commit()
    session.refresh(newPerson)
    print('new persons commit ')
    print(newPerson.name_commitmsg)
    print(newPerson.name_tag)
    print(newPerson.name_commit_hash)
    print('adding email')
    newPerson.email = "patrick.hastings@verizon.com"
    session.commit()
    print('added email')
    print('changing name...')
    newPerson.name = 'updateFieldTest'
    session.commit()
    print('changed name...')
    #session.close()
    print('removing database in 100s')
    time.sleep(100) # give myself 35s to poke around at the db
    print('removing database in 10s')
    time.sleep(10)
    os.remove('sqlalchemy_example.db')