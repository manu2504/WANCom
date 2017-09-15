#!/usr/bin/python
import os
import logging
import sys
import subprocess
from pytools.common.common import *
from pytools.common.proc import check_pid_output
from pytools.ycsb.parsing.parse_ycsb_file import cpp_parse_ycsb_file
from pytools.ycsb.ycsb import YCSB_MASK, PARSED_FILE_EXTENSION, PARSING_VALID_PREFIXES
import traceback



def separator(msg):
    for _ in range(0, 5):
        print ">>>      "
    print ">>>      ", msg

    for _ in range(0, 5):
        print ">>>      "

def parse_ycsb_if_necessary(src_file_name):
    """ Function checks if a parsed file already present in the sub directory, if it is, then the
    parsed file name is returned, if there are no such file, then parsing is done at this stage"""

    if src_file_name.endswith(PARSED_FILE_EXTENSION):
        return src_file_name

    parsed_file_name = "%s.%s" % (src_file_name, PARSED_FILE_EXTENSION)

    if not os.path.isfile(parsed_file_name):
        logging.info("Parsed ycsb file [%s] not found, doing cpp parsing...", parsed_file_name)
        cpp_parse_ycsb_file(src_file_name, parsed_file_name, valid_prefixes=PARSING_VALID_PREFIXES)
        return parsed_file_name

    return src_file_name





def get_skip_initial_samples_min(post_proc_args):
    """ Function iterates over a list of arguments of the form
    ["plot_all_individual_cdfs", "visualise_traceworkload", "skipmins_3"]
    searches for "skipmins_3" and returns 3 in this case.
    This parameter indicates how many minutes to skip from the ycsb results"""

    for p in post_proc_args:
        if p.startswith("skipmins"):
            skipmins = int(p.split("_")[1])
            return skipmins
    return 0



def try_post_iteration_processing(conf, out_fldr, exp_id):


    if "results_post_processing" in conf["workload_1"]:
        minutes2skip_from_ycsb_trace = get_skip_initial_samples_min(
            conf["workload_1"]["results_post_processing"])
        if "p_hdrhistogram.slo" in conf["workload_1"]:
            target_slo_us = conf["workload_1"]["p_hdrhistogram.slo"]
        else:
            target_slo_us = 30000


        for post_task in conf["workload_1"]["results_post_processing"]:

            if post_task == "plot_cdfs":
                postproc_plot_cdfs_per_experiment(
                    out_fldr, exp_id, minutes2skip_from_ycsb_trace, target_slo_us)

            if post_task == "plot_all_individual_cdfs":
                postproc_plot_all_individual_cdfs(
                    out_fldr, target_slo_us, minutes2skip_from_ycsb_trace)


            if post_task == "plot_merged_cdf":
                postproc_plot_merged_cdf(out_fldr, minutes2skip_from_ycsb_trace)

            if post_task == "visualise_traceworkload":

                warm_up_period_sec = 0
                if "p_warmupperiod" in conf["workload_1"]:
                    warm_up_period_sec = conf["workload_1"]["p_warmupperiod"]

                postproc_visualise_traceworkload(
                    conf, out_fldr, exp_id=exp_id, warm_up_period_sec=warm_up_period_sec)



