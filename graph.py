from os import system
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import numpy as np

save_path = "PyRat-1-master/saves/"
rat_path = ""
python_path = ""

n_test = 10
n_min = 5
n_max = 31
n_step = 4
x_list = [n for n in range(n_min, n_max + n_step, n_step)]
rat_list = [0 for n in range(n_min, n_max + n_step, n_step)]
python_list = [0 for n in range(n_min, n_max + n_step, n_step)]


def extract_data(filename):
    with open(filename) as f:
        lines = f.readlines()
        input = eval(lines[0])
        output = eval(lines[-1])
    return input['x'], output['win_rat'], output['win_python']


def test(rat_path, python_path, n_test):
    global x_list
    for n in x_list:
        assert (n % 2 == 1)
        system(f"python3 PyRat-1-master/pyrat.py --rat {rat_path} --python {python_path} --nodrawing --synchronous --test {n_test} -x {n} -y {n} -p {n}")


def create_datas():
    global rat_list
    global python_list
    global x_list
    onlyfiles = [f for f in listdir(save_path) if isfile(join(save_path, f))]
    onlyfiles.remove(".gitignore")
    for file in onlyfiles:
        datas = extract_data(save_path + file)
        i = x_list.index(datas[0])
        rat_list[i] += datas[1]
        python_list[i] += datas[2]
    return rat_list, python_list


def draw():
    global rat_list
    global python_list
    f = plt.figure()
    plt.plot(x_list, rat_list, label='rat')
    plt.plot(x_list, python_list, label='python')
    plt.legend()
    plt.show()


test(rat_path, python_path, n_test)
create_datas()
draw()
