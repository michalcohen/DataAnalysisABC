import json
from copy import deepcopy

no_queue_check_path = "/home/assaf/michal/hwmcc20/aig/2019/wolf/2019C/qspiflash_dualflexpress_divfive-p154_fixed_no_q.json"

queue_check_path = "/home/assaf/michal/hwmcc20/aig/2019/wolf/2019C/qspiflash_dualflexpress_divfive-p154_fixed_q.json"

new_path = "/home/assaf/michal/hwmcc20/aig/2019/wolf/2019C/qspiflash_dualflexpress_divfive-p154_fixed_merged.json"


def get_node(nodes, name):
    try:
        return next(node for node in nodes if node["name"] == name)
    except StopIteration:
        return None


def get_edge(edges, name):
    try:
        return next(edge for edge in edges if edge["dest"] == name)
    except StopIteration:
        return None


def main():
    with open(no_queue_check_path, 'r') as f:
        d_no_q = json.load(f)
    with open(queue_check_path, 'r') as f:
        d_q = json.load(f)

    new_d = deepcopy(d_no_q)
    for first_node in new_d["pceNodeJson"]:
        first_node["source"] = 0
        for first_edge in first_node["preds"]:
            first_edge["source"] = 0

    for second_node in d_q["pceNodeJson"]:
        first_node = get_node(new_d["pceNodeJson"], second_node["name"])
        if first_node is None:
            second_node["source"] = 1
            for edge in second_node["preds"]:
                edge["source"] = 1
            new_d["pceNodeJson"].append(second_node)
        else:
            first_node["source"] = 2
            for edge in second_node["preds"]:
                first_edge = get_edge(first_node["preds"], second_node["name"])
                if first_edge is None:
                    edge["source"] = 1
                    first_node["preds"].append(edge)
                else:
                    first_edge["source"] = 2
    with open(new_path, 'w') as f:
        json.dump(new_d, f, indent=4)


if __name__ == "__main__":
    main()
