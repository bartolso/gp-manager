TEST = False

if TEST:
    import puntuaciones_test as puntuaciones
else:
    import puntuaciones

class GPV:
    def __init__(self, hora_mbd, hora_gp, hora_drg, puesto, racha):
        if __name__ == "__main__":
            self.hora_mbd = hora_mbd
            self.hora_gp = hora_gp
            self.hora_drg = hora_drg
        else:
            self.hora_mbd = hour_to_minutes(hora_mbd)
            self.hora_gp = hour_to_minutes(hora_gp)
            self.hora_drg = hour_to_minutes(hora_drg)
            
        self.puesto = puesto
        self.racha = racha

    def find_closest_value(self, my_value, values):
        closest_value = min(values, key=lambda x: abs(x - my_value))

        return closest_value
    
    def hour_to_minutes(hour):
        hour_parts = hour.split(":")
        hours = int(hour_parts[0])
        minutes = int(hour_parts[1])
        total_minutes = (hours * 60) + minutes
        return total_minutes
    
    def get_tiempo_respuesta_points(self):
        # hora mbd, hora gp
        response_time = self.hora_gp - self.hora_mbd

        indexes_list = list(puntuaciones.V1.keys())
        response_time_closest = self.find_closest_value(response_time, indexes_list)
        points = puntuaciones.V1[response_time_closest]

        return points * puntuaciones.mV1

    def get_puesto_points(self):
        # puesto
        puesto = self.puesto

        indexes_list = list(puntuaciones.V2.keys())
        puesto_closest = self.find_closest_value(puesto, indexes_list)
        points = puntuaciones.V2[puesto_closest]

        return points * puntuaciones.mV2

    def get_racha_points(self):
        # racha
        racha = self.racha

        indexes_list = list(puntuaciones.V3.keys())
        racha_closest = self.find_closest_value(racha, indexes_list)
        points = puntuaciones.V3[racha_closest]

        return points * puntuaciones.mV3

    def get_mbd_drg_difficulty(self):
        # hora_mbd, hora_drg

        legal_time = self.hora_drg - self.hora_mbd

        print("legal time " + str(legal_time))
        indexes_list = list(puntuaciones.D1.keys())
        mbd_drg_difficulty_closest = self.find_closest_value(legal_time, indexes_list)
        points = puntuaciones.D1[mbd_drg_difficulty_closest]

        return points * puntuaciones.mD1
    
    def get_mbd_time_difficulty(self):
        # hora_mbd

        hora_mbd = self.hora_mbd

        indexes_list = list(puntuaciones.D2.keys())
        mbd_time_difficulty_closest = self.find_closest_value(hora_mbd, indexes_list)
        points = puntuaciones.D2[mbd_time_difficulty_closest]

        return points * puntuaciones.mD2

    def get_gpv(self):
        gpv = self.get_tiempo_respuesta_points() + self.get_puesto_points() + self.get_racha_points() + self.get_mbd_time_difficulty() + self.get_mbd_drg_difficulty()

        return gpv
    
def hour_to_minutes(hour):
    hour_parts = hour.split(":")
    hours = int(hour_parts[0])
    minutes = int(hour_parts[1])
    total_minutes = (hours * 60) + minutes
    return total_minutes
    
def main():
    # VALORES
    hora_mbd_str = "8:00"
    hora_gp_str = "8:00"
    hora_drg_str = "9:00"
    puesto = 5
    racha = 10

    hora_mbd = hour_to_minutes(hora_mbd_str)
    hora_gp = hour_to_minutes(hora_gp_str)
    hora_drg = hour_to_minutes(hora_drg_str)

    gp = GPV(hora_mbd, hora_gp, hora_drg, puesto, racha)

    print("-----------------------")
    print("DATOS DEL GP")
    print()
    print("Hora del G.P.: " + str(hora_gp_str))
    print("Hora del M.B.D.: " + str(hora_mbd_str))
    print("Hora del Drg: " + str(hora_drg_str))
    print("Puesto: " + str(puesto))
    print("Racha: " + str(racha))
    print("-----------------------")
    print("PUNTOS")
    print()
    print("V1 Tiempo de respuesta: " + str(gp.get_tiempo_respuesta_points()) + " (x" + str(puntuaciones.mV1) + ")")
    print("V2 Puesto: " + str(gp.get_puesto_points()) + " (x" + str(puntuaciones.mV2) + ")")
    print("V3 Racha: " + str(gp.get_racha_points()) + " (x" + str(puntuaciones.mV3) + ")")
    print("D1 Tiempo entre M.B.D. y Drg: " + str(gp.get_mbd_drg_difficulty()) + " (x" + str(puntuaciones.mD1) + ")")
    print("D2 Hora del M.B.D.: " + str(gp.get_mbd_time_difficulty()) + " (x" + str(puntuaciones.mD2) + ")")
    print("-----------------------")
    print("GPV: " + str(gp.get_gpv()))
    print("-----------------------")

if __name__ == '__main__':
    main()