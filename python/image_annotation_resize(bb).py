import csv
import urllib.request
import urllib
import json
from PIL import Image, ImageFile


def main():
    input = "(path to csv data)"
    output = "(path to new csv data)"
    hd_folder = "(path to directory)"
    crop_folder = "(path to directory)"
    final_arr = []

    with open(input, 'r') as csvfile:
        source = csv.reader(csvfile)
        next(source)

        for row in source:
            print("working")
            # column number of HD Image
            hd_link = get_image(row[3], hd_folder)
            name = hd_link[1]
            hd_img = Image.open(hd_link[0])
            # column number of downsample image
            ds_img = row[4]
            # column number of annotation
            pre_anno = row[0]
            if pre_anno == "" or pre_anno == " ":
                continue
            anno = json.loads(pre_anno)
            # column number unique id
            # rid = row[16]
            sizehd = hd_img.size
            sizeds = getsizes(ds_img)
            w_ratio = sizehd[0]/sizeds[0]
            h_ratio = sizehd[1]/sizeds[1]

            # print(sizehd)
            # print(sizeds)
            # print("**********")

            j = 0
            for shape in anno:

                left_ds = shape['x']
                top_ds= shape['y']
                right_ds= shape['x'] + shape['width']
                bottom_ds= shape['y'] + shape['height']
                
                # Converting annotations (box points) to fit in hd images and expanding box by 50 pixels

                left = (left_ds * w_ratio) - 50
                top = (top_ds * h_ratio) - 50
                right = (right_ds * w_ratio) + 50
                bottom = (bottom_ds * h_ratio) + 50

                # top, left, bottom, right = 0, 0, 0, 0
                # shape_dict = {}
                # shape_dict['type'] = shape['type']
                # shape_dict['id'] = shape['id']
                # i = 1
                # new_points = []
                # for point in shape['points']:
                #     if i % 2 == 0:
                #         new_point = int(point * h_ratio)
                #         if int(new_point) < top or top == 0:
                #             top = int(new_point)
                #         if int(new_point) > bottom:
                #             bottom = int(new_point)
                #     else:
                #         new_point = int(point * w_ratio)
                #         if int(new_point) < left or left == 0:
                #             left = int(new_point)
                #         if int(new_point) > right:
                #             right = int(new_point)
                #     new_points.append(new_point)
                #     i += 1
                # shape_dict['points'] = new_points
                # shape_dict['active'] = shape['active']
                # annontation_new = json.dumps({"shapes": [shape_dict]})
                # final_arr.append([annontation_new, rid,
                #                   pre_anno, hd_img, ds_img, top, left, name,
                #                   i])
                # # name = name.split(".")
                # # ext = name[-1]
                # # reg_name = name[:-1]
                # # reg_name = "".join(reg_name)
                # # crop_name = crop_folder + reg_name + "_" + str(j) + "." + ext
                #
                # # top *= 1.0
                # # left *= 1.0
                # # if right * 1.2 > sizehd[0]:
                # #     right *= 1.2
                # # if bottom * 1.7 > sizehd[1]:
                # #     bottom *= 1.7
                #
                # top *= 0.9
                # left *= 0.9
                # if right * 0.9 > sizehd[0]:
                #     right *= 0.9
                # # else:
                # #    right = sizehd[0]
                # if bottom * 1.5 > sizehd[1]:
                #     bottom *= 1.5
                # # else:
                # #    bottom = sizehd[1]
                #
                # # if top - 50 > sizehd[0]:
                # #     top -= 50
                # # if left - 50 > sizehd[1]:
                # #     left -= 50
                # # if right + 50 > sizehd[0]:
                # #     right += 50
                # # else:
                # #    right = sizehd[0]
                # # if bottom + 50 > sizehd[1]:
                # #     bottom += 50
                # # else:
                # #    bottom = sizehd[1]
                #
                # if top - 50 > 0:
                #     top -= 50
                # if left - 50 > 0:
                #     left -= 50
                # if right + 50 < sizehd[0]:
                #     right += 50
                # if bottom + 50 < sizehd[1]:
                #     bottom += 50
                #
                crop_name = crop_folder + str(j) + "_" + name + ".png"
                crop_section(hd_img, left, top, right, bottom, crop_name)
                j += 1

    with open(output, 'a') as outcsv:
        writer = csv.writer(outcsv, delimiter=',')
        headers = ["annotation", "id", "annotation_ds", "hd_image",
                   "ds_image", "top", "left", 'name', "image_num"]
        writer.writerow(headers)

        i = 1
        for n in final_arr:
            writer.writerow(n)
            print("Adding Row %s to CSV: " + str(i))
            i += 1

def crop_section(image, left, top, right, bottom, output_name):

    img = image.crop((left, top, right, bottom))
    img.save(output_name)

def get_image(url, hdfolder):
    name = url.split("/")[-1]
    output_filename = hdfolder + name
    urllib.request.urlretrieve(url, output_filename)
    return(output_filename, name)


def getsizes(url):
    file = urllib.request.urlopen(url)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    data = file.read(1024)
    p.feed(data)
    if p.image:
        return p.image.size
    else:
        print("Error no size")
        return None


if __name__ == '__main__':
    main()
