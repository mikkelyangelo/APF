from math import exp, sqrt
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from cell import Cell

#параметризация

k_res = 50000
k_att = 5
radius = 50
n = 20
step = 1
dstep = 50
dynamic_on = False
ax3d_on = True
list_of_obs = {str(i): [random.randint(0, 99) for _ in range(2)] for i in range(n)}
# list_of_obs = {1: (5, 50), 2: (80, 12), 3: (40, 50), 4: (60, 35), 5: (35, 35), 6: (56, 75), 7: (73, 72)}

step_2 = 1


class Field:

    def __init__(self, iters=2000, start=(1/step_2, 1/step_2), end=(99/step_2, 99/step_2)):
        self.size = 100
        self.start = self._prepare_start_end(start)
        self.end = self._prepare_start_end(end)
        self.iters = iters
        self.step = 100.0 / self.size
        self.field = np.zeros((self.size, self.size), dtype=Cell)
        self._fill_field()
        self.start_ = start
        self.end_ = end

    def _prepare_start_end(self, obj):
        """Преобразование координат """

        return int(obj[0]), int(abs(self.size - obj[1]))

    # заполняется поле нулями потом обьектами типа Cell.

    def _fill_field(self):
        for y in range(self.size):
            for x in range(self.size):
                self.field[y][x] = Cell(x, y, self.end)

    def get_barriers(self, i):
        # if i % 2 == 0: #динамика препятствия
        #     if i <= 35:
        #         list_of_obs[5] = (35 - i, 35 - i)
        #     if i <= 100:
        #         list_of_obs[1] = (1 + i, 50 - i)
        for obs in list_of_obs.keys():
            x = int(list_of_obs[obs][0])
            y = int(list_of_obs[obs][1])
            self.field[self.size - y - 1][x].is_polygon = 1

    def find_distances(self):

        points_list = {}
        for i in list_of_obs.keys():
            x = list_of_obs[i][0]
            y = self.size - list_of_obs[i][1] - 1
            points_list[str(i)] = [x, y]

        for y in range(self.size):
            for x in range(self.size):
                # if self.field[y][x].is_polygon == 0:
                for obs in points_list.keys():
                    distances = {str((points_list[obs][0], points_list[obs][1])): sqrt(
                        (x - points_list[obs][0]) ** 2 + (y - points_list[obs][1]) ** 2)}
                    sorted_keys = sorted(distances, key=distances.get)
                    points = [eval(point) for point in sorted_keys[:2]]
                    self.field[y][x].distances.append(distances[str(points[0])])


    def field_potential_fill(self):

        # Рассчет сил притяжения для каждой точки
        for y in range(self.size):
            for x in range(self.size):
                cell = self.field[y][x]
                # if cell.is_polygon != 1:
                for distance in cell.distances:
                    if distance != 0:
                        cell.capability += 1 / 2 * k_res * pow(((1 / distance - 1 / radius)), 2)
                    else:
                        cell.capability += 1 / 2 * k_res * 1.2 * pow(((1 / (distance + 1) - 1 / radius)), 2)
                cell.capability += 1 / 2 * k_att * cell.evcl_distance ** 2

    def _get_neighbours(self, cell):
        """Получение соседей клетки."""

        x, y = cell.x, cell.y
        neighs = ((x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1), (x + 1, y + 1), (y - 1, y - 1))
        return tuple(self.field[xy[1]][xy[0]] for xy in neighs
                     if xy[0] in range(self.size) and xy[1] in range(self.size))

    def _find_min(arr):
        """Нахождение точки с минимальным 'потенциалом' из списка."""

        min_ = np.inf
        min_cell = np.inf
        # print(len(arr))
        for cell in arr:
            # print(cell)
            if cell.is_polygon != 1:
                # print((cell.x, cell.y), cell.capability, min_)
                if cell.capability == min_ and cell.evcl_distance < min_cell.evcl_distance or cell.capability < min_:
                    min_ = cell.capability
                    min_cell = cell

        return min_cell

    def find_way(self):
        start = self.field[self.start[1]][self.start[0]]
        way = {1: start}
        for i in range(1, self.iters):
            neighs = self._get_neighbours(way[i])
            min_m = np.inf
            quite = False
            for neigh in range(0, len(neighs) - 1):
                if self.field[neighs[neigh].y][neighs[neigh].x].capability < min_m:
                    min_m = self.field[neighs[neigh].y][neighs[neigh].x].capability
                    min_field = self.field[neighs[neigh].y][neighs[neigh].x]
                    if min_m == self.field[self.end[1] - 1][self.end[0]].capability:
                        # if i == 10:
                        quite = True
            way[i + 1] = min_field
            # # self.show_2d_capability(True)
            # self.show_3d_capability(way)
            # self.get_barriers(i)
            # self.find_distances()
            # self.field_potential_fill()
            if quite == True:
                break
        return way

    def show_2d_capability(self, is_d=False):

        z = np.zeros((self.size, self.size))

        for xi in range(self.size):
            for yi in range(self.size):
                if is_d:
                    z[xi][yi] = self.field[xi][yi].capability
                else:
                    z[xi][yi] = self.field[xi][yi].capability
                # self.field[xi][yi].reset()

        plt.imshow(z, cmap='inferno', vmin=np.min(z), vmax=np.max(z))  # np.max(z)
        plt.show()

    # def show_3d_capability(self, way, param):
    def show_3d_capability(self, way):
        # Creating dataset
        # frames = []
        x = np.arange(0, self.size).reshape(1, -1)
        # x = np.repeat(x/step - dstep, self.size, axis=0)
        x = np.repeat(x, self.size, axis=0)
        y = np.arange(0, self.size).reshape(1, -1)
        # y = np.repeat((self.size - y)/step - dstep, self.size, axis=0).T
        # y = np.repeat(y/step - dstep, self.size, axis=0).T
        y = np.repeat(y, self.size, axis=0).T
        z = np.zeros((self.size, self.size))
        x_1 = []
        y_1 = []
        z_1 = []
        for i in way.values():
            # i.x = i.x/step - dstep
            # # i.y = (self.size - i.y)/step - dstep
            # i.y = i.y/step - dstep
            x_1.append(i.x)
            y_1.append(i.y)
            z_1.append(i.capability)

        for xi in range(self.size):
            for yi in range(self.size):
                z[xi][yi] = self.field[xi][yi].capability
                self.field[xi][yi].reset()
        # z = self._normalize(z)

        cmap = LinearSegmentedColormap.from_list('red_blue', ['b', 'w', 'r'], 256)
        # surf = ax_3d.plot_surface(x, y, z, cmap = 'inferno', alpha = .8)
        # fig = plt.figure()
        # plot = [ax.plot_surface(x, y, z)]
        # frame_animation = ax.plot_surface(x, y, z)

        if ax3d_on:
            ax_3d = plt.axes(projection='3d')
            ax_3d.contour(x, y, z, 50)
            ax_3d.plot(x_1, y_1, z_1, color='red', linestyle='dashed')
        elif not ax3d_on:
            fig, ax = plt.subplots(1)
            im = ax.contour(x, y, z, 50)
            fig.colorbar(im)
            ax.plot(x_1, y_1,color='red')
        # frames.append([frame_animation])
        plt.show()
        new_obs = {}

        # for i in list_of_obs.keys():
        #     x = int(list_of_obs[i][0])/step - dstep
        #     y = (int(self.size - list_of_obs[i][1]))/step - dstep
        #     new_obs[i] = (x, y)
        # print(new_obs)
    @staticmethod
    def _normalize(field):
        """Нормализация данных для отображения на графике."""

        field -= np.min(field)
        field -= np.mean(field)
        field /= np.max(field)

        return field
