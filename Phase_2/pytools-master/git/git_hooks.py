#!/usr/bin/python
# from git import Repo
import logging
import os
import sh
import time
import subprocess
from sh import ErrorReturnCode

logging.basicConfig(format="(%(process)d)\t%(asctime)s  %(levelname)s\t%(message)s", datefmt='%H:%M:%S', level=logging.WARNING)
logger = logging.getLogger("GitHooks")

git = None

#working_dir = "/home/kirillb/projects/cassandrarep/"
working_dir = "/home/kirillb/cassandrarep"

TMP_GIT_DIR = "/home/kirillb/tmp_gits/"
SHADOW_BRANCH_FOLDER_MAKS = "repo_for_job_{job_id}"

# TODO: how does chacking out deleted file works? will it remove the original?

STAGED_FILES_PATTERN_LIST = ["M ", "D ", "A "]
UNSTAGED_FILES_PATTERN_LIST = [" M", " D", " A"]
UNTRACKED_FILES_PATTERN_LIST = ["??"]

JOBS_BRANCH_PREFIX = "jobs_"

def remove_repeated_spaces(line):
    return " ".join(line.split())

def construct_jobs_branch_name(active_branch):
    return "%s%s"% (JOBS_BRANCH_PREFIX, active_branch)

def is_local_branch_exist(branch_name):
    try:
        git("rev-parse", "--verify", branch_name)
    except ErrorReturnCode:
        return False

    return True

def try_checkout_branch(branch_name):
    try:
        git("checkout", branch_name)
    except ErrorReturnCode:
        return False

    return True

def parseout_filename_from_status_line(line) :
    """
    expected format of the line: " M  ../../readme "
    we need to return only clean file name
    """
    line = line.lstrip() #rm front space for split
    line = remove_repeated_spaces(line)
    fname = line.split(" ")[1].rstrip().lstrip()

    return fname

def get_current_brach_name():

    buf = []

    for line in git("status", _iter=True):
        if "On branch" in line:
            line = remove_repeated_spaces(line)
            return line.split(" ")[2].rstrip()
        buf.append(line)

    for l in buf:
        print l
    raise RuntimeError()

def get_files_from_status(prefix_pattern_list):

    list_of_files = []
    for line in git("status", "-s", _iter=True, _tty_out=False):
        # print "[%s]-[%s]"%(line.rstrip(), prefix_pattern_list)

        for pat in prefix_pattern_list:
            if line.startswith(pat):

                fname = parseout_filename_from_status_line(line)
                list_of_files.append(fname)
                break

    return list_of_files


def checkout_create_rem_branch(branch_name):

    if try_checkout_branch(branch_name):
        pass
    else:
        # try to fetch new remote brances and retry
        git("fetch")
        if try_checkout_branch(branch_name):
            pass

        print "creating a branch %s" % branch_name

        # no branch found create a new one
        git("checkout", "-b", branch_name)
        # push to remote
        git("push", "-u", "origin", branch_name)

def is_merge_brances_has_written(from_branch, to_branch, merge_msg="auto merge"):
    """
    returns True, if merge is successful and it has modified some untracked_files
    return False, if there is nothing to merge
    """

    for line in git("merge", from_branch, to_branch, "-m", merge_msg, _iter=True, _tty_out=False):
        if "Already up-to-date." in line:
            return False

    return True

def get_current_hash():

    for line in git("rev-parse",  "HEAD", _iter=True, _tty_out=False):
        git_hash = line.rstrip()
        assert len(git_hash) == len("d82cd975340153b95d0a81556eb675adea97cd45")
        break
    return git_hash

def has_staged_files():
    staged_files = get_files_from_status(STAGED_FILES_PATTERN_LIST)
    return len(staged_files) > 0

def commit_if_has_staged_files(commit_message):

    staged_files = get_files_from_status(STAGED_FILES_PATTERN_LIST)
    # print staged_files
    if len(staged_files) > 0:
        git("commit", "-m", commit_message)

def dump_log_2file_git_add(log_file_name, log_msg):
    """
    Dumps a log_msg into a text file,
    adds this file to be tracked by git"""

    log_full_path = os.path.join(working_dir, log_file_name)
    write_key = "w"
    if os.path.isfile(log_full_path):
        write_key = "a"

    with open(log_full_path, write_key) as job_log:
        job_log.write(log_msg)

    git("add", log_file_name)

def get_modified_files_branch_diff(branch_name):

    changed_file_list = []
    for line in git("diff", "--name-status", branch_name, _iter=True, _tty_out=False):
        fname = parseout_filename_from_status_line(line)
        changed_file_list.append(fname)

    return changed_file_list

def checkout_files_from_branch(file_list, branch_name):

    for f in file_list:
        logger.debug("git checkout %s %s" % (branch_name, f))
        git("checkout", branch_name, f)

def git_reset_files(file_list):

    for f in file_list:
        logger.debug("git reset %s " % f)
        git("reset", f)

def print_hook_status(msg, status, length=30):
    print "{msg}:{spaces}[{status}]".format(
        msg=msg,
        spaces=" "*(length-len(msg)),
        status=status)

def is_git_sshkey_added() :

    add = sh.Command("ssh-add")

    for line in add("-l", _iter=True):
        if "git" in line:
            return True

    return False

def get_tmp_fldr_name_4shadow_repo(job_id):
    return os.path.join(TMP_GIT_DIR, SHADOW_BRANCH_FOLDER_MAKS.format(job_id=job_id))

