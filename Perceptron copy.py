import time
import numpy as np
import matplotlib.pyplot as plt


def rand_samples(m, b, n_points, rand_param):
    x_coors, y_coors, labels = np.array([]), np.array([]), np.array([]) # create empty array

    # the size of figure
    x_rand_param = rand_param
    y_rand_param = [m * x_rand_param + b , b]
    if m < 0:
        tmp = y_rand_param[0]
        y_rand_param[0] = y_rand_param[1]
        y_rand_param[1] = tmp

    # number of positive and negtive samples
    pos_num = int(n_points / 2)
    neg_num = n_points - pos_num

    # randomly generate points
    for state, n_points in [['pos', pos_num], ['neg', neg_num]]:
        if state == 'pos':
            cnt = 0
            while cnt < pos_num:
                x = np.random.randint(x_rand_param)
                y = np.random.randint(y_rand_param[1],y_rand_param[0])
                if y - m * x - b < -(rand_param/20):
                    cnt += 1
                    x_coors = np.append(x_coors, x)
                    y_coors = np.append(y_coors, y)
                    labels = np.append(labels, np.ones(1, dtype=int))
        else:
            cnt = 0
            while cnt < neg_num:
                x = np.random.randint(x_rand_param)
                y = np.random.randint(y_rand_param[1],y_rand_param[0])
                if y - m * x - b > (rand_param/20):
                    cnt += 1
                    x_coors = np.append(x_coors, x)
                    y_coors = np.append(y_coors, y)
                    labels = np.append(labels, -1 * np.ones(1, dtype=int))
    return x_coors, y_coors, labels

if __name__ == '__main__':
    # y = mx + b
    m, b = 1, 3

    # other parameters
    n_points = 30
    rand_param = 30
    pos_num = int(n_points / 2)


    # plot function curve
    x = np.arange(rand_param + 1)   # x = [0, 1,..., rand_param]
    y = m * x + b
    plt.plot(x, y)
    plt.title('y = {}x + {}'.format(m,b))

    # randomly generate points
    x_coors, y_coors, labels = rand_samples(m, b, n_points, rand_param)

    # plot random points. Blue: positive, red: negative
    plt.plot(x_coors[:pos_num], y_coors[:pos_num], 'o', color='blue')   # positive
    plt.plot(x_coors[pos_num:], y_coors[pos_num:], 'o', color='red')    # negative
    plt.show()