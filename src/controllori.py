# controllori.py

import math

class P_Controller:

    def __init__(self, kp):
        self.kp = kp

    def evaluate(self, u):
        return self.kp*u


class P_SAT_Controller:

    def __init__(self, kp, _max):
        self.kp = kp
        self._max = _max

    def evaluate(self, u):
        output = self.kp*u
        if output > self._max:
            output = self._max
        elif output < - self._max:
            output = -self._max
        return output


class PI_Controller:

    def __init__(self, kp, ki):
        self.kp = kp
        self.ki = ki
        self.integral_term = 0

    def evaluate(self, u, delta_t):
        self.integral_term = self.integral_term + u * delta_t
        return self.kp * u + self.ki * self.integral_term


class PI_SAT_Controller:

    def __init__(self, kp, ki, sat):
        self.kp = kp
        self.ki = ki
        self.saturation = sat
        self.integral_term = 0
        self.saturation_flag = False

    def evaluate(self, u, delta_t):
        if not(self.saturation_flag):
            self.integral_term = self.integral_term + u * delta_t

        output = self.kp * u + self.ki * self.integral_term

        if output > self.saturation:
            self.saturation_flag = True
            output = self.saturation
        elif output < - self.saturation:
            self.saturation_flag = True
            output = -self.saturation
        else:
            self.saturation_flag = False
        return output

class PID_SAT_Controller:

    def __init__(self, kp, ki, kd, sat):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.saturation = sat
        self.integral = 0
        self.prev_error = 0
        self.saturation_flag = False

    def evaluate(self, u, delta_t):
        error = u
        if not(self.saturation_flag):
            self.integral = self.integral + error * delta_t
        deriv = (error - self.prev_error) / delta_t
        self.prev_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * deriv
        if output > self.saturation:
            output = self.saturation
            self.saturation_flag = True
        elif output < -self.saturation:
            output = -self.saturation
            self.saturation_flag = True
        else:
            self.saturation_flag = False
        return output



class ProfilePositionController:

    def __init__(self, max_speed, accel, decel):
        self.__accel = accel
        self.__max_speed = max_speed
        self.__decel = decel
        self.__decel_distance = max_speed * max_speed / (2.0 * decel)
        self.__output_speed = 0 # la velocita' a cui andremo

    def evaluate(self, target_position, current_position,\
			current_speed, delta_t):
        distance = target_position - current_position

        # calcoliamo il segno e usiamo distanze sempre positive
        if distance >= 0:
            s = 1
        else:
            s = -1
            distance = -distance
        if distance < 0.01:
            return 0

        if distance < self.__decel_distance:
            # ok siamo nella fase di decelerazione
            vel_attesa = \
		math.sqrt(self.__max_speed * self.__max_speed - \
                          2 * self.__decel * \
			(self.__decel_distance - distance))
            if vel_attesa > self.__output_speed:
                # uhm... strana condizione,
                # vuol dire che siamo ancora in accelerazione (fase 1)
                # continuiamo ad accelerare
                self.__output_speed += self.__accel * delta_t
                # controlliamo se abbiamo comunque raggiunto
		# (e superato) la velocita' attesa
                if self.__output_speed > vel_attesa:
                    self.__output_speed = vel_attesa
                # evitiamo anche di superare la velocita' massima
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed
            else:
                # qui siamo effettivamente in decelerazione
                self.__output_speed = vel_attesa

        else:
            # non siamo nella fase di decelerazione quindi...
            if self.__output_speed < self.__max_speed:
                # se non siamo gia' a velocita' massima, acceleriamo
                self.__output_speed += self.__accel * delta_t
                # ma evitiamo sempre di superare la velocita' massima
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed

        # applichiamo il segno
        return s * self.__output_speed


