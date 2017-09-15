#!/usr/bin/python
import os
import time
import subprocess
import json

time_stapm_format = "%Y-%m-%d_%H%M%S"

def setup_experiment_folder(exp_name, where="./", link_name="last_run"):

    exp_folder_path = mkdir_unique_results_folder(exp_name, where)

    create_end_shortcut_2results(exp_folder_path, link_name)

    return exp_folder_path

def mkdir_unique_results_folder(exp_name, where="./"):
    """
    Creates the directory where the results of the experiment will be stored
    @param exp_name: The name of this experiment
    """

    if not os.path.isdir(where):
        subprocess.check_call(["mkdir",  where])

    unique_fldr_name = "{time_stapm}_{exp_name}".format(
        time_stapm=time.strftime(time_stapm_format, time.gmtime()),
        exp_name=exp_name)

    exp_folder_path = os.path.join(where, unique_fldr_name)

    subprocess.check_call(["mkdir",  exp_folder_path])

    return exp_folder_path

def create_end_shortcut_2results(exp_folder_path, link_name="last_run"):
    """
    Links the directory where the results of the experiment will be stored

    @param exp_name: The output folder of this experiment
    """

    subprocess.check_call(["rm", link_name, "-rf"])

    subprocess.check_call(["ln", "-s", exp_folder_path, link_name])


def load_json_config(input_file):

    assert os.path.isfile(input_file)

    with open(input_file, "r") as ff:
        jconf = json.load(ff)
    return jconf


def make_dir(new_dir_name):
    """
    Recursively makes a directory if one does not exists yet
    """
    if not os.path.exists(new_dir_name):
        try:
            os.makedirs(new_dir_name)
        except OSError as e:
            print e
