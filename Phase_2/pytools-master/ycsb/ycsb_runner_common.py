#!/usr/bin/python
import datetime
import logging
import os
import subprocess
import time
import itertools
import multiprocessing
import copy
import socket
from pytools.common.proc import check_pid_output
from pytools.common.common import *
from ycsb_post_processing import *


MNET = None

NAMING_PREFIX=""

def construct_ycsb_cmd(conf_workload, run_or_load):

    ycsb_dir = "./bin/ycsb"
    workload_dir = conf_workload["workload_dir"]

    cmd_list = [ycsb_dir, run_or_load,  "cassandra-cql",  "-P", workload_dir, "-s",
            "-threads", "%s"%conf_workload["threads"],
            "-p", "port=9042"]


    if "target" in conf_workload and conf_workload["target"]:
        cmd_list += ["-target", "%s"%conf_workload["target"]]

    cmd_list = check_add_p_properties(cmd_list, conf_workload)
    cmd_list = check_add_strp_properties(cmd_list, conf_workload)

    if conf_workload["coordinators"]:
        cmd_list += ["-p", "coordinators={}".format(
            ",".join(conf_workload["coordinators"]))]

    if "-cp" in conf_workload and conf_workload["-cp"]:
        cmd_list += ["-cp", conf_workload["-cp"]]

    cmd_list = check_add_driver_args(cmd_list, conf_workload)
    return cmd_list


def check_add_p_properties(cmd_list, conf):
    for prop_name, prop_val in conf.iteritems():
        if prop_name.startswith("p_") and prop_val:
            pname = prop_name[2:]
            cmd_list += ["-p", "%s=%s" %(pname, prop_val)]
    return cmd_list


def check_add_strp_properties(cmd_list, conf):
    """ a group of properties are being stringified and moved into a commma separated form
    example:
    "strp_driver_args": {
            "model_interval_ms":5000,
            "name":"test",
            }
    becomes:
    -p driver_args model_interval_ms:5000,name:test"""
    for prop_name, prop_val in conf.iteritems():
        if prop_name.startswith("strp_") and prop_val:
            arg_list = []
            for sub_pname, sub_pval in prop_val.iteritems():
                arg_list.append("%s:%s" % (sub_pname, sub_pval))
            pname = prop_name[5:]
            cmd_list += ["-p", "%s=%s" %(pname, ",".join(arg_list))]
    return cmd_list


def get_property_if_exists(conf, prop):
    if prop in conf and conf[prop]:
        return conf[prop]
    return None


def check_add_driver_args(cmd_list, conf):
    """ DRC driver takes a lot of arguments, which are encoded via driver_args sublist
    and passed as a comma sepratated list of tuples <k>:<v> """
    args = ""
    if "driver_args" in conf:
        for k, v in conf["driver_args"].iteritems():
            args = "{args},{key}:{value}".format(
                args=args, key=k, value=v)
        args = args[1:] # remove preceeding comma

        cmd_list += ["-p", "%s=%s" %("driver_args", args)]

    return cmd_list


def wait_on_ycsb(ycsb_proc, run_or_load, timeout_min=3*60):

    time_start = datetime.datetime.now()
    while True:
        retcode = ycsb_proc.poll()

        if retcode is not None:
            break # Process has terminated

        time.sleep(5)

        delta = (datetime.datetime.now() - time_start).seconds
        if timeout_min * 60 < delta:
            ycsb_proc.kill()
            raise RuntimeError("YCSB did not finished in time")

        logging.info("YCSB is %s-ing %d seconds. Timeout %d min",
            run_or_load, delta, timeout_min)


def _ycsb_execute(conf, workload_name, run_or_load, of_ycsb_out, loading_host=None):

    owd = os.getcwd()
    # os.chdir(conf["env"]["ycsb_dir"])
    os.chdir(conf[workload_name]["ycsb_dir"])

    ycsb_cmd_list = construct_ycsb_cmd(conf[workload_name], run_or_load)

    with open(of_ycsb_out, "w") as ycsb_out:

        # Set how many CPU cores we are allowed to use
        if get_property_if_exists(conf[workload_name], "taskset_cpus"):
            ycsb_cmd_list = [
            "taskset", "-c", get_property_if_exists(conf[workload_name], "taskset_cpus")
            ] \
            + ycsb_cmd_list


        logging.info("Launching YCSB in [%s] on host [%s] mode [%s]",
            run_or_load, loading_host, " ".join(ycsb_cmd_list))

        # Execute either on a mininet host or in the current environment natively
        if loading_host:
            ycsb_proc = loading_host.popen(
                ycsb_cmd_list, stdout=ycsb_out, stderr=ycsb_out, shell=False)
        else:
            ycsb_proc = subprocess.Popen(
                ycsb_cmd_list, stdout=ycsb_out, stderr=ycsb_out, shell=False)

        wait_on_ycsb(ycsb_proc, run_or_load, conf[workload_name]["timeout_min"])

    os.chdir(owd)


def try_prepare_kurma_configs(conf, out_fldr, iteration):
    """ This function tries to prepares special configuration for KURMA if certain fields are found
    If it is not a kurma configuration, then no changes will be applied.
    """

    if "strp_driver_args" in conf["workload_1"]:
        conf["workload_1"]["strp_driver_args"]["logging_folder"] = out_fldr
        conf["workload_1"]["strp_driver_args"]["logging_prefix"] = "i%s_" % iteration

    return conf