def make_tmp_dir(job_id):
    fldr_name = get_tmp_fldr_name_4shadow_repo(job_id)

    sh.rm(fldr_name, "-rf")
    sh.mkdir(fldr_name)

    return fldr_name

def get_repo_top_location(some_repo_subfolder):

    tmp_git = sh.git.bake(_cwd=some_repo_subfolder)
    line = tmp_git("rev-parse", "--show-toplevel")
    return line.rstrip()

def get_repo_rootname_from_remote_url(url):
    """ pasing the string of the form:
    git@bitbucket.org:bitnsg/cassandrarep.git
    to get string: "cassandrarep" """

    return url.split("/")[-1].split(".")[0]



def get_repo_name_from_path(repo_path):

    return repo_path.split("/")[-1]

def get_remote_url():
    return git("config", "--get", "remote.origin.url").rstrip()


def init_tmp_shadow_repo(working_dir, job_id):
    repo_path = get_repo_top_location(working_dir)
    repo_name = get_repo_name_from_path(repo_path)
    logger.debug("%s %s", repo_path, repo_name)

    # Create copy of repo in a tmp folder. This is done not to affect your
    # Text editor, if it is pointing to the working dir right now.

    tmp_fldr = make_tmp_dir(job_id)
    git = sh.git.bake(_cwd=tmp_fldr)

    git("clone", "file:///"+repo_path)

    print_hook_status("Init shadow repo", "OK")
    return os.path.join(tmp_fldr, repo_name)


def copy_unstaged_from_working2shadow(working_repo_path, shadow_repo_path):

    files2copy = get_files_from_status(
        STAGED_FILES_PATTERN_LIST +
        UNSTAGED_FILES_PATTERN_LIST)

    for mod_file in files2copy:
        sh.cp(
            os.path.join(working_repo_path, mod_file),
            os.path.join(shadow_repo_path, mod_file)
        )


    print_hook_status("Copy out modified files", "OK")


# This is test 1
def generate_job_branch_snapshot(working_dir, job_id, commit_msg):
    global git
    print_hook_status("Starting Git Hooks", "OK")

    git = sh.git.bake(_cwd=working_dir)
    working_branch =  get_current_brach_name()
    assert not working_branch.startswith(JOBS_BRANCH_PREFIX), \
        "Starting active branch cannot be a jobs branch starting with %s"% JOBS_BRANCH_PREFIX

    assert is_git_sshkey_added(), \
        "Please add git key to ssh agent, otherwise script will hang on push to remote"

    print_hook_status("Basic checks", "OK")

    working_remote_url = get_remote_url()
    shadow_repo_path = init_tmp_shadow_repo(working_dir, job_id)
    working_repo_path = get_repo_top_location(working_dir)


    git = sh.git.bake(_cwd=working_repo_path)

    copy_unstaged_from_working2shadow(
        working_repo_path=working_repo_path,
        shadow_repo_path=shadow_repo_path)


    git = sh.git.bake(_cwd=shadow_repo_path)

    git("stash")

    ############################################################
    ## <1> Checkout/Create Jobs Branc
    ############################################################
    jobs_branch_name = construct_jobs_branch_name(working_branch)
    checkout_create_rem_branch(jobs_branch_name)
    git("remote", "set-url", "origin", working_remote_url)
    git("pull")
    print_hook_status("Checkout/Create job branch", "OK")


    ############################################################
    ## <2> Merge commits and stash from working into jobs branch
    ############################################################
    git("merge", "-X", "theirs", working_branch, "-m", "%s:[auto merge] %s" % (job_id, commit_msg))
    print_hook_status("Merge working into jobs", "OK")
    git("checkout", "stash", "--",  ".")
    if has_staged_files():
        git("commit", "-m", "%s:[auto stash commit] %s" % (job_id, commit_msg))
    print_hook_status("Merging Stash into jobs", "OK")


    # commit_msg = "\"job_%04d %s\"" % (job_id, commit_msg)
    # dump_log_2file_git_add("job_branch.log", commit_msg+"\n")
    #

    # git("add", "-u") # adding unstaged files if any
    # commit_if_has_staged_files(commit_msg)


    git("push")
    print_hook_status("Push jobs to remove", "OK")
    snapshot_hash = get_current_hash()

    ############################################################
    ## <3> Return back to working branch
    ############################################################

    git("checkout", working_branch)

    mod_files = get_modified_files_branch_diff(jobs_branch_name)
    checkout_files_from_branch(mod_files, jobs_branch_name)
    git_reset_files(mod_files)

    print_hook_status("Git Hooks Done", "OK")

    return snapshot_hash, working_remote_url


def process_output(line):
        print(line)

# def init_git(where):

#     global git
#     if not git:
#         print_hook_status("Starting Git Hooks", "OK")

#         git = sh.git.bake(_cwd=where)

def clone_tag_to(repo, tag, where_to):
    """We checkout a repo to a target directory
    return path to the root of that checked out repo"""

    if os.path.isdir(where_to):
        logging.info("Removing existing repo!!!: %s", where_to)
        subprocess.check_call(["rm", where_to, "-rf"])

    subprocess.check_call(["mkdir", "-p", where_to])

    git = sh.git.bake(_cwd=where_to)

    git("clone", repo)


    repo_root_fldr =  get_repo_name_from_path(repo)


    full_root_path = os.path.join(where_to, repo_root_fldr)

    print full_root_path

    return full_root_path



