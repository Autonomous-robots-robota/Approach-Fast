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

    tuples = list(zip(xs, ys))
    df = pd.DataFrame(tuples, columns=["x", "y"])
    ax = df.plot(kind="line", x="x", y="y", figsize=(7, 7))
    ax.scatter(drone_pos[0], drone_pos[1], color='red', label='Drone start Position')
    ax.scatter(hit_pos[0], hit_pos[1], color='blue', label='Intercept Position')
    ax.legend()
    plt.show()



