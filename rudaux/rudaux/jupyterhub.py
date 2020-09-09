#import git
from dictauth.users import _load_dict, add_user, remove_user
from collections import namedtuple
from subprocess import check_call, check_output, STDOUT, CalledProcessError
import os

class SnapshotExistsError(Exception):
    def __init__(self, path):
        self.path = path

class JupyterHub(object):
    """
    Interface to a local Jupyterhub with NbGrader assignments
    """

    def __init__(self, course):
        self.jupyterhub_config_dir = course.config.jupyterhub_config_dir
        self.jupyterhub_user_folder_root = course.config.jupyterhub_user_folder_root
        self.assignment_folder_root = course.config.assignment_folder_root
        self.dry_run = course.dry_run

    def snapshot_all(self, snap_name):
        cmd_list = ['zfs', 'snapshot', '-r', self.jupyterhub_user_folder_root.strip('/') + '@'+snap_name]
        if not self.dry_run:
            check_output(cmd_list)
        else:
            print('[Dry run: would have called: ' + ' '.join(cmd_list) + ']')

    def snapshot_user(self, user, snap_name):
        cmd_list = ['zfs', 'snapshot', os.path.join(self.jupyterhub_user_folder_root, user).strip('/') + '@'+snap_name]
        if not self.dry_run:
            check_output(cmd_list)
        else:
            print('[Dry run: would have called: ' + ' '.join(cmd_list) + ']')

    def list_snapshots(self):
        out = check_output(['zfs', 'list', '-t', 'snapshot'], stderr = STDOUT)

    def create_grader_folder(self, grader_name):
        #make sure there isn't already a folder in /tank/home with this name; never overwrite a grader account
        epwrds = _load_dict(self.jupyterhub_config_dir)
        CreateArgs = namedtuple('CreateArgs', 'username salt digest directory')
        args = 'TODO' #CreateArgs(username = ,)
        add_user(args)


        username = 'TODO'
        callysto_user = 'jupyter'
        course = 'dsci100'
        check_call([os.path.join(self.jupyterhub_config_dir, 'zfs_homedir.sh'), course, username, callysto_user])
        pass
    
    def assign_grader(self, assignment_name, ta_username):
        #just add authentication using dictauth
        pass

    def unassign_grader(self, assignment_name):
        #just remove the authentication for the account using dictauth; don't touch the folder
        #to be called when grading is done
        pass

    def stop(self):
        check_call(['systemctl', 'stop', 'jupyterhub'])
 
    def start(self):
        check_call(['systemctl', 'start', 'jupyterhub'])

    

        #======================================================#
        #    Ensure course_dir is a clean git repo and pull    #
        #======================================================#
        
        #print('Ensuring course directory is a clean git repo')
        #
        #try:
        #    repo = git.Repo(course_dir)
        #except git.exc.InvalidGitRepositoryError as e:
        #    sys.exit(f"There was an error creating a git repo object from {course_dir}.")

        ## Before we do anything, make sure our working directory is clean with no untracked files.
        #if repo.is_dirty() or repo.untracked_files:
        #  continue_with_dirty = input(
        #    """
        #    Your repository is currently in a dirty state (modifications or
        #    untracked changes are present). We strongly suggest that you resolve
        #    these before proceeding. Continue? [y/n]:"""
        #  )
        #  # if they didn't say yes, exit
        #  if continue_with_dirty.lower() != 'y':
        #    sys.exit("Exiting...")


        #print(ttbl.AsciiTable([['Pulling course repository']]).table)

        #try:
        #    repo.git.pull('origin', 'master')
        #except git.exc.GitCommandError as e:
        #    sys.exit(f"There was an error pulling the git repo from {course_dir}.")
