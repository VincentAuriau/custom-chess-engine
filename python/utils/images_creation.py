import os

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

black_pawn = np.array(Image.open("own_illustrations/queen_grey.png"))

black_back = (np.array([0.4, 0.4, 0.8]) * 255).astype("uint8")
white_back = (np.array([0.4, 0.8, 0.4]) * 255).astype("uint8")

changed = []
for i in range(3):
    channel = np.copy(black_pawn[:, :, i])
    channel[black_pawn[:, :, i] < 137] = 100 * i
    channel[black_pawn[:, :, i] == 0] = 200 / (i + 1)
    channel[black_pawn[:, :, i] > 137] = 100 * i - 50
    changed.append(channel)

plt.figure()
plt.imshow(np.dstack(changed))
plt.show()

plt.figure()
plt.imshow(black_pawn)
plt.show()
# black_back = (np.dstack([np.ones((500, 500))*.4, np.ones((500, 500))*.4,
#                                     np.ones((500, 500))*.8]) * 255).astype('uint8')
# white_back = (np.dstack([np.ones((500, 500))*.4, np.ones((500, 500))*.8,
#                                     np.ones((500, 500))*.4]) * 255).astype('uint8')
#
# imgb = Image.fromarray(black_back)
# imgb.save('own_illustrations/b.png')
# imgb = Image.fromarray(white_back)
# imgb.save('own_illustrations/w.png')
#
# print(black_pawn.shape)
#
# # if black_pawn.shape[0] > 500 or black_pawn.shape[1] > 0:
# #     resize_ratio = 500 / max(black_pawn.shape[1], black_pawn.shape[0])
# #     print(resize_ratio)
# #     new_size = (int(resize_ratio * black_pawn.shape[0]), int(resize_ratio * black_pawn.shape[1]))
# #     print(new_size)
# #     black_pawn.resize(new_size, Image.LANCZOS)
#
# max_size = np.max([black_pawn.shape[0], black_pawn.shape[1]])
#
# #print(len(black_pawn[0]))
#
# plt.imshow(black_pawn)
# plt.show()
# #
# black_pawn_black_back = (np.dstack([np.ones((max_size, max_size))*.4, np.ones((max_size, max_size))*.4,
#                                     np.ones((max_size, max_size))*.8]) * 255).astype('uint8')
# for i in range(max_size):
#     for j in range(max_size):
#
#         h_plus = - int((black_pawn.shape[0] - max_size) / 2)
#         w_plus = - int((black_pawn.shape[1] - max_size) / 2)
#
#         if h_plus <= i < h_plus + black_pawn.shape[0] and w_plus <= j < w_plus + black_pawn.shape[1]:
#             if black_pawn[i-h_plus][j-w_plus][3] == 0:
#                 pass
#             else:
#                 black_pawn_black_back[i][j] = (black_pawn[i-h_plus][j-w_plus][:3])
#
#
# plt.imshow(black_pawn_black_back)
# plt.show()
#
# imgf = Image.fromarray(black_pawn_black_back).resize((500, 500))
# imgf.save('own_illustrations/bw_Q.png')
#
# black_pawn_black_back = (np.dstack([np.ones((max_size, max_size))*.4, np.ones((max_size, max_size))*.8,
#                                     np.ones((max_size, max_size))*.4]) * 255).astype('uint8')
# for i in range(max_size):
#     for j in range(max_size):
#
#         h_plus = - int((black_pawn.shape[0] - max_size) / 2)
#         w_plus = - int((black_pawn.shape[1] - max_size) / 2)
#
#         if h_plus <= i < h_plus + black_pawn.shape[0] and w_plus <= j < w_plus + black_pawn.shape[1]:
#             if black_pawn[i-h_plus][j-w_plus][3] == 0:
#                 pass
#             else:
#                 black_pawn_black_back[i][j] = (black_pawn[i-h_plus][j-w_plus][:3])
#
# plt.imshow(black_pawn_black_back)
# plt.show()
#
# imgf = Image.fromarray(black_pawn_black_back).resize((500, 500))
# imgf.save('own_illustrations/ww_Q.png')

#
# for img_name in os.listdir('own_illustrations'):
#     if img_name[0] == 'w':
#         print('Treating: ', img_name)
#         img = np.array(Image.open(os.path.join('own_illustrations', img_name)))
#         for i in range(img.shape[0]):
#             for j in range(img.shape[1]):
#                 if np.sum(img[i][j]==np.array([102, 204, 102])) == 3:
#                     img[i][j][0] = 51
#                     img[i][j][1] = 153
#                     img[i][j][2] = 51
#         Image.fromarray(img).save(('own_illustrations/' + 'down_'+img_name))
#     if img_name[0] == 'b':
#         print('Treating: ', img_name)
#         img = np.array(Image.open(os.path.join('own_illustrations', img_name)))
#         for i in range(img.shape[0]):
#             for j in range(img.shape[1]):
#                 if np.sum(img[i][j]==np.array([102, 102, 204])) == 3:
#                     img[i][j][0] = 51
#                     img[i][j][1] = 51
#                     img[i][j][2] = 153
#         Image.fromarray(img).save(('own_illustrations/' + 'down_'+img_name))
