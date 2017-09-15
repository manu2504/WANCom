#!/usr/bin/python

import matplotlib.pyplot as plt

E6flt = 1000*1000.0
E9int = 1000*1000*1000



def tracedirection2plot_name(dm, td):
    return src_dst2plot_name(dm, td.source(), td.destination())

def path2plot_name(dm, p):
    return src_dst2plot_name(dm, p.source(), p.destination())


def src_dst2plot_name(dm, src_ip, dst_ip):
    """ converts src/dst into readable form based on endnode names"""
    return "{}--{}".format(
            dm.ndm.getEndNodeByIp(src_ip).name,
            dm.ndm.getEndNodeByIp(dst_ip).name
            )

def path_pair_ids2legend_names(dm, path_pair_ids):
    out_legend_buf = []

    out_legend_buf.append("Forward path:")

    path = dm.pdm.pid2Path[path_pair_ids[0]]
    for i, h in enumerate(path.hops):
        out_legend_buf.append("%2i) %s" %(i, h))

    out_legend_buf.append(" ")
    out_legend_buf.append("Reverse path:")
    path = dm.pdm.pid2Path[path_pair_ids[1]]
    for i, h in enumerate(path.hops):
        out_legend_buf.append("%2i) %s" %(i, h))

    return out_legend_buf


def get_new_figure():
    """ returns a figure with default common configuration """
    return plt.figure(dpi=1000, figsize=(18,10))

def close_figure():

    # cleanup
    plt.clf()
    plt.cla()
    plt.close()
