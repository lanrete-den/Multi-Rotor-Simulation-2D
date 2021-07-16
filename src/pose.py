class Pose:

    x_center = 640
    z_center = 360

    def __init__(self):
        self.__x = 0
        self.__z = 0
        self.__a = 0

    def get_pose(self):
        return (self.__x, self.__z)

    def set_pose(self, x, z, a):
        self.__x = x
        self.__z = z
        self.__a = a

    def to_pixel(self):
        return (Pose.x_center + self.__x * 100, Pose.z_center - self.__z * 100)

    @classmethod
    def xz_to_pixel(_cls_, x, z):
        return (Pose.x_center + x * 100, Pose.z_center - z * 100)

    @classmethod
    def pixel_scale(_cls_, val):
        return val * 100

