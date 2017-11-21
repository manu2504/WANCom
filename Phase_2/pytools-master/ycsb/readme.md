#### Run YCSB experiment multiple times

**ycsb_runner.py** can execute an experiment of a given configuration multiple times. The main input is a json configuration file which describes the experiment and the number of iterations it needs to repeat. Script extends **jobgenerator** which allows it to substitude various configurations using arguments.

Minimum configuration is looks like this
```json
{
    "cassandra": {
        "exp": {
            "repeat": 5
        }
    },

    "env": {
        "ycsb_dir": "/home/kirillb/projects/tectonic/cas/nc_ycsb"
    },

    "workload_1":{
        "timeout_min":60,
        "execute_on_host":"h1.4",
        "ycsb_cpus": 2,
        "workload_dir":"workloads/workloadc",
        "p_hosts":"172.31.12.37",
        "coordinators": [],
        "-cp":"./slf4j-simple-1.7.12.jar:/home/ec2-user/tec_javadriver/driver-core/target/cassandra-driver-core-3.0.8-SNAPSHOT.jar",
        "p_cassandra_writeconsistency":"ONE",
        "p_cassandra_readconsistencylevel":"LOCAL_ONE",
        "p_measurementtype":"raw",
        "p_measurement.interval":"both",
        "p_driver_maxconnections":128,
        "p_driver_newconnection_threshold_local":256,
        "p_driver_maxrequests_perconnection_local":512,
        "p_driver_maxqueuesize":50000,
        "p_recordcount":100000,

        "threads":"4000",
        "p_tracefile":"/home/ec2-user/traces/workloads/unix_ts_10_1.out_reg1.data_scle_900_ycsb.trace",
        "p_workload":"com.yahoo.ycsb.workloads.TraceWorkload",
        "p_driver_loadbalancer":"dcrr"
    },

}
```
Configuration must have at least one workload configuration with post-fix "_1" which identifies its sequence number.

* **`p_`** all arguments starting with "p_<key>:<value>" will be directly translated into YCSB's arguments of the form "-p key=value"
* **`execute_on_hosts`** List of hosts that are going to execute YCSB workload. Ideally should be different hosts from those that run Servers example: ["h1.3"]
* **`ycsb_cpus`** number of CPU cores allocated for each YCSB instance (if more than 1)
* **`host`** this is the first host in the list that YCSB will contact
* **`coordinators`** optional list of coordinators to use (see nc_ycsb repository)

#### Running multiple YCSB's at the same time

It is possible to start more than 1 YCSB. To do that specify additional workloads with subsequent indexes "_2", "_3" etc.
You do not have to duplicate all the entries from workload_1 but instead just specify new fields specific for these other YCSB, all properties not specified here will be taken from the "workload_1".

```json
    "workload_2":{
        "execute_on_hosts":"h1.3",
        "taskset_cpus":"15,13,11,9"
    },

    "workload_3":{
        "execute_on_hosts":"h1.2",
        "taskset_cpus":"7,5,3,1"
    }
```

#### How to convert YCSB report into a movie set of pictures

- Convert a sample ycsb report into a set of images
./logs2avi.py --src_files ./samples/sample.ycsb  --out_dir ./sample_out --n_jobs 16 --step_ms 10

- The create an avi file as follows
ffmpeg -r 30 -start_number 0 -i ./sample_out/img_%04d.png  -c:v libx264   -pix_fmt yuv420p sample.mp4


#### Making Videos out of YCSB raw report

First you will need ycsb report file that was recorded with ``-p measurementtype=raw`` property set on, then logs2avi.py script can be used to help you with creating the video.

**Examples**
```bash
logs2avi.py --src_files ./i1_ycsb.ycsb --out_dir "/ram_scratch/out/" --make_video  --step_ms 50 --res_size_ms 1000  --latency_lims 0 40


  --out_data_file OUT_DATA_FILE
                        This is a file where all plotting samples will be
                        stored for future replots (default: out.csv)
  --n_jobs N_JOBS       CPU threads to use (default: 16)
  --out_image_frmt_name OUT_IMAGE_FRMT_NAME
  --ffmpeg_image_frmt_name FFMPEG_IMAGE_FRMT_NAME
  --step_ms STEP_MS     Time step per frame [ms] (default: 100)
  --res_size_ms RES_SIZE_MS
                        How many samples to keep in a reservoir (based on time
                        interval) [ms] (default: 1000)
  --hist_buckets HIST_BUCKETS
                        Number of buckets in the histogram (default: 100)
  --latency_lims [LATENCY_LIMS [LATENCY_LIMS ...]]
                        Two values, defining the min and max latency values,
                        if not set the best fit will be used dynamically
                        (default: [])
  --figure_size_dpi FIGURE_SIZE_DPI
                        Three number defining the size of the figure per plot
                        + dpi resolution (default: [7, 7, 400])
  --make_video          Convert YCSB output into a video and store in
                        designated location (default: False)


```