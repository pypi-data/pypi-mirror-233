import json_numpy


def write(path, obj_list):
    with open(path, "wt") as f:
        for obj in obj_list:
            f.write(json_numpy.dumps(obj, indent=None))
            f.write("\n")


def read(path):
    obj_list = []
    with open(path, "rt") as f:
        for line in f.readlines():
            obj_list.append(json_numpy.loads(line))
    return obj_list
