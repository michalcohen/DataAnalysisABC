import os
import tqdm
from multiprocess import Pool

max_pool = 12
files = list()


def process_aig(f):
    print(f)
    out = f[:f.rindex(".")]
    os.system(f"~/abc/abc -c \"read {f}; zero; fold; write_aiger {out}_fixed.aig\"")
    os.system(f"python ~/michal/extavy/avy/ext/brunch.py --out {out}.txt {out}_fixed.aig -v ")
    os.system(f"~/extavy/build/avy/src/avypdr {out}_fixed.aig -v 2 -q > {out}_q.txt")
    

def scan_directory(dir_name):
    for entry in os.scandir(dir_name):
        if entry.is_file() and entry.path.endswith(".aig") and not entry.path.endswith("_fixed.aig"):
            files.append(entry.path)
        elif entry.is_dir():
            scan_directory(entry.path)


def main(root):
    scan_directory(root)
    with Pool(max_pool) as p:
        pool_outputs = list(tqdm.tqdm(p.imap(process_aig, files), total=len(files)))


if __name__ == "__main__":
    main("../hwmcc20")
