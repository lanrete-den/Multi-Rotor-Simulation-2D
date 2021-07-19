from utilities import meter_to_pixel,pixel_to_meter

class Pose:

    def __init__(self,_ui):
        self.__x = 0
        self.__z = 0
        self.__a = 0
        self.ui = _ui


    def get_a(self):
        return self.__a

    def get_pose(self):
        return (self.__x, self.__z)

    def set_pose(self, x, z, a):
        self.__x = x
        self.__z = z
        self.__a = a

    def to_pixel(self):
        return meter_to_pixel(self.__x,self.__z,self.ui.width(),self.ui.height(),self.ui.autopilot.quadrotor.dronePix.height())

    @classmethod
    def pixel_scale(_cls_, val):
        return val * 100

