from os import system
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
import os


ai_list = [
    # "etape8_1",
    # "etape8",
    "etape8_enemyScore_scraped",
    "etape8_2",
    "etape8_3"
]

save_path = "PyRat-1-master/saves/"
# rat_path = "PyRat-1-master/AIs/etape8_1.py"
python_path = "PyRat-1-master/AIs/etape6_1.py"

n_test = 150
n_min = 5
n_max = 45
n_step = 4  # must be odd
x_list = [n for n in range(n_min, n_max + n_step, n_step)]
rat_list = [0 for n in range(n_min, n_max + n_step, n_step)]
python_list = [0 for n in range(n_min, n_max + n_step, n_step)]
rat_miss = [0 for n in range(n_min, n_max + n_step, n_step)]


def extract_data(filename):
    with open(filename) as f:
        lines = f.readlines()
        input = eval(lines[0])
        output = eval(lines[-1])
    return input['x'], output['win_rat'], output['win_python'], output['miss_rat']


def test(rat_path, python_path, n_test):
    global x_list
    for n in x_list:
        assert (n % 2 == 1)
        system(f"python3 PyRat-1-master/pyrat.py --rat {rat_path} --python {python_path} --nodrawing --test {n_test} -x {n} -y {n} -p {n} --save --synchronous")


def create_datas():
    global rat_list
    global python_list
    global x_list
    global rat_miss
    rat_list = np.array(rat_list)
    python_list = np.array(python_list)
    rat_miss = np.array(rat_miss)

    onlyfiles = [f for f in listdir(save_path) if isfile(join(save_path, f))]
    onlyfiles.remove(".gitkeep")
    for file in onlyfiles:
        datas = extract_data(save_path + file)
        i = x_list.index(datas[0])
        rat_list[i] += datas[1]
        python_list[i] += datas[2]
        rat_miss[i] += datas[3]
    rat_list = list(rat_list / n_test)
    python_list = list(python_list / n_test)
    rat_miss = list(rat_miss / n_test)


def write_datas():
    f = open("./datas", 'a')
    f.write(f"{rat_path}\n")
    f.write(f"{rat_list}\n")
    f.write(f"{python_list}\n")
    f.write(f"{rat_miss}\n")
    f.close()


def read_datas():
    f = open("./datas", 'r')
    lines = f.readlines()
    f.close()
    for i in range(0, len(lines), 4):
        lines[i] = lines[i].split('/')[-1][:-4]
        lines[i + 1] = eval(lines[i + 1])
        lines[i + 2] = eval(lines[i + 2])
        lines[i + 3] = eval(lines[i + 3])

    max_miss = 0
    for i in range(0, len(lines), 4):
        local_max = np.max(lines[i + 3])
        if local_max > max_miss:
            max_miss = local_max
    return lines, max_miss


def draw():
    global x_list
    datas, max_miss = read_datas()
    for i in range(0, len(datas), 4):
        f, ax1 = plt.subplots(constrained_layout=True)
        ax2 = ax1.twinx()
        t, = ax1.plot(x_list, datas[i + 1], label=f"win rate of {datas[i]}")
        cl = t.get_color()
        ax1.plot(x_list, datas[i + 2], color=cl, linestyle="--", label="Win rate of etape6_1")
        ax2.bar(x_list, datas[i + 3], color=cl, alpha=0.5)
        ax2.set_ylim(0, max_miss * 1.10)

        ax1.set_xlabel("Size of maze and number of cheese")
        ax1.set_ylabel(f"Win rate in {n_test} try")
        ax2.set_ylabel("Mean of misses")
        plt.title(f"Result of duel between {datas[i]} with etape6_1 (greedy with eyes)")
        ax1.legend()
        plt.savefig(f"./result_{datas[i]}.png", dpi=600)
        # plt.clf()
    # plt.show()


def clear_saves():
    for file_name in os.listdir(save_path):
        # construct full file path
        file = save_path + file_name
        if os.path.isfile(file) and file_name != ".gitkeep":
            os.remove(file)


def main():
    global rat_path
    for ai in ai_list:
        rat_path = f"PyRat-1-master/AIs/{ai}.py"
        test(rat_path, python_path, n_test)
        create_datas()
        write_datas()
        clear_saves()
    read_datas()
    draw()


read_datas()
draw()
# clear_saves()
# main()
