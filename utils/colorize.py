import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

black_pawn = np.array(Image.open("../dev-illustrations/knight_grey.png"))
black_pawn = black_pawn.astype("float32")
black_pawn = black_pawn.astype("uint8")
print(black_pawn[300])

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


black_pawn = black_pawn[:, :, :3]
for h in range(len(black_pawn)):
	row = black_pawn[h]
	for w in range(len(row)):
		pix = row[w]
		for i in range(len(pix)):
			if pix[i] in list(range(116, 165)):
				black_pawn[h][w][i] = 255
			elif pix[i] == 0:
				pass
			else:
				pix[i] = 128 * (i == 0)

plt.imshow(black_pawn[:, :, :3])
plt.show()
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

