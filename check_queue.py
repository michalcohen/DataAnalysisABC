import os

max_pool = 12
files = list()


def process_dir(d, out):
    print(d)
    for entry in os.scandir(d):
        base_path = entry.path[:entry.path.rindex(".")]
        if entry.is_file() and entry.path.endswith(".aig") and (not entry.path.endswith("_fixed.aig") and not os.path.isfile(base_path + "_fixed.aig")):
            os.system(f"/home/assaf/michal/abc/abc -c \"read {entry.path}; zero; fold; write_aiger {base_path}_fixed.aig\"")

    # os.system(f"python /home/assaf/michal/extavy/avy/ext/brunch.py --out {out}.txt {out}_fixed.aig -v 2")
    # os.system(f"python /home/assaf/michal/extavy/avy/ext/brunch.py --out {out}_q.txt {out}_fixed.aig -v 2 -q")

    os.system(f"/home/assaf/michal/extavy/avy/ext/brunch.py --no-ts --out {out} --format base:Cpu:Frames:Invar:run:Result {d}/*_fixed.aig -- /home/assaf/michal/extavy/build/avy/src/avypdr -v 2 {{f}}")
    os.system(f"/home/assaf/michal/extavy/avy/ext/brunch.py --no-ts --out {out}_q --format base:Cpu:Frames:Invar:run:Result {d}/*_fixed.aig -- /home/assaf/michal/extavy/build/avy/src/avypdr -v 2 -q {{f}}")


def scan_subdirectories(dir_name, output_file):
    for entry in os.scandir(dir_name):
        if entry.is_dir():
            process_dir(entry.path, output_file)
            scan_subdirectories(entry.path, output_file)


def main(root):
    scan_subdirectories(root, "results")
    # with Pool(max_pool) as p:
    #     pool_outputs = list(tqdm.tqdm(p.imap(process_dir, files), total=len(files)))


if __name__ == "__main__":
    main("../hwmcc20")
