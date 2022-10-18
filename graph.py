from os import system
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
import os


ai_list=["etape8_1","etape8","etape8_enemyScore_scraped"]

save_path = "PyRat-1-master/saves/"
rat_path = "PyRat-1-master/AIs/etape8_1.py"
python_path = "PyRat-1-master/AIs/etape6_1.py"

n_test = 100
n_min = 5
n_max = 41
n_step = 4 # must be odd
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
        system(f"python3 PyRat-1-master/pyrat.py --rat {rat_path} --python {python_path} --nodrawing --synchronous --test {n_test} -x {n} -y {n} -p {n} --save")


def create_datas():
    global rat_list
    global python_list
    global x_list
    rat_list = np.array(rat_list)

    onlyfiles = [f for f in listdir(save_path) if isfile(join(save_path, f))]
    onlyfiles.remove(".gitkeep")
    for file in onlyfiles:
        datas = extract_data(save_path + file)
        i = x_list.index(datas[0])
        rat_list[i] += datas[1]
        python_list[i] += datas[2]
    rat_list = list(rat_list / n_test)

def write_datas():
    f = open("./datas",'a')
    f.write(f"{rat_path}\n")
    f.write(f"{rat_list}\n")
    f.close()

def read_datas():
    f = open("./datas",'r')
    lines = f.readlines()
    f.close()
    for i in range(0,len(lines),2):
        lines[i] = lines[i].split('/')[-1][:-4]
        lines[i+1] = eval(lines[i+1])
    return lines

def draw():
    global x_list
    datas = read_datas()
    f = plt.figure()
    for i in range(0,len(datas),2):
        plt.plot(x_list, datas[i+1], label=f"{datas[i]}")
    plt.xlabel("Size of maze and number of cheese")
    plt.ylabel(f"Win rate in {n_test} try")
    plt.title("Result of duel with etape6_1 (greedy with eyes)")
    plt.legend()
    plt.show()


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

clear_saves()
main()