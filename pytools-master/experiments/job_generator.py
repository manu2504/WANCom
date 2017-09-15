#!/usr/bin/python
import argparse
import itertools
import json
import copy
from pytools.common.common import merge_dicts

def get_value_from_string(value):

    if value.isdigit():
        return int(value)
    elif value.replace('.','',1).isdigit(): # replacing only a single "."
        return float(value)
    return value

def setProperty(jdata, prop, value):
    plist = prop.split(".")
    dic = jdata
    for i,p in enumerate(plist):
        # print i, p
        if (i+1) < len(plist):
            dic = dic[p]
        else:
            dic[p] = get_value_from_string(value)

def constructVariations(var):

    if var.startswith("list:"):
        var_list = var.split(":")
        assert len(var_list) == 2
        var_list = var_list[1].split(",")
        return var_list
    else:
        raise NotImplementedError()

def get_generators_argparser():

    parser = argparse.ArgumentParser("Job Generator")
    parser.add_argument("--cfg_json",
        type=argparse.FileType("r"), help="Initial Source Config File")

    parser.add_argument("--cfg_jsons",  nargs='*', default=[],
        type=argparse.FileType("r"),
        help="Sequence of config files, all configs are merged into the first one")

    parser.add_argument("--comment", default="", help="Comment for the given experiment")

    parser.add_argument("--properties", nargs='*',
        default=[],
        help="""List of properties where json fields separated by dots e.g.:
        ycsb.threads ycsb.launch_from_host, replay.type """)

    parser.add_argument("--ranges", nargs='*',
        default=[],
        help="""List of matching ranges for properties, or lists of strings separated by |
        list:32,64,128,256,512,1024 list:h4,h5 list:static,dynamic """)

    parser.add_argument("--allowed_machines", nargs='*', default=[],
        help="List of machines that allowed to take these jobs. Jobs will be spread equally")

    parser.add_argument("--single_assignment", action='store_true',
        help="If set each task will be assigned only to a single machine. Round robin allocation")

    return parser

def merge_group_configs(cfg_jsons):
    """ we get list of cfg json files, we load each and merge into the first one in
    the list. Then return result"""
    jdata = json.load(cfg_jsons[0])
    for cfg in cfg_jsons[1:]:
        jcfg = json.load(cfg)
        merge_dicts(jdata, jcfg, overwrite=True)
    return jdata

def construct_elm_list(properties, ranges):
    elm_list = []
    for i, p in enumerate(properties):
        # for each property that we want to variate we construct
        # a list of possible parameters
        # e.g. ycsb.threads => [1,2,4,8...]
        prop_var = constructVariations(ranges[i])

        # for each possible option, we pair parameter with option
        # e.g. [(ycsb.threads, 1), (ycsb.threads, 2)...]
        prop_var = [(p, x) for x in prop_var]

        elm_list.append(prop_var)

    return elm_list


def generate_jobs_configs_from_file(path_cfg_json, properties, ranges):
    jdata = json.load(path_cfg_json)
    generate_jobs_configs_from_json(jdata, properties, ranges)

def generate_jobs_configs_from_json(jdata, properties, ranges):
    assert len(properties) == len(ranges)

    elm_list = construct_elm_list(properties, ranges)

    job_list = []
    for _, props in enumerate(itertools.product(*elm_list)):
        job_id = ""
        job_short_id = ""
        job_fields_id = ""
        for prop, value in props:
            setProperty(jdata, prop, value)
            job_id += prop.split(".")[-1] + str(value) + "."
            job_short_id += "%s." % value
            job_fields_id += "[%s]" % prop

        jdata["job_id"] = job_id[:-1] # remove trailing dot "."
        jdata["job_short_id"] = job_short_id[:-1]
        jdata["job_fields_id"] = job_fields_id
        job_list.append(copy.deepcopy(jdata))

    return job_list