def prepare_multiple_configs(conf):
    """ This function uses workload_1 as a base, and then duplicates its configuration for all
    other workloads 2,3... while leaving properties already defined in subsequent workloads (2,3..)
    unchanged.

    """
    keys_starting_with_workload = []
    for k, _ in conf.iteritems():
        if k.startswith("workload"):
            keys_starting_with_workload.append(k)

    for k in keys_starting_with_workload:
        if k != "workload_1":
            merge_dicts(dst_dic=conf[k], src_dic=conf["workload_1"], overwrite=False)

    return conf, keys_starting_with_workload



##########################################################################################
# <1.> RUN YCSB API ######################################################################
##########################################################################################

def run_ycsb_multiple_native(conf, out_fldr, taskset_cpus=None):
    run_ycsb_multiple_parallel_iterations(conf, out_fldr, None, taskset_cpus, is_mininet=False)
    # if not taskset_cpus:
    #     taskset_cpus = get_property_if_exists(conf["workload"], "taskset_cpus")

def run_ycsb_multiple_mininet(conf, out_fldr, net, cpu_allocator=None):
    run_ycsb_multiple_parallel_iterations(conf, out_fldr, net, cpu_allocator, is_mininet=True)


##########################################################################################
# <2.> RUN YCSB REPEAT ITERATIONS ########################################################
##########################################################################################

def run_ycsb_multiple_parallel_iterations(
    conf, out_fldr, net, cpu_allocator=None, is_mininet=False):


    repeat = int(conf["cassandra"]["exp"]["repeat"])
    for iteration in range(1, repeat+1):

        run_ycsb_multiple_parallel(conf, out_fldr, net, iteration, cpu_allocator, is_mininet)

        time.sleep(10)

##########################################################################################
# <3.> RUN YCSB MULTIPROCESSING ##########################################################
##########################################################################################


def run_ycsb_multiple_parallel(
    conf, out_fldr, net, iteration, cpu_allocator=None, is_mininet=False):

    """ We can not pickle mininet object, thus we share it as a global variable """
    global MNET
    MNET = net

    conf = try_prepare_kurma_configs(conf, out_fldr, iteration)
    conf, workloads = prepare_multiple_configs(conf)

    for w in workloads:
        if is_mininet and not is_strin_anIP(conf[w]["p_hosts"]):
            # It is possible that mininet host has been already converted to an IP (iters)
            conf[w]["p_hosts"] = net.getNodeByName(conf[w]["p_hosts"]).IP()

            if cpu_allocator:
                conf[w]["taskset_cpus"] = cpu_allocator.get_next_cores4workload_string()
        conf[w]["workload_id"] = w.split("_")[1]


    logging.info("Running YCSB is_mininet=[%s], n_parallel_workloads=[%s]", is_mininet, len(workloads))

    pool = multiprocessing.Pool(processes=len(workloads))

    pool.map(_run_ycsb_singular_wrapper,
        itertools.izip(
            itertools.repeat(conf),
            workloads,
            itertools.repeat(out_fldr),
            itertools.repeat(iteration),
            itertools.repeat(is_mininet)
            )
        )

    pool.close()
    pool.join()

    logging.warning("YCSB iteration completed on [%s]", socket.gethostname())

    try_post_iteration_processing(conf, out_fldr, iteration)

def _run_ycsb_singular_wrapper(args):
    _run_ycsb_singular(*args)

def _run_ycsb_singular(conf, workload_name, out_fldr, iteration, is_mininet):

    loading_host = None
    global MNET

    if is_mininet:
        assert MNET
        net = MNET
        loading_host = net.getNodeByName(conf[workload_name]["execute_on_host"])

    try:
        _run_ycsb(conf, workload_name, out_fldr, iteration, loading_host)
    except  RuntimeError as e:
        logging.error(e)
        raise

def _run_ycsb(
    conf, workload_name, out_fldr, iteration, loading_host=None):

    ec2_region_name = get_property_if_exists(conf, "ec2_region_name")
    if not ec2_region_name:
        ec2_region_name = ""
    of_ycsb_out = os.path.join(out_fldr, "i{}_wl{}_{}_ycsb.ycsb".format(
        iteration, conf[workload_name]["workload_id"], ec2_region_name))

    _ycsb_execute(
        conf, workload_name, "run", of_ycsb_out, loading_host)

    try_postprocessing(conf, workload_name, of_ycsb_out)


##########################################################################################
# LOAD YCSB ##############################################################################
##########################################################################################

def load_ycsb_native(conf, out_fldr):
    dst_host_ip = conf["workload"]["host"]

    of_ycsb_out = os.path.join(out_fldr, "load.ycsb.log")

    _ycsb_execute(conf, "load", of_ycsb_out, dst_host_ip)


def load_ycsb_mininet(orig_conf, out_fldr, net, taskset_cpus, workload_name="workload_1"):

    # We are doing some temporal modifications to config, to speed up loading time
    conf = copy.deepcopy(orig_conf)
    conf[workload_name]["p_workload"] = "com.yahoo.ycsb.workloads.CoreWorkload"
    conf[workload_name]["threads"] = 32
    conf[workload_name]["p_operationcount"] = conf[workload_name]["p_recordcount"]

    loading_host = net.getNodeByName(conf[workload_name]["execute_on_host"])

    if not is_strin_anIP(conf[workload_name]["p_hosts"]):
        conf[workload_name]["p_hosts"] = net.getNodeByName(conf[workload_name]["p_hosts"]).IP()

    if taskset_cpus:
        conf[workload_name]["taskset_cpus"] = taskset_cpus

    of_ycsb_out = os.path.join(out_fldr, "load.ycsb.log")

    _ycsb_execute(
        conf, workload_name, "load", of_ycsb_out, loading_host)
