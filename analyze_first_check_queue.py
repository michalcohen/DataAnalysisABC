import os

dirname = "../beem"
frames_list = []  # [os.path.join(dirname, filename) for filename in os.listdir(dirname) if filename.endswith(".txt")]
for subdir in os.listdir(dirname):
    if subdir.startswith("results"):
        continue
    frames_list += set(
        [os.path.join(dirname, subdir, filename) for filename in os.listdir(os.path.join(dirname, subdir)) if
         filename.endswith(".txt")])
max_pool = 12
keys = ["Frames", "Invar", "Pdr_solve", "blockCube", "ensureFrames", "ensureFrames_Invar", "generalize", "pushClauses",
        "pushClauses.Pdr_ManCheckCube", "run", "solverAddClause"]


def get_data_from_file(filename):
    with open(filename, "r") as f_obj:
        data = f_obj.read()
        last_level = int(data.split(" : ")[-2].split("\n")[-1].lstrip())
        proof_count = data.count(" : ")
        res = data.split("Result: ")[1].split("\n")[0] == 'true'
        stat_ind = data.rfind("************** BRUNCH STATS *****************")
        end_ind = data.rfind("************** BRUNCH STATS END *****************")

        stats = data[stat_ind + len("************** BRUNCH STATS *****************"): end_ind]
        d = {}
        stats = stats.split("\nBRUNCH_STAT ")[1:]
        result = stats[-1].split(" ")[1].strip()
        stats = stats[:-1]

        for stat in stats:
            x = stat.split(" ")
            d[x[0]] = float(x[1])
        return last_level, proof_count, result, d


def process_aig(f):
    if f.endswith("_q.txt"):
        return
    base_name = os.path.splitext(f)[0]
    f_q = base_name + "_q.txt"
    if os.path.isfile(f) and os.path.isfile(f_q):
        try:
            last_level_no_q, proof_count_no_q, res_no_q, d_no_q = get_data_from_file(f)
        except:
            print("non complete: " + f)
            return
        try:
            last_level_q, proof_count_q, res_q, d_q = get_data_from_file(f_q)
        except:
            print("non complete: " + f_q)
            return
        try:
            if res_q != res_no_q:
                print("not eq: " + f)
                return
            result = [base_name, res_q]
            for key in keys:
                if key not in d_no_q:
                    result.append('nan')
                else:
                    result.append(str(d_no_q[key]))
            for key in keys:
                if key not in d_q:
                    result.append('nan')
                else:
                    result.append(str(d_q[key]))
            for key in keys:
                if key not in d_q or key not in d_no_q:
                    result.append('nan')
                else:
                    result.append(str(d_q[key] / d_no_q[key]) if d_no_q[key] != 0 else "nan")
            return ",".join(result)
        except KeyError:
            print("wrong keys: " + f_q)
            return
        # return (proof_count_q / proof_count_no_q)
        # return (last_level_q / last_level_no_q)
        # return d_no_q, d_q


pool_outputs = [process_aig(v) for v in frames_list]
pool_outputs = [output for output in pool_outputs if output is not None]

lines = [",".join(["FileName", "Result"] + keys + [key + "_q" for key in keys] + [key + "_r" for key in keys])] + pool_outputs
with open("tmp.csv", 'w') as f:
    f.write("\n".join(lines))
