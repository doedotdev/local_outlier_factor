import matplotlib.pyplot as plt
import lof


x = [0, 0, 1, 1, 4, 8, 9, 8, 9]
y = [0, 1, 1, 0, 0, 9, 8, 8, 9]
coords_as_x_and_y_array = [x, y]

test_lof = lof.LOF(coords_as_x_and_y_array, lof.LOF.CONST_MANHATTAN, 1)
lofs = test_lof.get_lof_sorted_filtered(True)
for l in lofs:
    print(str(l[0]) + ": " + str(l[1]))

plt.scatter(x, y)

plt.xlabel('x')
plt.ylabel('y')
plt.title('K Value Too Small')
plt.grid(True)
# plt.savefig("test.png")
plt.show()
