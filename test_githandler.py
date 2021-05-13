#############
# Git wrapper handler
#############

# Unit test overhead
import unittest
import time
from gitmixin import gitHandler

# directory manipulation imports
import os
import shutil

class gitsimplyTest(unittest.TestCase):
    '''Tests Git Simply'''
    SLOW_TEST_THRESHOLD = 0.3

    def setupInitialRepo(self):
        # ------ Version Control
        self.versionControlDirectory = 'version_control'
        if (os.path.exists('version_control') == True):
            shutil.rmtree('version_control')
        self.focused_repo = gitHandler(git_repo_name="testdb-table-field-1")


    def setUp(self):
        '''Hooks to unit test setup'''
        self.focused_repo = None
        self.setupInitialRepo()
        self._started_at = time.time()
    
    def __teardownTestDirectories(self):
        gitRepoPath =self.focused_repo.git_repo_path
        versionControlDirectory =self.focused_repo.version_control_directory
        # ------ Version Control
        if (os.path.exists(versionControlDirectory) == True):
            shutil.rmtree('version_control')


    def tearDown(self):
        '''
        Hooks to unit test to get the module and time for each function
        '''
        self.__teardownTestDirectories()
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 2)))
        # SLOW_TEST_THRESHOLD = 0.3
        # Commented out only print slow test threshold
        #if elapsed > SLOW_TEST_THRESHOLD:
            #print('{} ({}s)'.format(self.id(), round(elapsed, 2)))   

    
    def test_write_to_file_inside_repo(self):
        results = self.focused_repo.pack_string_into_file(filename='fieldname.txt', filecontent='#initial file contents\n#some arbitrary string')
        self.assertEqual(results[0], True) # tuple[0] in results is "isNewFile", should be true
        self.assertEqual(results[1], False) # tuple[1] in results is "isModified", should be false since its a new file (NOT UPDATED)

    def test_stage_and_commit(self):
        results = self.focused_repo.pack_string_into_file(filename='fieldname.txt', filecontent='#initial file contents\n#some arbitrary string')
        self.assertEqual(results[0], True) # tuple[0] in results is "isNewFile", should be true
        self.assertEqual(results[1], False) # tuple[1] in results is "isModified", should be false since its a new file (NOT UPDATED)
        self.focused_repo.stage_and_commit_all_changes('test version control')

    def test_create_tag(self):
        results = self.focused_repo.pack_string_into_file(filename='fieldname.txt', filecontent='#initial file contents\n#some arbitrary string')
        self.assertEqual(results[0], True) # tuple[0] in results is "isNewFile", should be true
        self.assertEqual(results[1], False) # tuple[1] in results is "isModified", should be false since its a new file (NOT UPDATED)
        self.focused_repo.stage_and_commit_all_changes('test version control')
        self.focused_repo.create_tag('1.0.0')
        currtag = self.focused_repo.get_current_git_tag()
        self.assertEqual('1.0.0', currtag)


    def test_get_all_tags(self):
        filenameForTesting='fieldname.txt'
        results = self.focused_repo.pack_string_into_file(filename=filenameForTesting, filecontent='#initial file contents\n#some arbitrary string')
        self.focused_repo.stage_and_commit_all_changes('test version control')
        self.focused_repo.create_tag('1.0.0')
        currtag = self.focused_repo.get_current_git_tag()
        results = self.focused_repo.pack_string_into_file(filename=filenameForTesting, filecontent='even newer changes, version 2~!!!!')
        self.focused_repo.stage_and_commit_all_changes('version control tag 2')
        self.focused_repo.create_tag('2.0.0')
        commits = self.focused_repo.return_all_tags_and_commits()
        print(commits)
        #for tag, commit in commits.items():
        #    print(tag)
        #    print(commit.get("author"))
        #    print(commit.get("committed_datetime"))
        #    print(commit.get("author_tz_offset_committed_datetime"))
        #    print(commit.get("message"))
        #    print(commit.get("size"))
        self.assertEqual('test version control', commits.get('1.0.0').get('message'))
        self.assertEqual('version control tag 2', commits.get('2.0.0').get('message'))
        filecontents = self.focused_repo.retrieve_file_contents_by_commit(filename=filenameForTesting, hexsha=commits.get('1.0.0').get('hexsha'))
        print(filecontents)
        #time.sleep(300)




if __name__ == '__main__':
    unittest.main()