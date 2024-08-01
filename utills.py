import csv
import pandas as pd
import matplotlib.pyplot as plt



def load_csv2(file):
    df = pd.read_csv(file)
    # print(df['pre_dist'])
    return df


def plot_parbulah(a, b, c, x_start, x_end, drone_pos, hit_pos):
    xs = []
    ys = []
    if x_start <= x_end:
        for x in range(x_start, x_end + 1):
            y = a * (x ** 2) + b * x + c
            xs.append(x)
            ys.append(y)
    else:
        for x in range(x_start, x_end -1, -1):
            y = a * (x ** 2) + b * x + c
            xs.append(x)
            ys.append(y)

    # tuples = list(zip(xs, ys))
    # df = pd.DataFrame(tuples, columns=["x", "y"])
    # ax = df.plot(kind="line", x="x", y="y", figsize=(7, 7))
    # ax.scatter(drone_pos[0], drone_pos[1], color='red', label='Drone start Position')
    # ax.scatter(hit_pos[0], hit_pos[1], color='blue', label='Intercept Position')
    # ax.legend()
    plt.plot(xs,ys)
    plt.scatter(drone_pos[0], drone_pos[1], color='red', label='Drone start Position')
    plt.scatter(hit_pos[0], hit_pos[1], color='blue', label='Intercept Position')
    plt.show()


def plot_parbulah_and_linear(a, b, c, m, n, drone_pos, intercept_pos):
    xs = []
    ys = []
    zs = []
    if drone_pos[0] <= intercept_pos[0]:
        for x in range(int(drone_pos[0])-1, int(intercept_pos[0])+1 ):
            y = a * (x ** 2) + b * x + c
            xs.append(x)
            ys.append(y)
            z = m * x + n
            zs.append(z)
    else:
        for x in range(int(intercept_pos[0])-1, int(drone_pos[0])+1):
            y = a * (x ** 2) + b * x + c
            xs.append(x)
            ys.append(y)
            z = m * x + n
            zs.append(z)
    plt.figure(figsize=(12, 7))

    plt.subplot(1, 2, 1)
    plt.plot(xs, ys)
    plt.scatter(drone_pos[0], drone_pos[1], color='red', label='Drone start Position')
    plt.scatter(intercept_pos[0], intercept_pos[1], color='blue', label='Intercept Position')
    plt.legend()
    plt.title("x-y path")
    plt.axis('scaled')
    plt.xlabel("x axis")
    plt.ylabel("y axis")

    plt.subplot(1, 2, 2)
    plt.plot(xs, zs)
    plt.scatter(drone_pos[0], drone_pos[2], color='red', label='Drone start Position')
    plt.scatter(intercept_pos[0], intercept_pos[2], color='blue', label='Intercept Position')
    plt.legend()
    plt.title("x-z path")
    plt.axis('scaled')
    plt.xlabel("x axis")
    plt.ylabel("z axis")

    plt.show()