def postproc_model_logs(out_fldr):
    """ These scripts are designed to be executed after results from different remote YCSBs are
    being aggregated locally into one folder """
    fname = sys._getframe().f_code.co_name
    separator(fname)

    old_dir = os.getcwd()
    os.chdir(out_fldr)

    try:
        cmd = "model_rate_post_processor.r --src_folder {out_fldr}".format(out_fldr=out_fldr)

        logging.info("Executing [%s] \n cmd[%s]", fname, cmd)
        proc = subprocess.Popen(cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_pid_output(proc)

        # proc = subprocess.Popen(("Rscript " + ycsb_dir + "/models/model_rate_post_processor.r --f " + src_dir).split(), stdout=subprocess.PIPE)

    except:
        print_generic_exception()

    finally:
        os.chdir(old_dir)


def postproc_plot_all_individual_cdfs(out_fldr, target_slo_us, minutes2skip_from_ycsb_trace):
    """ This function searches for ycsb files in the target directory and plots a one .png
    file per one .ycsb file """
    separator(sys._getframe().f_code.co_name)

    old_dir = os.getcwd()
    os.chdir(out_fldr)

    try:

        files = get_files_matching_mask(where="./", mask=YCSB_MASK)
        print os.getcwd()
        print "Files, ", files

        for f in files:

            parsed_ycsb_file = parse_ycsb_if_necessary(f)

            cmd = "ycsb_plot_cdfs.py --src_files {src_files} --out_name {out_name} "\
                "--skip_first_samples_min {skip} --target_latency_slo_us {slo} "\
                "--consider_siblings --pre_parsed_input".format(
                src_files=parsed_ycsb_file,
                out_name="%s.png" % f,
                skip=minutes2skip_from_ycsb_trace,
                slo=target_slo_us)

            logging.info("Executing postproc_plot_all_individual_cdfs \n cmd[%s]", cmd)
            proc = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            check_pid_output(proc)

    except:
        print_generic_exception()

    finally:
        os.chdir(old_dir)


def postproc_plot_cdfs_per_experiment(
    out_fldr, exp_id, minutes2skip_from_ycsb_trace, target_slo_us, mask=YCSB_MASK):
    separator(sys._getframe().f_code.co_name)


    old_dir = os.getcwd()
    os.chdir(out_fldr)

    try:

        files = get_files_matching_mask(where="./", mask="i%s*.ycsb"%exp_id)
        print os.getcwd()
        print "Files, ", files
        cdf_files = []
        for f in files:
            out_file_name = "%s.%s" % (f, PARSED_FILE_EXTENSION)
            cdf_files.append(out_file_name)
            if not os.path.isfile(out_file_name):
                cpp_parse_ycsb_file(f, out_file_name, valid_prefixes=["READ"])

        cmd = "ycsb_plot_cdfs.py --src_files {src_files} --out_name {out_name} "\
            "--skip_first_samples_min {skip} --target_latency_slo_us {slo} "\
            "--consider_siblings --pre_parsed_input".format(
            src_files=" ".join(cdf_files),
            out_name="i%s_cdfs.png" % exp_id,
            skip=minutes2skip_from_ycsb_trace,
            slo=target_slo_us)

        logging.info("Executing postproc_plot_cdfs_per_experiment \n cmd[%s]", cmd)
        proc = subprocess.Popen(cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_pid_output(proc)

    except:
        print_generic_exception()

    finally:
        os.chdir(old_dir)


# def postproc_plot_cdfs(out_fldr, mask="*.ycsb", out_name="all_cdfs.png"):
#     """ This function looks for all *.ycsb files in the directory
#     and plots all CDFs for all of them"""
#     separator(sys._getframe().f_code.co_name)
#     logging.info("POST Processing, plotting all CDFs")

#     old_dir = os.getcwd()
#     os.chdir(out_fldr)

#     try:

#         files = get_files_matching_mask(where="./", mask=mask)
#         for f in files:
#             out_file_name = "%s.%s" % (f, PARSED_FILE_EXTENSION)
#             if not os.path.isfile(out_file_name):
#                 cpp_parse_ycsb_file(f, out_file_name, valid_prefixes=["READ"])

#         cmd = "ycsb_plot_cdfs.py --src_files %s --out_name %s --skip_first_samples_min %s" % (
#             " ".join(["%s.%s" % (x, PARSED_FILE_EXTENSION) for x in files]), out_name, 30)

#         logging.info("Executing postproc_plot_cdfs \n cmd[%s]", cmd)
#         proc = subprocess.Popen(cmd,
#             stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#         check_pid_output(proc)

#     except:
#         print_generic_exception()

#     finally:
#         os.chdir(old_dir)


def postproc_plot_merged_cdf(out_fldr, minutes2skip_from_ycsb_trace=0, mask=YCSB_MASK, out_name="merged_cdfs.png"):
    separator(sys._getframe().f_code.co_name)
    old_dir = os.getcwd()
    os.chdir(out_fldr)

    try:

        files = get_files_matching_mask(where="./", mask=mask)
        for f in files:
            parse_ycsb_if_necessary(f)

        merged_fname = "cdf.merged"
        proc = subprocess.Popen("echo \"\" > %s" % merged_fname,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_pid_output(proc)

        cdf_files = get_files_matching_mask(where="./", mask=YCSB_MASK)

        for f in cdf_files:
            cmd = "cat %s > %s" % (f, merged_fname)
            logging.info("cmd[%s]", cmd)
            proc = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            check_pid_output(proc)

        cmd = "ycsb_plot_cdfs.py --src_files %s --out_name %s --skip_first_samples_min %s --consider_siblings --pre_parsed_input" % (merged_fname, out_name, minutes2skip_from_ycsb_trace)
        logging.info("Executing postproc_plot_merged_cdf \n cmd[%s]", cmd)
        proc = subprocess.Popen(cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_pid_output(proc)

    except:
        print_generic_exception()

    finally:
        os.chdir(old_dir)



def try_postprocessing(conf, workload_name, of_ycsb_out, mask=YCSB_MASK):

    #    if conf[workload_name]["p_workload"] == "com.yahoo.ycsb.workloads.TraceWorkload":
    #       postproc_traceworkload(conf, workload_name, of_ycsb_out)

    if "only_stats" in conf and conf["only_stats"] == "1":
        tmp_out = "%s.short" % of_ycsb_out
        cmd = "head -n 5000 {inn} > {tmp_out}".format(inn=of_ycsb_out, tmp_out=tmp_out)
        print "Executing: ", cmd
        proc = subprocess.Popen(cmd, shell=True)
        check_pid_output(proc)

        print "Executing: ", cmd
        cmd = "tail -n 5000 {inn} >> {tmp_out}".format(inn=of_ycsb_out, tmp_out=tmp_out)
        print "Executing: ", cmd
        proc = subprocess.Popen(cmd, shell=True)
        check_pid_output(proc)

        print "Executing: ", cmd
        cmd = "mv {tmp_out} {inn}".format(inn=of_ycsb_out, tmp_out=tmp_out)
        print "Executing: ", cmd
        proc = subprocess.Popen(cmd, shell=True)
        check_pid_output(proc)
    pass


def postproc_visualise_traceworkload(
    conf, out_fldr, exp_id=None, mask=YCSB_MASK, warm_up_period_sec=0):

    separator(sys._getframe().f_code.co_name)
    def get_exp_and_workload_ids(ycsb_out_file_name):
        # i1_wl1_ycsb.ycsb
        tokens = ycsb_out_file_name.split("_")
        exp_id = int(tokens[0][1:])
        workload_id = int(tokens[1][2:])

        return exp_id, workload_id

    old_dir = os.getcwd()
    os.chdir(out_fldr)

    if exp_id != None:
        mask = "i%s%s" % (exp_id, mask)

    try:
        files = get_files_matching_mask(where="./", mask=mask)
        print os.getcwd()
        print "Files", files
        for f in files:
            print "Processing file: ", f

            exp_id, workload_id = get_exp_and_workload_ids(os.path.basename(f))
            tmp_R_file = "%s.r" % f

            cpp_parse_ycsb_file(f, tmp_R_file, valid_prefixes=["R"], pattern=2)

            workload_name = "workload_%s" % workload_id

            cmd = "visualize_ycsb_trace.R "\
                    "--intended_ts_file {trace_file} --actual_ts_file {tmp_R_file}"\
                    " --duration 1000 --interval 1 --id {id} --warmup {warmup} ".format(
                trace_file=conf[workload_name]["p_tracefile"],
                tmp_R_file=tmp_R_file, warmup=warm_up_period_sec,
                id=exp_id)

            logging.info("Executing post processing for workloadTrace 2/2 \n cmd[%s]", cmd)
            proc = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            check_pid_output(proc)

            logging.info("Removing tmp file [%s]", tmp_R_file)
            remove_files([tmp_R_file])


        # exp_index = os.path.basename(of_ycsb_out)[:2] # taking iX from i1_ycsb.ycsb

        # tmp_out_file = "%s_r.data" %exp_index

        # # cmd = 'cat %s | grep " R " |  awk "NF==3{print}{}" > %s' % (
        # #     of_ycsb_out, tmp_out_file)

        # # logging.info("Executing post processing for WorkloadTrace 1/2 \n cmd[%s]", cmd)
        # # proc = subprocess.Popen(cmd,
        # #     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # # check_pid_output(proc)

        # cmd = "visualize_ycsb_trace.R "\
        #         "--intended_ts_file {trace_file} --actual_ts_file {tmp_out_file}"\
        #         " --duration 1000 --interval 1 --id {id}".format(
        #     trace_file=conf[workload_name]["p_tracefile"],
        #     tmp_out_file=tmp_out_file,
        #     id=exp_index)

        # logging.info("Executing post processing for workloadTrace 2/2 \n cmd[%s]", cmd)
        # proc = subprocess.Popen(cmd,
        #     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # check_pid_output(proc)


    except:
        print_generic_exception()



    finally:
        os.chdir(old_dir)
