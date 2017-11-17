#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <cstdint>
#include <assert.h>
#include <set>
#include <unordered_set>
#include <stdio.h>
#include <string.h>
#include <algorithm>

#define TIMESTAMP_2014 1400000000000
#define TIMESTAMP_2022 1600000000000
                       


#define CHECK_UNIX_TIMESTAMP_NS(pch, res)  \
        uint64_t time_ns = strtoull(pch, &res, 10); \
        if ((*res) || (time_ns == UINT64_MAX)) { \
            return 2; \
        } else if ((time_ns < TIMESTAMP_2014) || (time_ns > TIMESTAMP_2022)) { \
            return 22; \
        } 


std::unordered_set<std::string> valid_values;

int is_valid_line_patter_1(std::string line) {
    char* pch;
    char *res;
    int pos_count = 0;
    // Check that we only have 2 commas in the line
    size_t n_commas = std::count(line.begin(), line.end(), ',');
    if (n_commas != 2 ) {
        return 6;
    }
    pch = strtok((char*)line.c_str(),",");
    while (pch != NULL) {
      if (pos_count == 0) {
        std::string token(pch);
        if (valid_values.find(token) == valid_values.end()) {
            return 1;
        }
      } else if (pos_count == 1) {
        CHECK_UNIX_TIMESTAMP_NS(pch, res);
      } else if (pos_count == 2) {
        // try to convert to uint32
        uint64_t latency = strtoull(pch, &res, 10);
        if ((*res) || (latency == UINT64_MAX)) {  // conversion failed
            return 3;
        }
      }
      pch = strtok(NULL, ",");
      pos_count++;
    }

    if (pos_count != 3) return 4;

    return 0;
}

/* Capturing R output in the form:
<thread id> R <time offset ns>
example:
37 R 67699261
*/
int is_valid_line_patter_2(std::string line) {
    char* pch;
    char *res;
    int pos_count = 0;
    pch = strtok((char*)line.c_str()," ");
    while (pch != NULL) {
      if (pos_count == 0) {
        // try to convert to uint32
        uint64_t latency = strtoull(pch, &res, 10);
        if ((*res) || (latency == UINT64_MAX)) {  // conversion failed
            return 1;
        }
      } else if (pos_count == 1) {
        std::string token(pch);
        if (valid_values.find(token) == valid_values.end()) {
            return 2;
        }

      } else if (pos_count == 2) {
        // try to convert to uint64
        uint64_t time_ns = strtoull(pch, &res, 10);
        if ((*res) || (time_ns == UINT64_MAX)) {  // conversion failed
            return 3;
        }
      }
      pch = strtok(NULL, " ");
      pos_count++;
    }

    if (pos_count != 3) return 4;

    return 0;
}


int main(int argc, char *argv[]) {
    if (argc < 4) {
        return 1;
    }

    std::string ifilename = argv[1];
    std::string ofilename = argv[2];
    int pattern = atoi(argv[3]);

    for (int i = 4; i < argc; i++) {
        valid_values.insert(argv[i]);
    }

    // std::cout << "Input     File: " << ifilename << std::endl;
    // std::cout << "Output    File: " << ofilename << std::endl;
    // std::cout << "Pattern       : " << pattern << std::endl;
    // std::cout << "Valid Prefixes: [";
    // for (auto it = valid_values.begin(); it != valid_values.end(); ++it) {
    //     std::cout << " " << *it;
    // }
    // std::cout << " ]" << std::endl;


    std::ifstream infile(ifilename);
    std::ofstream out(ofilename);

    int ret = 0;
    int line_count = 0;
    int valid_lines = 0;
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        line_count++;

        if (line_count % 1000000 == 0) {
            std::cout << "progress: " << line_count << std::endl;
        }

        size_t pos = 0;
        std::string token;

        if (pattern == 1) {
            ret = is_valid_line_patter_1(line);
        } else if (pattern == 2) {
            ret = is_valid_line_patter_2(line);
        } else {
            assert(false);  //  Unknown pattern
        }

        if (ret == 0) {
            out << line << std::endl;
            valid_lines++;
        }
    }

    out.close();
    infile.close();

    std::cout << "File: "<< ifilename <<" total lines parsed [ " << line_count <<
        " ] valid lines [ " << valid_lines << " ]" << std::endl;

    return 0;
}
