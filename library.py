import random
from math import log, fabs, sqrt, pow, exp
from mysql.connector import (connection)

g0 = 9.81


class Engine:
    name = None
    impulse_v = None
    impulse_sl = None
    thrust_v = None
    thrust_sl = None
    diameter = None
    length = None
    fuel = None
    density_f = None
    oxidiser = None
    density_o = None
    mix_ratio = None
    id = None

    def generate(self, id):
        self.load_engine(id)

    def load_engine(self, id):
        query = "SELECT name, impulse_v, impulse_sl, thrust_v, thrust_sl, diameter, length, fuel, density_f, oxidiser, density_o, mix_ratio FROM engine WHERE id = " + str(
            id)
        cnx = connection.MySQLConnection(user='root', password='root',
                                         host='127.0.0.1',
                                         database='engines')
        cursor = cnx.cursor()
        try:
            cursor.execute(query)
            for (
            name, impulse_v, impulse_sl, thrust_v, thrust_sl, diameter, length, fuel, density_f, oxidiser, density_o,
            mix_ratio) in cursor:
                self.name = name
                self.impulse_v = impulse_v
                self.impulse_sl = impulse_sl
                self.thrust_v = thrust_v
                self.thrust_sl = thrust_sl
                self.diameter = diameter
                self.length = length
                self.fuel = fuel
                self.density_f = density_f
                self.oxidiser = oxidiser
                self.density_o = density_o
                self.mix_ratio = mix_ratio


        finally:
            cursor.close()
            cnx.close()

    def count_engines(self):
        query = "SELECT COUNT(*) FROM engine"
        cnx = connection.MySQLConnection(user='root', password='root',
                                         host='127.0.0.1',
                                         database='engines')
        cursor = cnx.cursor()
        try:
            cursor.execute(query)
            for (count,) in cursor:
                return count

        finally:
            cursor.close()
            cnx.close()


class Rocket:
    stages = []
    payload = None
    index_tab = []

    def generate(self, p, stg, index_tab):
        self.payload = p
        self.generate_stages(stg, index_tab)

    def fill_index(self, index_tab):
        for i in range(0, 3):
            index_tab.append(None)

    def generate_stages(self, stg, index_tab):
        for i in range(0, stg):
            tmp_stage = Stage()
            tmp_stage.generate_engine(index_tab[i])
            self.stages.append(tmp_stage)

    def empty_mass(self):
        empty_mass = 0
        for i in range(0, len(self.stages)):
            empty_mass = empty_mass + self.stages[i].empty
        return empty_mass

    def fuel_mass(self):
        fuel_mass = 0
        for i in range(0, len(self.stages)):
            fuel_mass = fuel_mass + self.stages[i].fuel
        return fuel_mass

    def payload_ratio(self, stage_number):
        payload = self.payload.payload
        for i in range(stage_number + 1, len(self.stages)):
            payload += self.stages[i].mass()
        return payload / self.stages[stage_number].mass()

    def structural_ratio(self, stage_number):
        return self.stages[stage_number].empty / self.stages[stage_number].mass()

    def mass_ratio(self, stage_number):
        top = self.payload.payload + self.stages[stage_number].mass()
        bot = self.payload.payload + self.stages[stage_number].empty
        for i in range(stage_number + 1, len(self.stages)):
            top += self.stages[i].mass()
            bot += self.stages[i].mass()
        return top / bot

    def burnout_velocity(self):
        c1 = self.stages[0].engine1.impulse_v
        v_bo1 = c1 * log(self.mass_ratio(0)) - g0 * self.stages[0].fuel
        c2 = self.stages[1].engine1.impulse_v
        v_bo2 = c2 * log(self.mass_ratio(1)) - g0 * self.stages[1].fuel
        c3 = self.stages[2].engine1.impulse_v
        v_bo3 = c3 * log(self.mass_ratio(2)) - g0 * self.stages[2].fuel
        return v_bo1 + v_bo2 + v_bo3

    def h_max(self):
        c1 = self.stages[0].engine1.impulse_v()
        c2 = self.stages[1].engine1.impulse_v()
        c3 = self.stages[2].engine1.impulse_v()
        h1_max = c1 * (
                self.stages[0].mass() + self.stages[1].mass() + self.stages[2].mass()) / self.stages[
                     0].engine1.propellant_flow_rate * (
                         1 + log(1 / self.mass_ratio(0)) - self.mass_ratio(0)) + 0.5 * c1 ** 2 / g0 * (
                     log(1 / self.mass_ratio(0))) ** 2
        h2_max = c2 * (self.stages[1].mass() + self.stages[2].mass()) / self.stages[1].engine1.propellant_flow_rate * (
                1 + log(1 / self.mass_ratio(1)) - self.mass_ratio(1)) + 0.5 * c2 ** 2 / g0 * (
                     log(1 / self.mass_ratio(1))) ** 2
        h3_max = c3 * self.stages[2].mass() / self.stages[2].engine1.propellant_flow_rate * (
                1 + log(1 / self.mass_ratio(2)) - self.mass_ratio(2)) + 0.5 * c3 ** 2 / g0 * (
                     log(1 / self.mass_ratio(2))) ** 2

        return h1_max + h2_max + h3_max

    @staticmethod
    def generate_acceleration():
        return random.randint(1, 10) * g0

    def calculate_model(self, v0):
        k = 5
        c = []
        e = []
        n = []
        m = []
        me = []
        mp = []
        s = []
        load = []
        limit = 0
        for i in range(0, len(self.stages)):
            c.append(self.stages[i].engine1.impulse_v)
            e.append(0.05 * (3 + i))
            n.append(None)
            m.append(None)
            me.append(None)
            mp.append(None)
            s.append(None)
            load.append(None)
        load[len(self.stages) - 1] = self.payload.payload
        for i in range(0, len(self.stages)):
            if (1 / (c[i] / 1000)) > limit:
                limit = (1 / (c[i] / 1000))
        while True:
            value_kon = 0
            value = []
            for i in range(0, len(self.stages)):
                value.append(0)
            for i in range(0, len(self.stages)):
                value[i] = c[i] / 1000 * log(c[i] / 1000 * k - 1) - log(k) * c[i] / 1000 - c[i] / 1000 * log(
                    c[i] / 1000 * e[i])
            for i in range(0, len(self.stages)):
                value_kon = value_kon + value[i]
            if fabs(value_kon - v0) <= 0.01:
                break
            else:
                if value_kon > v0:
                    k = k - 0.5 * (k - limit)
                else:
                    k = k + 0.5 * (k - limit)
            if k < limit or k > 100000:
