import numpy as np
import math

def get_path():
    path_list = [(63, 20), (75, 36), (103, 36), (115,44), (115,68), (115,78), (115,88),
                 (119,96), (119,106), (121,106), (123,120), (129,136), (129,145), (131,152), (144,169), (159,192), (169,212),
                 (179, 216), (189, 222),(203,236), (227,256), (251, 256), (263, 244)]

    path_matrix = np.zeros((300,300), dtype = (int,2))

    def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    for i in range(0,300):
        for j in range(0,300):
            max_ind = 0
            max_point = (0,0)
            for ind, point in enumerate(path_list):
                d = distance((i,j), point)

                if ind > max_ind and d<75:
                    max_ind =ind
                    max_point = point


            path_matrix[i][j] = (max_point[0]-i, max_point[1]-j)
            #print(i,j, 'path', path_matrix[i][j])
    return path_matrix

#print(get_path()[60][20])


# for i in range(40,300):
#     for j in range(40,300):
#         print(path_matrix[i][j])