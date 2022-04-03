import time
from turtle import pos
import numpy as np
import matplotlib.pyplot as plt
import random


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

def sign(x,w):
    if np.dot(x,w)>=0:
        return 1
    elif np.dot(x,w)<0:
        return -1

def PLA(dataset,w0,max_upd):
    iteration_times = 0
    w = w0
    num = len(dataset[0])
    X = np.array([dataset[0], dataset[1], np.ones(num,dtype=int)]).T
    Y = dataset[2]
    while iteration_times < max_upd:
        flag = True
        for j in range(num):
            if sign(X[j],w) != int(Y[j]):
                w += Y[j]*np.matrix(X[j]).T
                flag = False
                iteration_times += 1
            else:
                continue
        if flag:
            break
    return w, iteration_times

def pocket_algorithm(dataset,w0,max_upd):
    iteration_times = 0
    w = w0.copy()
    bestw = w0.copy()
    now_mistakes = 0
    num = len(dataset[0])
    X = np.array([dataset[0], dataset[1], np.ones(num,dtype=int)]).T
    Y = dataset[2]
    for j in range(num):
        if sign(X[j],w) != int(Y[j]):
            # print(j,end = ' ')
            now_mistakes += 1
    rand_sort = range(num)
    rand_sort = random.sample(rand_sort, num)
    while iteration_times < max_upd:
        flag = True
        for j in range(num):
            if sign(X[rand_sort[j]],w) != int(Y[rand_sort[j]]):
                w = bestw.copy()
                w += Y[rand_sort[j]] * np.matrix(X[rand_sort[j]]).T
                tmp_mistakes = 0
                for k in range(num):
                    if sign(X[k],w) != int(Y[k]):
                        tmp_mistakes += 1
                # print(tmp_mistakes,now_mistakes,end=' ')
                # print()
                if tmp_mistakes <= now_mistakes:
                    now_mistakes = tmp_mistakes
                    bestw = w.copy()
                iteration_times += 1
                flag = False
            else:
                continue
        if flag:
            break
    return bestw, iteration_times, now_mistakes

if __name__ == '__main__':
    # y = mx + b
    m, b = -2, 1

    # other parameters
    n_points = 2000
    rand_param = 30
    pos_num = int(n_points / 2)

    # plot
    fig = plt.figure()
    ax = plt.subplot(1,3,1)
    ax2 = plt.subplot(1,3,2)
    ax3 = plt.subplot(1,3,3)

    # plot function curve
    x = np.arange(rand_param + 1)   # x = [0, 1,..., rand_param]
    y = m * x + b
    ax.plot(x, y)
    ax2.plot(x, y)
    ax3.plot(x, y)

    # randomly generate points
    x_coors, y_coors, labels = rand_samples(m, b, n_points, rand_param)
    labels2 = labels.copy()
    for i in range(n_points):
        if i >= 950 and i < 1000:
            labels2[i] = -1.0
        if i >= 1950 and i < 2000:
            labels2[i] = 1.0

    # Perceptron Learning Algorithm
    dataset = [x_coors, y_coors, labels]
    w0 = np.zeros((3,1))
    max_upd = 100
    start = time.time()
    w, times = PLA(dataset,w0,max_upd)
    end = time.time()
    print('PLA number of iterations:{}'.format(times))
    print('PLA execute time:{}'.format(end-start))
    print('{}x + {}y + {}=0'.format(int(w[0]),int(w[1]),int(w[2])))
    x = np.arange(rand_param + 1,dtype=float)   # x = [0, 1,..., rand_param]
    y = (float(w[0]) * x + float(w[2])) / float(w[1]) * (-1.0)
    ax.plot(x, y, color='red')
    ax.set_title('PLA(red)\niterations:{}\ntime:{:.6f}'.format(times,end-start),loc='left')

    # PLA with pocket algorithm
    start = time.time()
    w0 = np.zeros((3,1))
    w2, times2, now_mis = pocket_algorithm(dataset,w0,max_upd)
    end = time.time()
    print('PLA with pocket algorithm number of iterations:{}'.format(times2))
    print('PLA with pocket algorithm execute time:{}'.format(end-start))
    print('{}x + {}y + {}=0'.format(int(w2[0]),int(w2[1]),int(w2[2])))
    if w2[1] != 0:
        x2 = np.arange(rand_param + 1,dtype=float)   # x = [0, 1,..., rand_param]
        y2 = (float(w2[0]) * x2 + float(w2[2])) / float(w2[1]) * (-1.0)
    else:
        y2 = np.arange(m * rand_param + b + 1,dtype=float)
        x2 = (float(w2[2]) * -1.0 + 0.0 * y2) / float(w2[0])
    ax2.plot(x2, y2, color='green')
    ax2.set_title('Pocket(green)\niterations:{}\ntime:{:.6f}'.format(times2,end-start),loc='left')

    # PLA with mislabel
    start = time.time()
    w0 = np.zeros((3,1))
    dataset2 = [x_coors, y_coors, labels2]
    w3, times3, now_mis = pocket_algorithm(dataset2,w0,max_upd)
    end = time.time()
    print('PLA with pocket algorithm number of iterations:{}'.format(times3))
    print('PLA with pocket algorithm execute time:{}'.format(end-start))
    print('{}x + {}y + {}=0'.format(int(w3[0]),int(w3[1]),int(w3[2])))
    if w3[1] != 0:
        x3 = np.arange(rand_param + 1,dtype=float)   # x = [0, 1,..., rand_param]
        y3 = (float(w3[0]) * x3 + float(w3[2])) / float(w3[1]) * (-1.0)
    else:
        y3 = np.arange(m * rand_param + b + 1,dtype=float)
        x3 = np.full(len(y3),(float(w3[2]) * -1.0) / float(w3[0]))
    ax3.plot(x3, y3, color='black')
    ax3.set_title('Pocket(black)\niterations:{}\ntime:{:.6f}\naccuracy:{}/2000'.format(times3,end-start,now_mis),loc='left')

    # plot random points. Blue: positive, red: negative
    ax.plot(x_coors[:pos_num], y_coors[:pos_num], 'o', color='blue')   # positive
    ax.plot(x_coors[pos_num:], y_coors[pos_num:], 'o', color='red')    # negative
    ax2.plot(x_coors[:pos_num], y_coors[:pos_num], 'o', color='blue')   # positive
    ax2.plot(x_coors[pos_num:], y_coors[pos_num:], 'o', color='red')    # negative
    ax3.plot(x_coors[:pos_num-50], y_coors[:pos_num-50], 'o', color='blue')   # positive
    ax3.plot(x_coors[n_points-50:], y_coors[n_points-50:], 'o', color='blue')   # positive
    ax3.plot(x_coors[pos_num-50:n_points-50], y_coors[pos_num-50:n_points-50], 'o', color='red')    # negative
    plt.show()