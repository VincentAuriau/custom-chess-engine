import numpy as np
from PIL import Image

from settings import settings

class ColorEditor(object):

	def __init__(self, 
				white_cell, 
				down_white_cell,
				black_cell, 
				down_black_cell,
				white_piece_fill, 
				white_piece_border, 
				black_piece_fill, 
				black_piece_border):

		self.white_cell = white_cell
		self.down_white_cell = down_white_cell
		self.black_cell = black_cell
		self.down_black_cell = down_black_cell
		self.white_piece_fill = white_piece_fill
		self.white_piece_border = white_piece_border
		self.black_piece_fill = black_piece_fill
		self.black_piece_border = black_piece_border

	def get_edited_black_cell(self):
		return np.array([[self.black_cell] * 64] * 64), np.array([[self.down_black_cell] * 64] * 64)

	def get_edited_white_cell(self):
		return np.array([[self.white_cell] * 64] * 64), np.array([[self.down_white_cell] * 64] * 64)

	def get_edited_black_material(self, material_type, cell_color):
		if cell_color == "black":
			cell_color = self.black_cell
		else:
			cell_color = self.white_cell

		image = Image.open(settings["grayscale_images"][material_type])
		r_map = {0: cell_color[0], 128: self.black_piece_fill[0], 255: self.black_piece_border[0]}
		g_map = {0: cell_color[1], 128: self.black_piece_fill[1], 255: self.black_piece_border[1]}
		b_map = {0: cell_color[2], 128: self.black_piece_fill[2], 255: self.black_piece_border[2]}

		edited_img = np.array(image)
		edited_img = np.dstack([np.vectorize(r_map.get)(edited_img), 
				np.vectorize(g_map.get)(edited_img),
				np.vectorize(b_map.get)(edited_img)])

		if cell_color == "black":
			cell_color = self.down_black_cell
		else:
			cell_color = self.down_white_cell

		r_map = {0: cell_color[0], 128: self.black_piece_fill[0], 255: self.black_piece_border[0]}
		g_map = {0: cell_color[1], 128: self.black_piece_fill[1], 255: self.black_piece_border[1]}
		b_map = {0: cell_color[2], 128: self.black_piece_fill[2], 255: self.black_piece_border[2]}

		down_edited_img = np.array(image)
		down_edited_img = np.dstack([np.vectorize(r_map.get)(edited_img), 
				np.vectorize(g_map.get)(edited_img),
				np.vectorize(b_map.get)(edited_img)])

		return edited_img, down_edited_img

	def get_edited_white_material(self, material_type):
		if cell_color == "black":
			cell_color = self.black_cell
		else:
			cell_color = self.white_cell

		image = Image.open(settings["grayscale_images"][material_type])
		r_map = {0: cell_color[0], 128: self.white_piece_fill[0], 255: self.white_piece_border[0]}
		g_map = {0: cell_color[1], 128: self.white_piece_fill[1], 255: self.white_piece_border[1]}
		b_map = {0: cell_color[2], 128: self.white_piece_fill[2], 255: self.white_piece_border[2]}

		edited_img = np.array(image)
		edited_img = np.dstack([np.vectorize(r_map.get)(edited_img), 
				np.vectorize(g_map.get)(edited_img),
				np.vectorize(b_map.get)(edited_img)])

		if cell_color == "black":
			cell_color = self.down_black_cell
		else:
			cell_color = self.down_white_cell

		r_map = {0: cell_color[0], 128: self.white_piece_fill[0], 255: self.white_piece_border[0]}
		g_map = {0: cell_color[1], 128: self.white_piece_fill[1], 255: self.white_piece_border[1]}
		b_map = {0: cell_color[2], 128: self.white_piece_fill[2], 255: self.white_piece_border[2]}

		down_edited_img = np.array(image)
		down_edited_img = np.dstack([np.vectorize(r_map.get)(edited_img), 
				np.vectorize(g_map.get)(edited_img),
				np.vectorize(b_map.get)(edited_img)])

		return edited_img	


	def generate_all_images(self, path="temp_illustrations"):
		b = self.get_edited_black_cell()
		Image.from_array(b).save(os.path.join(path, "b.png"))
		w = self.get_edited_black_cell()
		Image.from_array(b).save(os.path.join(path, "w.png"))
		for piece in ["pawn", "bishop", "knight", "rook", "king", "queen"]:
			b_p = self.get_edited_black_material(material_type=piece, )

