import glob
import cv2

import config

cfg = config.Config


def img_crop(img, y_per=cfg.IMG_MARGIN_Y, x_per=cfg.IMG_MARGIN_X, h_per=cfg.IMG_MARGIN_HEIGHT,
             w_per=cfg.IMG_MARGIN_WIDTH):
    h, w, _ = img.shape
    return img[int(h * y_per):int(h * h_per), int(w * x_per):int(w * w_per)]


def cap_crop(img, x, y, h, w, _, y_per=cfg.CAP_MARGIN_Y, x_per=cfg.CAP_MARGIN_X,
             h_per=cfg.CAP_MARGIN_HEIGHT, w_per=cfg.CAP_MARGIN_WIDTH):
    img_h, img_w, _ = img.shape
    return img[max(0, int(y - h * y_per)):min(int(y + h + h * h_per), img_h),
           max(0, int(x - w * x_per)):min(int(x + w + w * w_per), img_w)]


def cap_draw(src, x, y, h, w, _, margin_per=0.15):
    m = int(min(h, w) * margin_per)
    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 0)
    cv2.rectangle(src, (max(0, x - m), max(0, y - m)), ((x + w + m), (y + h + m)), (0, 255, 0), 2)


def debug_draw(src, stats, num_labels, max_label):
    for i in range(1, num_labels):
        if i == max_label:
            cap_draw(src, *stats[max_label])
            continue
        x, y, w, h, _ = stats[i]
        cv2.rectangle(src, (x, y), (x + w, y + h), (255, 255, 0), 0)


def process_images(path=cfg.SOURCE_PATH, ext=cfg.IMG_TYPE):
    images = glob.glob(f"{path}/*.{ext}")
    print(f"Processing {len(images)} images")

    for image in images:
        img = img_crop(cv2.imread(image))
        _, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY_INV)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))

        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh)
        max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key=lambda j: j[1])
        print(f"Max component size: {max_size}")
        if max_size < cfg.MIN_SIZE:
            print(f"Discarded!")
            continue

        res = cap_crop(img, *stats[max_label])

        if cfg.OUTPUT_MODE == config.SAVE_MODE:
            res_name = "".join(image.split('.')[:-1])
            cv2.imwrite(f"./{res_name}_res.jpg", res)

            if cfg.DEBUG:
                debug = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
                debug_draw(debug, stats, num_labels, max_label)
                cv2.imwrite(f"./{res_name}_res_debug.jpg", debug)

        elif cfg.OUTPUT_MODE == config.SHOW_MODE:
            cv2.namedWindow(image)
            cv2.imshow(image, res)
            cv2.waitKey(0)

            if cfg.DEBUG:
                debug = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
                debug_draw(debug, stats, num_labels, max_label)
                cv2.imshow(image, debug)
                cv2.waitKey(0)
            print("Press any key to show next")

    print(f"Finished!")
    if cfg.OUTPUT_MODE == config.SHOW_MODE:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    process_images()
