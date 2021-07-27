import os


def process_dir(d, out):
    print(d)
    # for entry in os.scandir(d):
    #     base_path = entry.path[:entry.path.rindex(".")]
    #     if entry.is_file() and entry.path.endswith(".aig") and (not entry.path.endswith("_fixed.aig") and not os.path.isfile(base_path + "_fixed.aig")):
    #         os.system(f"/home/assaf/michal/abc/abc -c \"read {entry.path}; zero; fold; write_aiger {base_path}_fixed.aig\"")

    os.system(f"/home/assaf/michal/extavy/avy/ext/brunch.py --cpu 1900 --mem 8000 --no-hdr --no-ts --out {out} --format base:Cpu:Frames:Invar:run:Result {d}/*_fixed.aig -- /home/assaf/michal/extavy/build/avy/src/avypdr -v 2 {{f}}")
    os.system(f"/home/assaf/michal/extavy/avy/ext/brunch.py --cpu 1900 --mem 8000 --no-hdr --no-ts --out {out}_q --format base:Cpu:Frames:Invar:run:Result {d}/*_fixed.aig -- /home/assaf/michal/extavy/build/avy/src/avypdr -q -v 2 {{f}}")


def scan_subdirectories(dir_name, output_file):
    for entry in os.scandir(dir_name):
        if entry.is_dir():
            process_dir(entry.path, output_file)
            scan_subdirectories(entry.path, output_file)


def main(root):
    with open("results/stats", 'w') as f:
        f.write("base,Cpu,Frames,Invar,run,Result")
    with open("results_q/stats", 'w') as f:
        f.write("base,Cpu,Frames,Invar,run,Result")
    scan_subdirectories(root, "results")


if __name__ == "__main__":
    main("../hwmcc20")
