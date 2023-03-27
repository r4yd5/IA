import time
import cv2
import pywinauto
import subprocess
from pyModbusTCP.server import ModbusServer
from detectar import detectar
from gui_errores import gui_errores
import os
from datetime import datetime
from datetime import time as timee

def alive(ramp):
    if ramp > 99:
        ramp = 0
        return ramp
    else:
        ramp += 1
        return ramp


print('----------------INICIANDO APLICACION CAMARA----------------')
subprocess.run('start microsoft.windows.camera:', shell=True)
desktop = pywinauto.Desktop(backend="uia")
cam = desktop['Camera']
try:
    cam.child_window(title="Cambiar al modo Foto", auto_id="CaptureButton_0", control_type="Button")
except:
    pass


search_dir = r"C:\Users\PC LASER\Pictures\Camera Roll/"
time.sleep(2)


contadores = {
    'calle0':[0,0,0,0,0,0,0,0,0,0],
    'calle1':[0,0,0,0,0,0,0,0,0,0],
    'calle2':[0,0,0,0,0,0,0,0,0,0],
    'calle3':[0,0,0,0,0,0,0,0,0,0],
    'calle4':[0,0,0,0,0,0,0,0,0,0],
    'calle5':[0,0,0,0,0,0,0,0,0,0],
    'calle6':[0,0,0,0,0,0,0,0,0,0],
    'calle7':[0,0,0,0,0,0,0,0,0,0]
    }

pasada = 0
nombre = 0
hora_anterior = hora_base = datetime(1, 1, 1, 0, 0)
primera_vez = True

if __name__ == '__main__':
    server = ModbusServer('172.31.80.91', 502,no_block=True)  # Declaro el servidor TCP/IP(dir_IP,nro_puerto, no_block para que el programa continue luego de iniciarlo)
    proof = [0]
    ramp = 0
    try:  # Inicio el servidor
        server.start()
        state = [0]
        print("Server started: " + str(server.is_run))
        print('----------------PUEDE INICIAR LA MAQUINA----------------')
        while True:  # Inicio bucle para que quede a la espera de peticiones

            if ([0] != server.data_bank.get_holding_registers(1)):
                server.data_bank.set_holding_registers(8, [1])# Cuando el valor del registro 1 se cambie:

                cam.child_window(title="Tomar Foto", auto_id="CaptureButton_0", control_type="Button").click()
                time.sleep(1)

                os.chdir(search_dir)
                files = filter(os.path.isfile, os.listdir(search_dir))
                files = [os.path.join(search_dir, f) for f in files]  # add path to each file
                files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

                ruta = files[0]
                frame = cv2.imread(ruta)


                imgg, lista_calles, hora_anterior = detectar(frame, contadores, primera_vez, hora_anterior)

                primera_vez = False

                cv2.imshow('img', imgg)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if cv2.getWindowProperty('img', cv2.WND_PROP_VISIBLE) < 1:
                    break


                if files[1] == r'C:\Users\PC LASER\Pictures\Camera Roll/desktop.ini':
                    pass
                else:
                    os.remove(files[1])

                server.data_bank.set_holding_registers(0, [lista_calles])  # Saco una foto (detectar()), paso el array a binario (binarify()), escribo el valor binario en el registro (se transforma a int[base2]).
                # state = server.data_bank.get_holding_registers(1)  # Aviso que valor recibio [para debug, puede irse esto y lo que sigue
                # print("Detection has been asked: " + str(state))
                # server.data_bank.set_holding_registers(1, [0])#Pongo un 0 en el registro 1 para que vuelva a esperar un cambio.
                # state = server.data_bank.get_holding_registers(3)  # Establezco la variable state de nuevo en 0 para las comparaciones
                server.data_bank.set_holding_registers(8, [0])  # Pongo un 1 en el registro 2 para que vuelva a esperar un cambio.
            ramp = proof[0]
            server.data_bank.set_holding_registers(5, [alive(ramp)])
            proof = server.data_bank.get_holding_registers(5)

    except Exception as e:



        try:
            for remover in range(len(files)):
                os.remove(files[remover])
        except:
            pass
        cv2.destroyAllWindows()
        gui_error = gui_errores(error2=True)
        cv2.imshow('gui_error', gui_error)
        cv2.waitKey()

        print("Failed")
        print(e)

for remover in range(len(files)):
    os.remove(files[remover])

cv2.destroyAllWindows()
