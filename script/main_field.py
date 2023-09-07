import time

from algorythm import Field
SIZE = 10
MAX_ITERS = 10000
START = (1, 1)
END = (99, 99)


def mainn():
    stat_time = time.time()
    field = Field(MAX_ITERS, START, END)

    print("Size:", field.size, 'x', field.size)
    field.get_barriers(1)
    field.find_distances()
    field.field_potential_fill()
    way = field.find_way()
    #
    # # print("Time of work:", round((time.time() - stat_time), 2), 's')
    # field.show_2d_capability(True)
    field.show_3d_capability(way)



if __name__ == '__main__':
    main()
