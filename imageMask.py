# -*- coding: utf-8 -*-

import cv2
from future.moves.tkinter import messagebox
from pylab import *
import os
from tkinter import filedialog
import json
import tkinter as tk


def rgb2gray(rgb):

    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def mask_change(source_img_path,add_img_path,save_path,rgb):

    source_img_black = cv2.imread(source_img_path)
    add_image = cv2.imread(add_img_path)

    # add_image_gray = cv2.cvtColor(add_image, cv2.COLOR_BGR2GRAY)
    # hsv = cv2.cvtColor(add_image, cv2.COLOR_BGR2HSV)

    # rgb = [255,255,0]


    color_lower = [i-10 for i in rgb]
    print(color_lower)
    color_upper = [i+10 for i in rgb]
    print(color_upper)
    # color_lower = (0, 250, 250)
    # color_upper = [10, 255, 255]

    # (T, mask_binary) = cv2.threshold(add_image_gray, rgb2gray(rgb), 255, cv2.THRESH_BINARY)  # 将非黑色部分全部涂白
    # cv2.imshow("a", mask_binary)
    # cv2.waitKey(0)

    lower_blue = np.array(color_lower)
    upper_blue = np.array(color_upper)

    # 将所选区域涂白,其他地方都是黑的
    mask = cv2.inRange(add_image, lower_blue, upper_blue)

    # 膨胀操作的卷集核
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    # 膨胀操作
    # mask_binary_dilation = cv2.dilate(mask, kernel)
    #
    # add_image_dilation = cv2.dilate(add_image, kernel)
    #
    # img_mask_rgb = cv2.bitwise_and(add_image_dilation, add_image_dilation, mask=mask_binary_dilation)

    img_mask_rgb = cv2.bitwise_and(add_image, add_image, mask=mask)
    final_image = source_img_black + img_mask_rgb
    cv2.imwrite(save_path, final_image)


def source_and_add_filepath_define(source_dir_path,add_dir_path):
    source_dir = os.listdir(source_dir_path)  # 读取制定路径下的全部文件
    add_dir = os.listdir(add_dir_path)  # 读取add文件夹下的全部文件
    # print(path)
    isafterfolderexist = os.path.exists(add_dir_path + "/after")  # add文件夹路径下是否存在after文件夹，如果不存在则创建

    if not isafterfolderexist:
        os.makedirs(add_dir_path + "/after")

    with open(add_dir_path + r"\rgb.json", 'r') as load_f:
        load_dict = json.load(load_f)
        rgb = load_dict["rgb"]
    rgb = [rgb[2], rgb[1], rgb[0]]

    for imgname in source_dir:
        if (imgname == "add" or imgname == "after" or imgname == "rbg.json"):
            continue
        print(imgname)
        shortName = imgname.split(".")[0]

        add_image_name = shortName + "_add.bmp"
        if add_image_name not in add_dir:
            add_image_name = shortName + "_add.BMP"
            if add_image_name not in add_dir:
                messagebox.showinfo("错误", "该souece文件不存在对应的add文件")
                continue

        mask_change(source_dir_path + "/" + imgname, add_dir_path + "/" + add_image_name,
                        add_dir_path + "/after/" + shortName + ".bmp",rgb)

def add_file_define(dir_path):
    dir = os.listdir(dir_path)  # 读取总路径下的全部文件
    source_dir_path = dir_path + r"/source"  # 最开始的source文件
    for i in range(1,10):  # 默认最多有10个add类
        add_dir_path = dir_path + r"/add_"+str(i)
        print(add_dir_path)
        if(r"add_"+str(i) not in dir):
            messagebox.showinfo("提示", r"操作完毕")
            break
        if i != 1:
            source_dir_path = dir_path+r"/add_"+str(i-1)+r"/after"
        source_and_add_filepath_define(source_dir_path, add_dir_path)

messagebox.showinfo("提示", r"请选择文件夹")
# root = tk.Tk()
# root.withdraw()

file_path = filedialog.askdirectory()
add_file_define(file_path)
