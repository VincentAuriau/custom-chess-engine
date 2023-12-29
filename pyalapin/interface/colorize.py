import argparse
import os

from PIL import Image
import numpy as np


def color_one_img(pil_img, background_color, border_color, inner_color):
    img = np.array(pil_img)
    x_min = np.min(np.where(img == 255)[0])
    x_max = np.max(np.where(img == 255)[0])
    img = img[x_min:x_max]

    r_dict = {0: background_color[0], 128: inner_color[0], 255: border_color[0]}
    g_dict = {0: background_color[1], 128: inner_color[1], 255: border_color[1]}
    b_dict = {0: background_color[2], 128: inner_color[2], 255: border_color[2]}

    img = [
        np.vectorize(r_dict.get)(img),
        np.vectorize(g_dict.get)(img),
        np.vectorize(b_dict.get)(img),
    ]
    img = np.dstack(img)

    img = Image.fromarray(img.astype("uint8"))

    img = img.resize((int(img.size[0] / img.size[1] * 450), 450))

    x_coordinate = int((500 - img.size[0]) / 2)
    y_coordinate = 25

    background = np.dstack(
        [np.ones((500, 500)) * background_color[i] for i in range(3)]
    ).astype("uint8")
    background = Image.fromarray(background)
    background.paste(img, (x_coordinate, y_coordinate))
    return background


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ccb", "--color_cell_black", nargs="+")
    parser.add_argument("-ccw", "--color_cell_white", nargs="+")

    parser.add_argument("-ibp", "--inner_black_piece", nargs="+")
    parser.add_argument("-obp", "--outer_black_piece", nargs="+")

    parser.add_argument("-iwp", "--inner_white_piece", nargs="+")
    parser.add_argument("-owp", "--outer_white_piece", nargs="+")

    args = parser.parse_args()

    if args.color_cell_black is None:
        color_cell_b = [0, 191, 255]
    else:
        color_cell_b = [int(i) for i in args.color_cell_black]

    if args.color_cell_white is None:
        color_cell_w = [207, 185, 151]
    else:
        color_cell_w = [int(i) for i in args.color_cell_white]

    if args.inner_black_piece is None:
        inner_color_b = [109, 7, 26]
    else:
        inner_color_b = [int(i) for i in args.inner_black_piece]
    if args.outer_black_piece is None:
        border_color_b = [0, 0, 0]
    else:
        border_color_b = [int(i) for i in args.outer_black_piece]

    if args.inner_white_piece is None:
        inner_color_w = [200, 200, 200]
    else:
        inner_color_w = [int(i) for i in args.inner_white_piece]
    if args.outer_white_piece is None:
        border_color_w = [255, 255, 255]
    else:
        border_color_w = [int(i) for i in args.outer_white_piece]

    down_color_cell_b = np.clip(np.array(color_cell_b) - 70, 0, 255)
    down_color_cell_w = np.clip(np.array(color_cell_w) - 70, 0, 255)

    for img_name in os.listdir("../gs_illustrations"):
        img = Image.open(os.path.join("../gs_illustrations", img_name))
        img_bb = color_one_img(img, color_cell_b, border_color_b, inner_color_b)
        img_ww = color_one_img(img, color_cell_w, border_color_w, inner_color_w)
        img_wb = color_one_img(img, color_cell_w, border_color_b, inner_color_b)
        img_bw = color_one_img(img, color_cell_b, border_color_w, inner_color_w)

        down_img_bb = color_one_img(
            img, down_color_cell_b, border_color_b, inner_color_b
        )
        down_img_ww = color_one_img(
            img, down_color_cell_w, border_color_w, inner_color_w
        )
        down_img_wb = color_one_img(
            img, down_color_cell_w, border_color_b, inner_color_b
        )
        down_img_bw = color_one_img(
            img, down_color_cell_b, border_color_w, inner_color_w
        )

        name = img_name.split("_")[0]
        name = {
            "pawn": "P",
            "bishop": "B",
            "knight": "N",
            "rook": "R",
            "queen": "Q",
            "king": "K",
        }[name]
        img_bb.save(os.path.join("../temp_images", f"bb_{name}.png"))
        img_bw.save(os.path.join("../temp_images", f"bw_{name}.png"))
        img_wb.save(os.path.join("../temp_images", f"wb_{name}.png"))
        img_ww.save(os.path.join("../temp_images", f"ww_{name}.png"))

        down_img_bb.save(os.path.join("../temp_images", f"down_bb_{name}.png"))
        down_img_bw.save(os.path.join("../temp_images", f"down_bw_{name}.png"))
        down_img_wb.save(os.path.join("../temp_images", f"down_wb_{name}.png"))
        down_img_ww.save(os.path.join("../temp_images", f"down_ww_{name}.png"))

    bg_w = Image.fromarray(
        np.dstack([np.ones((500, 500)) * color_cell_w[i] for i in range(3)]).astype(
            "uint8"
        )
    )
    bg_w.save(os.path.join("../temp_images", "w.png"))
    bg_b = Image.fromarray(
        np.dstack([np.ones((500, 500)) * color_cell_b[i] for i in range(3)]).astype(
            "uint8"
        )
    )
    bg_b.save(os.path.join("../temp_images", "b.png"))

    down_bg_w = Image.fromarray(
        np.dstack(
            [np.ones((500, 500)) * down_color_cell_w[i] for i in range(3)]
        ).astype("uint8")
    )
    down_bg_w.save(os.path.join("../temp_images", "down_w.png"))
    down_bg_b = Image.fromarray(
        np.dstack(
            [np.ones((500, 500)) * down_color_cell_b[i] for i in range(3)]
        ).astype("uint8")
    )
    down_bg_b.save(os.path.join("../temp_images", "down_b.png"))