#                print("silniki za slabe")
                return False
        i = len(self.stages) - 1
        while i >= 0:
            n[i] = (c[i] / 1000 * k - 1) / (c[i] / 1000 * e[i] * k)
            m[i] = (n[i] - 1) / (1 - n[i] * e[i]) * load[i]
            if i >= 1:
                load[i - 1] = load[i] + m[i]
            me[i] = m[i] * e[i]
            mp[i] = m[i] - me[i]
            self.stages[i].empty = me[i]
            self.stages[i].fuel = mp[i]
            i = i - 1
#        print(k, "n = ", n[0], n[1], "masa rakiety = ",
#              self.stages[0].empty + self.stages[1].empty + self.stages[0].fuel + self.stages[1].fuel)
        return True

    def calculate_velocity(self, wydluzenie):
        drag = [[0. for x in range(18)] for y in range(102)]
        mi = 398600
        Rz = 6378
        R_low = 200
        R1 = Rz + R_low
        R2 = Rz + self.payload.orbit
        delta_1 = sqrt(mi / R1) * (sqrt((2 * R2) / (R1 + R2)) - 1)
        delta_2 = sqrt(mi / R2) * (1 - sqrt((2 * R1) / (R1 + R2)))
        delta_hohmann = delta_1 + delta_2
        gravity_loss = 1.4
        flight_control = 0.5
        if self.stages[0].empty == None:
            aerodynamic_loss = 0.20271
        else:
            flow_ratio = (self.stages[0].engine1.thrust_sl / 1000) / (self.stages[0].engine1.impulse_sl / 1000)
            work_time = self.stages[0].fuel / flow_ratio
            increment = work_time / 100
            for i in range(0, 100):
                if i == 0:
                    drag[i][0] = 0
                    drag[i][1] = self.empty_mass() + self.fuel_mass()
                    drag[i][2] = self.stages[0].engine1.impulse_sl * log(drag[0][1] / drag[i][1]) - 9.81 * drag[i][0]
                    drag[i][3] = 0
                    if drag[i][3] < 11000:
                        drag[i][4] = 15.04 - 0.00649 * drag[i][3]
                    else:
                        if 25000 >= drag[i][3] >= 11000:
                            drag[i][4] = -56.46
                        else:
                            drag[i][4] = -131.21 + 0.0029 * drag[i][3]
                    if drag[i][3] < 11000:
                        drag[i][5] = 101.29 * pow((drag[i][4] + 273.1) / 288.08, 5.256)
                    else:
                        if 25000 >= drag[i][3] >= 11000:
                            drag[i][5] = 22.65 * exp(1.73 - 0.000157 * drag[i][3])
                        else:
                            drag[i][5] = 2.488 * pow((drag[i][4] + 273.1) / 216.6, -11.388)
                    drag[i][6] = drag[i][5] / (0.2869 * (drag[i][4]))
                    drag[i][7] = drag[i][2] / sqrt(1.4 * 287 * (drag[i][4] + 273.1))
                    drag[i][8] = drag[i][6] * drag[i][2] * drag[i][2] / 2
                    drag[i][9] = 0
                    drag[i][10] = 0.5 * drag[i][9] * 1.414 * drag[i][6] * drag[i][2] * drag[i][2]
                    drag[i][11] = 0
                    drag[i][12] = 0
                    drag[i][13] = 0
                    drag[i][14] = 0

                else:
                    drag[i][0] = drag[i - 1][0] + increment
                    drag[i][1] = drag[i - 1][1] - flow_ratio * (drag[i][0] - drag[i - 1][0])
                    drag[i][2] = self.stages[0].engine1.impulse_sl * log(drag[0][1] / drag[i][1]) - 9.81 * drag[i][0]
                    drag[i][3] = drag[i - 1][3] + drag[i][2] * (drag[i][0] - drag[i - 1][0])
                    if drag[i][3] < 11000:
                        drag[i][4] = 15.04 - 0.00649 * drag[i][3]
                    else:
                        if 25000 >= drag[i][3] >= 11000:
                            drag[i][4] = -56.46
                        else:
                            drag[i][4] = -131.21 + 0.0029 * drag[i][3]
                    if drag[i][3] < 11000:
                        drag[i][5] = 101.29 * pow((drag[i][4] + 273.1) / 288.08, 5.256)
                    else:
                        if 25000 >= drag[i][3] >= 11000:
                            drag[i][5] = 22.65 * exp(1.73 - 0.000157 * drag[i][3])
                        else:
                            drag[i][5] = 2.488 * pow((drag[i][4] + 273.1) / 216.6, -11.388)
                    drag[i][6] = drag[i][5] / (0.2869 * (drag[i][4]))
                    drag[i][7] = drag[i][2] / sqrt(1.4 * 287 * (drag[i][4] + 273.1))
                    drag[i][8] = drag[i][6] * drag[i][2] * drag[i][2] / 2
                    drag[i][9] = 0.053 * 11.90 * pow(drag[i][7] / ((drag[i][8] / 47.8803)) * 21.42 * 3.28, 0.2)
                    drag[i][10] = 0.5 * drag[i][9] * 1.414 * drag[i][6] * drag[i][2] * drag[i][2]
                    if drag[i][3] < 40000:
                        drag[i][11] = drag[i][10] / drag[i][1] * (drag[i][0] - drag[i - 1][0])
                    else:
                        drag[i][11] = 0
                    drag[i][12] = 3.6 / (wydluzenie * (drag[i][7] - 1) + 3)
                    drag[i][13] = 0.5 * drag[i][12] * 1.414 * drag[i][6] * drag[i][2] * drag[i][2]
                    if drag[i][3] < 40000:
                        drag[i][14] = drag[i][13] / drag[i][1] * (drag[i][0] - drag[i - 1][0])
            suma = 0
            for i in range(0, 100):
                suma = suma + drag[i][11] + drag[i][14]
            aerodynamic_loss = suma
        ground_velocity = gravity_loss + flight_control + delta_hohmann + aerodynamic_loss
        v_leo200 = 7.784
        return v_leo200 + ground_velocity + delta_hohmann


class Stage:
    engine1 = None
    length = None
    empty = None
    fuel = None

    def mass(self):
        return self.empty + self.fuel

    def generate_engine(self, id):
        self.engine1 = Engine()
        self.engine1.load_engine(id)


class Payload:

    def __init__(self, payload, orbit):
        self.payload = payload
        self.orbit = orbit

