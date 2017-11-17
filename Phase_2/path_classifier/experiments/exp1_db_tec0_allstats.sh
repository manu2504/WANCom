#!/bin/bash

echo "****************"
echo ""
echo "This script connects to DB tec(0) and plots all stats to output dir"
echo ""
echo "****************"

OUT_DIR=/home/kirillb/data_sets_nc/KERNEL_TECTONIC/tec0

# ./../vis.py --out_dir $OUT_DIR \
#             --plot_tracedir_rtt

# ./../vis.py --out_dir $OUT_DIR \
#             --plot_path_pairs_boxes 30 True


# ./../vis.py --out_dir $OUT_DIR \
#             --plot_path_pairs_hist 6984 93 2372 688 6209 3795 5056 464 \
#             3742 724 3747 191 3747 724 3742 191 \
#             121 841 121 4044 133 841 121 341


# ./../vis.py --out_dir $OUT_DIR \
#             --plot_path_pairs_timeline 6984 93 2372 688 6209 3795 5056 464 \
#             3742 724 3747 191 3747 724 3742 191 \
#             121 841 121 4044 133 841 121 341


./../vis.py --out_dir $OUT_DIR \
            --plot_path_pairs_timeline_top 10