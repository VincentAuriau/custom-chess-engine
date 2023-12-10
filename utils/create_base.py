import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

black_pawn = np.array(Image.open("../dev-illustrations/queen_grey.png"))
black_pawn = black_pawn.astype("float32")
black_pawn = black_pawn.astype("uint8")
print("I_I")
print(black_pawn[0][:10])
print("I_I")
print(black_pawn[120][200])
print(np.unique(black_pawn[:, :, :3]))
print("R")
print(np.unique(black_pawn[:, :, 0]))
print("G")
print(np.unique(black_pawn[:, :, 1]))
print("B")
print(np.unique(black_pawn[:, :, 2]))
print("A")
print(np.unique(black_pawn[:, :, 3]))
plt.imshow(black_pawn[:, :, :])
plt.show()
plt.imshow(black_pawn[:, :, 3], cmap="gray")
plt.show()

bp = black_pawn.copy()

"""
Beautification of the Bishop

for i in range(300, 400):
	for j in range(120, 368):
		bp[i][j][0] = 255
		bp[i][j][1] = 255
		bp[i][j][2] = 255

for i in range(400, 440):
	for j in range(124, 368):
		bp[i][j][0] = 255
		bp[i][j][1] = 255
		bp[i][j][2] = 255

for i in range(440, 500):
	for j in range(125+int((i-440) / 2), 368-int((i-440) / 1.5)):
		bp[i][j][0] = 255
		bp[i][j][1] = 255
		bp[i][j][2] = 255


for i in range(460, 500):
	for j in range(250+int((i-460) / 2), 359-int((i-460) / 1.5)):
		bp[i][j][0] = 255
		bp[i][j][1] = 255
		bp[i][j][2] = 255

for i in range(500, 519):
	for j in range(155+2*(i-500), 330-2*(i-500)):
		bp[i][j][0] = 255
		bp[i][j][1] = 255
		bp[i][j][2] = 255


"""
"""
for i, j in zip([479, 480, 481]*3, [138, 138, 138, 139, 139, 130, 140, 140, 140]):
	bp[i][j][0] = 255
	bp[i][j][1] = 0
	bp[i][j][2] = 0
for i, j in zip([480, 481, 482], [141, 141, 142]):
	bp[i][j][0] = 255
	bp[i][j][1] = 0
	bp[i][j][2] = 0
plt.figure()
plt.imshow(bp[:, :, :3])
plt.show()
"""

"""
# Beautification of Rook

for i in range(80, 86):
	for j in range(114, 168):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120
for i in range(42, 86):
	for j in range(114, 120):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120
for i in range(42, 86):
	for j in range(162, 168):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120

for i in range(80, 86):
	for j in range(205, 259):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120

for i in range(86, 90):
	for j in range(205, 260):
		bp[i][j][0] = 100
		bp[i][j][1] = 100
		bp[i][j][2] = 100

for i in range(42, 86):
	for j in range(205, 211):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120
for i in range(42, 86):
	for j in range(253, 259):
		bp[i][j][0] = 120
		bp[i][j][1] = 120
		bp[i][j][2] = 120
"""

plt.figure()
plt.imshow(bp[:, :, :3])
plt.show()

black_pawn = bp

black_pawn = black_pawn[:, :, :3]
for h in range(len(black_pawn)):
	row = black_pawn[h]
	for w in range(len(row)):
		pix = row[w]
		for i in range(len(pix)):
			if pix[i] in list(range(116, 165)):
				black_pawn[h][w][i] = 255
			elif pix[i] == 255 or pix[i] == 0:
				pix[i] = 0
			else:
				pix[i] = 128 * (i == 0)

plt.imshow(black_pawn[:, :, :3])
plt.show()

img = Image.fromarray(black_pawn[:, :, 0])
img.save("../gs_illustrations/queen_grey.png")
print(black_pawn)

r_dict = {0:0, 128: 255, 255: 175}
g_dict = {0:0, 128: 192, 255: 238}
b_dict = {0:0, 128: 203, 255: 238}
own_pawn = [np.vectorize(r_dict.get)(black_pawn[:, :, 0].astype("uint8")), 
np.vectorize(g_dict.get)(black_pawn[:, :, 0]),
np.vectorize(b_dict.get)(black_pawn[:, :, 0])]
own_pawn = np.dstack(own_pawn)
rose = 255, 192, 203
turq = 175,238,238
print(own_pawn)
plt.imshow(own_pawn)
plt.show()

