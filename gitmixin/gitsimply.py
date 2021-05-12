from git import Repo
from pathlib import Path
import os



# TODO:
# - have one mirrored repo
# - have a process to auto take updates from that mirror
# - behavior to push or pull from repo
# - check for untracked changes
# - check for branch
# - merge between branches
# - roll back changes
# - correlate git hashes to version numbers



class gitHandler:

    def __init__(self, **kwargs):
        self.git_repo = None
        self.version_control_directory = None # wherever all the git directories are
        self.git_repo_path = None # the actual file path for OS passes
        self.git_repo_name = None # the REPO name "{database}-{table}-{field}-{id}"
        self.mirror_remote = False
        self.mirror_this_remote = None
        if (kwargs):
            self.__dict__.update(**kwargs)
        # Check version control path is full
        if (self.version_control_directory == None):
            self.version_control_directory = str(Path.cwd()) + '/version_control'
            if (self.git_repo_path != None and os.path.exists(self.git_repo_path) == False):
                os.mkdir(self.version_control_directory)
        if (os.path.exists(self.version_control_directory) == False):
            os.mkdir(self.version_control_directory)
        # Create full path to git repo
        if (self.git_repo_path == None):
            self.git_repo_path = self.version_control_directory + '/' + self.git_repo_name
        # Make directory
        if (os.path.exists(self.git_repo_path) == False):
            os.mkdir(self.git_repo_path)
        #self.git_repo = Repo.init(self.git_repo_path)
        if (self.git_repo == None):
            # if there is, or is not an existing repo it doesnt seem to matter 4/21/21
            self.git_repo = Repo.init(self.git_repo_path)

    def check_for_untracked_changes(self) -> list:
        return self.git_repo.untracked_files

    def pack_string_into_file(self, filename: str, filecontent:str)-> tuple:
        '''Will write filecontent to the filename inside the repo    
        with the tuple(isNewFile=Boolean,isModified=Boolean)
        '''
        if filecontent == None:
            filecontent = ''
        #newFile  & modified is redundant but both are present for clear expression of meaning
        filepath = self.git_repo_path + "/"+filename
        if (os.path.exists(filepath) == False):
            isNewFile = True
            isModified = False
        else:
            isNewFile = False
            isModified = True         
        fileHandler = open(filepath, "w")
        fileHandler.write(filecontent)
        fileHandler.close()
        return (isNewFile, isModified)


    def stage_new_changes(self, files: list) -> None:
        self.git_repo.index.add(files)

    def commit_new_changes(self, commitMsg:str ) -> str:
        if commitMsg == None:
            commitMsg = ''
        if len(commitMsg) > 120:
            raise Exception('commit message must be 120 characters or less')
        self.git_repo.index.commit(commitMsg)
        

    def create_tag(self, tagname:str) -> str:
        #print('git repo describe')
        #print(self.git_repo.head)
        #print(self.git_repo.head.log)
        #print(dir(self.git_repo.head))
        #print(dir(self.git_repo))
        #print(self.git_repo.tag(self.git_repo_path))
        print(self.git_repo.tags)
        self.git_repo.create_tag(tagname)
        return self.git_repo.tags[-1]

    def get_current_git_tag(self) -> str:
        '''returns latest git tag'''
        if len(self.git_repo.tags) == 0:
            return ""
        else:
            return str(self.git_repo.tags[-1])
    
    def return_all_tags_and_commits(self) -> dict:
        tagmap = {}
        for t in repo.tags():
            tagmap.setdefault(r.commit(t), []).append(t)
        return tagmap

    def reset_head(self):
        self.git_repo.reset('--hard')

    def stage_and_commit_all_changes(self, commitMsg:str) -> None:
        changedFiles = self.check_for_untracked_changes()
        self.stage_new_changes(files=changedFiles)
        self.commit_new_changes(commitMsg)
        




if __name__ == "__main__":
    import os
    import shutil


    # ----------CLEANUP---------
    # if version control && test directories exist
    # Clean them up for the next demo/test    

    #  ----- Version Control
    if (os.path.exists('version_control') == True):
        shutil.rmtree('version_control')

    #  ----- test directory
    if (os.path.exists('test') == True):
        shutil.rmtree('test')



    # -----------------------------
    # CREATE MOCK FILES
    if (os.path.exists('working_test_demo') == False):
        os.mkdir('test')
        oneFile = open('working_test_demo/onefile.py', 'w')
        oneFile.write('#this is a test comment \nprint("codehere") ')
        oneFile.close()

    # -----------------------------
    #            TEST

    # #------ Init the repo
    repo = Repo.init('./working_test_demo')
    print(repo.untracked_files)
    gh = gitHandler(git_repo_name="testdb-table-field-1")
    changes = gh.check_for_untracked_changes()
    print(changes)


    # #------ Check in the current 'new' files
    # #------ add a tag
    gh.stage_and_commit_all_changes('testing version control')
    gh.create_tag(tagname='1.0.0')

    # #---- Change the files 
