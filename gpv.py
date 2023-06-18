import json

class GPV:
    def __init__(self, hora_mbd, hora_gp, hora_drg, puesto, racha):
        self.hora_mbd = hora_mbd
        self.hora_gp = hora_gp
        self.hora_drg = hora_drg
        self.puesto = puesto
        self.racha = racha
    
    def get_tiempo_respuesta_points(self):
        pass
    def get_puesto_points(self):
        pass
    def get_racha_points(self):
        pass

    def get_mbd_difficulty(self):
        pass

    def get_gpv(self):
        points = self.get_tiempo_respuesta_points + self.get_puesto_points + self.get_racha_points()
        gpv = self.get_mbd_difficulty * points

        return gpv
    

def calculate_gpv():
    pass
    

if __name__ == "__main__":
    print(calculate_gpv())
