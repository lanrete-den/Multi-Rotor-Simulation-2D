class Pose:

    def __init__(self):
        self.__x = 0
        self.__z = 0
        self.__a = 0

    def get_a(self):
        return self.__a

    def get_pose(self):
        return (self.__x, self.__z)

    def set_pose(self, x, z, a):
        self.__x = x
        self.__z = z
        self.__a = a

    def to_pixel(self):
        return (self.__x * 100,self.__z * 100)

    @classmethod
    def xz_to_pixel(_cls_, x, z):
        return (x * 100, z * 100)

    @classmethod
    def pixel_scale(_cls_, val):
        return val * 100

