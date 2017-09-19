import math
import time

import matplotlib.pyplot
import matplotlib.colors
import matplotlib.cm
import numpy
import scipy.io
import xlrd
import xlwt

time_start = time.time()

image_origin = numpy.zeros([180, 512])
image_number = numpy.zeros([1024, 1024])
image_target = numpy.zeros([1024, 1024])
image_detect = numpy.zeros([1, 1024])
wookbook = xlrd.open_workbook('A题附件.xlsx')
table = wookbook.sheet_by_name('附件5')

delta_degree =-29.6
delta_x =34.32
delta_y =23.11


# 计算卷积函数结果
def convolution(index):
    return -2 / (math.pi * math.pi * (4 * index * index - 1))

h = [convolution(x) for x in range(-512, 512)]

# 读取Excel表格数据
for d in range(table.ncols):
    image_origin[d] = table.col_values(d)

# 旋转并叠加图像
for d in range(0, image_origin.shape[0]):
    print(d)
    image_detect[0, 256:768] = image_origin[d]

    # 滤波处理
    image_convol = numpy.convolve(image_detect[0], h, mode='same')

    # 旋转处理
    image_middle = numpy.ones([1024, 1]) * image_convol

    image_rotate = numpy.zeros([1024, 1024])
    for y in range(image_middle.shape[0]):
        for x in range(image_middle.shape[1]):
            y_new = (x - 511.5) * math.sin((-d + delta_degree) / 180 * math.pi) + (y - 511.5) * math.cos((-d + delta_degree) / 180 * math.pi) + 511.5
            x_new = (x - 511.5) * math.cos((-d + delta_degree) / 180 * math.pi) - (y - 511.5) * math.sin((-d + delta_degree) / 180 * math.pi) + 511.5
            if 0 <= round(y_new) < 1024 and 0 <= round(x_new) < 1024:
                image_number[round(y_new), round(x_new)] += 1
                image_rotate[round(y_new), round(x_new)] = image_middle[y, x]

    # 图像叠加
    image_target += image_rotate

# 对叠加点求平均
for y in range(image_target.shape[0]):
    for x in range(image_target.shape[1]):
        if image_number[y, x] != 0:
            image_target[y, x] /= image_number[y, x]

# 保存Numpy以备以后调用
numpy.save("Figure_3_SL.npy", image_target)
scipy.io.savemat("Figure_3_SL.mat", {"I3SL": image_target[int(512 - 182 + delta_y):int(512 + 183 + delta_y), int(512 - 182 + delta_x):int(512 + 183 + delta_x)]})

# 显示结果
time_stop = time.time()
print(time_stop - time_start, 's')

matplotlib.pyplot.imshow(image_target[int(256 + delta_y):int(768 + delta_y), int(256 + delta_x):int(768 + delta_x)], cmap=matplotlib.cm.get_cmap('gist_gray'))
matplotlib.pyplot.colorbar()
matplotlib.pyplot.savefig('Figure_3_SL_512x512.png',dpi=200)

matplotlib.pyplot.imshow(image_target[int(512 - 182 + delta_y):int(512 + 183 + delta_y), int(512 - 182 + delta_x):int(512 + 183 + delta_x)], cmap=matplotlib.cm.get_cmap('gist_gray'))
matplotlib.pyplot.colorbar()
matplotlib.pyplot.savefig('Figure_3_SL_365x365.png',dpi=200)
