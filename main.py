import configparser
import glob
import cv2

parser = configparser.ConfigParser()
parser.read("./config.ini")

margins = parser["Margins"]
paths = parser["Paths"]
config = parser["Main"]


# auxiliary funs

def img_crop(img, y_per=margins.getfloat("input_top"), x_per=margins.getfloat("input_left"),
             h_per=margins.getfloat("input_bottom"), w_per=margins.getfloat("input_right")):
    h, w, _ = img.shape
    return img[int(h * y_per):int(h * (1 - h_per)), int(w * x_per):int(w * (1 - w_per))]


def cap_crop(img, x, y, h, w, _, y_per=margins.getfloat("output_top"), x_per=margins.getfloat("output_left"),
             h_per=margins.getfloat("output_bottom"), w_per=margins.getfloat("output_right")):
    img_h, img_w, _ = img.shape
    return img[max(0, int(y - h * y_per)):min(int(y + h + h * h_per), img_h),
           max(0, int(x - w * x_per)):min(int(x + w + w * w_per), img_w)]


def cap_draw(src, x, y, h, w, _, y_per=margins.getfloat("output_top"), x_per=margins.getfloat("output_left"),
             h_per=margins.getfloat("output_bottom"), w_per=margins.getfloat("output_right")):
    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 0)
    cv2.rectangle(src, (int(x - w * x_per), int(y - h * y_per)),
                  (int(x + w + w * w_per), int(y + h + h * h_per)), (0, 255, 0), 2)


def debug_draw(src, stats, num_labels, max_label):
    for i in range(1, num_labels):
        if i == max_label:
            cap_draw(src, *stats[max_label])
            continue
        x, y, w, h, _ = stats[i]
        cv2.rectangle(src, (x, y), (x + w, y + h), (255, 255, 0), 0)


# main funs

def process_images(in_path, img_ext, min_area, show_debug=False):
    images = glob.glob(f"{in_path}/*.{img_ext}")
    print(f"Processing {len(images)} images... ")

    for image in images:
        img = img_crop(cv2.imread(image))

        _, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY_INV)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))

        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh)
        max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key=lambda j: j[1])
        print(f"Found area with size {max_size} in {image}")
        if max_size < min_area:
            print(f"Discarded!")
            continue

        res = cap_crop(img, *stats[max_label])
        img_name = "".join(image[2:].split('.')[:-1])
        cv2.imwrite(f"{img_name}_res.jpg", res)
        print(image)
        if show_debug:
            debug = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
            debug_draw(debug, stats, num_labels, max_label)
            cv2.imwrite(f"{img_name}_res_debug.jpg", debug)

    print(f"Finished!")


if __name__ == '__main__':
    process_images(paths.get("input_path"), config.get("input_ext"), config.getint("min_area"),
                   show_debug=config.getboolean("show_debug"))
