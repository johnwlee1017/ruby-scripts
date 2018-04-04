import csv
import urllib.request
import json
import cv2
import numpy as np


def draw_img(output_filename, anno_img, data_dict, alpha,
             category_labels, color_labels):
    full_img = cv2.imread(output_filename, cv2.IMREAD_COLOR)
    anno_img = cv2.imread(anno_img, cv2.IMREAD_COLOR)
    cols = len(full_img)
    rows = len(full_img[0])
    output = full_img.copy()
    overlay = full_img.copy()

    for i in range(cols):
        for j in range(rows):
            k = anno_img.item(i, j, 2)
            if k == 254:
                k = 0
            if k > 0:
                overlay.itemset((i, j, 0), data_dict[k][2])
                overlay.itemset((i, j, 1), data_dict[k][1])
                overlay.itemset((i, j, 2), data_dict[k][0])

    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    # This is for the key section, disable to not have key.
    blank_image = np.zeros((np.size(full_img, 0), 400, 3), np.uint8)
    blank_image.fill(255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Figure Eight Key:"
    x = 10
    y = 20
    cv2.putText(blank_image, text, (x, y), font, 0.8, (0, 0, 0), 1)
    y += 20
    for label, color in zip(category_labels, colors):
        cv2.rectangle(blank_image, (x, y), (x + 10, y + 10),
                      (color[2], color[1], color[0]), -2)
        text = " = " + label
        cv2.putText(blank_image, text, (x + 10, y + 10), font, 0.5,
                    (0, 0, 0), 1)
        y += 30
    # end key section
    new_img = np.concatenate((output, blank_image), axis=1)
    print("Writing Image")
    cv2.imwrite(output_filename, new_img)


# input csv and output folder for images
# output folder for full image
output = '/Users/johnlee/Desktop/python-scripts/images/'
input = '/Users/johnlee/Desktop/python-scripts/data/markov_data.csv'
# annotation folder to store annotation images
anno_folder = "/Users/johnlee/Desktop/python-scripts/anno/"
# order the colors in order of the categories here
colors = [
    [0,0,0],
    [0,0,255],
    [255,0,0]
    ]

# this section is for the key section, it should be in order and match
category_labels = [
                "Eraser",
                "Food",
                "Juice"
                ]
# end key section
annotation_col_number = 1
image_url_col_number = 0
# alpha is the degree of transparency btw 0.0(none) - 1.0(solid)
alpha = 0.5
# end of input areas

color_order = zip(range(0, len(colors)), colors)
data_dict = {}
for order, color in color_order:
    data_dict[order] = color

with open(input, 'r') as csvfile:
    source = csv.reader(csvfile)
    next(source)

    for row in source:
        anno = row[annotation_col_number]
        link = row[image_url_col_number]
        name = link.split("/")
        name = name[-1]

        if anno != '' and anno != "[]":
            output_filename = output + name
            anno_filename = anno_folder + name
            anno_link = json.loads(anno)["url"]
            full_img = urllib.request.urlretrieve(link, output_filename)
            anno_img = urllib.request.urlretrieve(anno_link, anno_filename)
            print(output_filename)
            draw_img(output_filename, anno_filename,
                     data_dict, alpha, category_labels, colors)
