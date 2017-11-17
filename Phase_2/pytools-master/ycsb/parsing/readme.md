This folder contains scripts that can parse YCSB outputs. 

  - fast_cpp_ycsb_parser.cpp a C++ version of the parses that speeds up process. 
  - split_file.sh a script that can split a text file into multiple sub files for parallelization
  - parse_ycsb.py a wrapper, splits a large file and then uses cpp parser to parse chunks in parallel. 
