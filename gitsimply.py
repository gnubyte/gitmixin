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
        if len(commitMsg) > 120:
            raise Exception('commit message must be 120 characters or less')
        self.git_repo.index.commit(commitMsg)
        return self.git_repo.head.object.hexsha

    def create_tag(self, tagname:str) -> None:
        self.git_repo.create_tag(tagname)
    
    def reset_head(self):
        self.git_repo.reset('--hard')

    def stage_and_commit_all_changes(self, commitMsg:str) -> None:
        changedFiles = self.check_for_untracked_changes()
        self.stage_new_changes(files=changedFiles)
        self.commit_new_changes(commitMsg)




if __name__ == "__main__":
    repo = Repo.init('./test')
    print(repo.untracked_files)
    gh = gitHandler(git_repo_name="testdb-table-field-1")
    changes = gh.check_for_untracked_changes()
    print(changes)
    gitCommitHash = gh.stage_and_commit_all_changes('testing version control')
    print(gitCommitHash)