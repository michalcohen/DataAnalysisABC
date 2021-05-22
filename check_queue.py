import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd
import tqdm
from multiprocess import Pool
from pandas import DataFrame as df
from os.path import join
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from subprocess import run



dirname = join("/home/assaf127/extavy/", "beem")
frames_list = [filename for filename in os.listdir(dirname) if filename.endswith(".aig")]
max_pool = 12

        
def process_aig(f):
    file_name = f.split(".")[0]
    out_name = join(dirname, "results", file_name + ".txt")
    q_out_name = join(dirname, "results", file_name + "_q.txt")
    input_filename = join(dirname, file_name + ".aig")
    #with open(join("../extavy/beem", f.split(".")[0] + ".txt"), 'w') as out_f:
    os.system(f"~/extavy/build/avy/src/avypdr {input_filename} -v 2 > {out_name}")
    #with open(join("../extavy/beem", f.split(".")[0] + "_q.txt"), 'w') as out_f:
    os.system(f"~/extavy/build/avy/src/avypdr {input_filename} -v 2 -q > {q_out_name}")
    return f


def main():
    with Pool(max_pool) as p:
        pool_outputs = list(
            tqdm.tqdm(
                p.imap(process_aig,
                       frames_list),
                total=len(frames_list)
            )
        )


if __name__ == "__main__":
    #os.system(f"~/extavy/build/avy/src/avypdr /home/assaf127/extavy/beem/beemadd1f1.aig -v 1 | tee /home/assaf127/extavy/beem/beemadd1f1_log.txt")
    main()
