# -*- coding: utf-8 -*-


import cv2
from future.moves.tkinter import messagebox
from pylab import *
import os
from tkinter import filedialog
import json
import numpy


def getMatrix(add_img_path, rgb):
    add_image = cv2.imread(add_img_path)
    # 将界限值往左右移动10单位
    color_lower = [i - 10 for i in rgb]
    # print(color_lower)
    color_upper = [i + 10 for i in rgb]
    # print(color_upper)

    lower_blue = np.array(color_lower)
    upper_blue = np.array(color_upper)
    # 将add所选区域涂白,其他地方都是黑的
    add_mask_tem = cv2.inRange(add_image, lower_blue, upper_blue)
    np.set_printoptions(threshold=np.nan)
    np.set_printoptions(linewidth=1200)

    add_mask_tem = numpy.asarray(add_mask_tem/255, dtype='int32')
    print(add_mask_tem, end='')
    shortName = add_img_path.split(".")[0]
    file = open(shortName+r".txt", "w")
    # file.write(add_mask_tem)

    for i in range(len(add_mask_tem)):
        for j in range(len(add_mask_tem[i])):
            file.write(str(add_mask_tem[i][j]) + " ")
        file.write("\n")

    # numpy.savetxt("result", add_mask_tem)

    # len(add_mask_tem)
    # for i in range(len(add_mask_tem)):
    #     file.write(str(add_mask_tem[i]))
    file.close()


def getFilePath(add_dir_path):

    add_dir = os.listdir(add_dir_path)
    with open(add_dir_path + r"\rgb.json", 'r') as load_f:
        load_dict = json.load(load_f)
        rgb = load_dict["rgb"]
    rgb = [rgb[2], rgb[1], rgb[0]]
    for add_image_name in add_dir:
        if "bmp" not in add_image_name:
            continue
        getMatrix(add_dir_path + "/" + add_image_name, rgb)

messagebox.showinfo("提示", r"请选择文件夹")
# root = tk.Tk()
# root.withdraw()

file_path = filedialog.askdirectory()
getFilePath(file_path)
