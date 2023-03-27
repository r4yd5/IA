
import psycopg2
from psycopg2 import Error
import datetime
from datetime import datetime, date
import time


def guardar_en_base(lista, primera_vez, hora_nueva, hora_anterior):
    try:


        connection = False

        wuser = "postgres"
        wpassword = "piojos"
        whost = "localhost"
        wport = "5432"
        wdatabase = "postgres"

        connection = psycopg2.connect(user=wuser, password=wpassword, host=whost, port=wport, database=wdatabase)

        cursor = connection.cursor()

        fecha = datetime.now().date()

        if primera_vez:
            try:
                cursor.execute("SELECT hora FROM takt_time_it26c where id_pasada = (select max(id_pasada) from takt_time_it26c);")
                hora_base = cursor.fetchall()[0][0]
                hora_anterior = hora_nueva

                hs_base = (hora_base.hour) * 3600
                minutos_base = (hora_base.minute) * 60
                segundos_base = (hora_base.second)

                hs_nueva = (hora_nueva.hour) * 3600
                minutos_nueva = (hora_nueva.minute) * 60
                segundos_nueva = (hora_nueva.second)

                s = (hs_nueva + minutos_nueva + segundos_nueva) - (hs_base + minutos_base + segundos_base)

                h = s // 3600
                s = s % 3600

                m = s // 60
                s = s % 60

                dif_pasada = str(h) + ':' + str(m) + ':' + str(s)
                hora_nueva = str(hora_nueva.hour) + ':' + str(hora_nueva.minute) + ':' + str(hora_nueva.second)



            except:
                hora_base = datetime(1, 1, 1, 0, 0)
                hora_anterior = hora_nueva

                hs_base = (hora_base.hour) * 3600
                minutos_base = (hora_base.minute) * 60
                segundos_base = (hora_base.second)

                hs_nueva = (hora_nueva.hour) * 3600
                minutos_nueva = (hora_nueva.minute) * 60
                segundos_nueva = (hora_nueva.second)

                dif_pasada = str(0) + ':' + str(0) + ':' + str(0)
                hora_nueva = str(hora_nueva.hour) + ':' + str(hora_nueva.minute) + ':' + str(hora_nueva.second)




        else:

            hs_anterior = (hora_anterior.hour) * 3600
            minutos_anterior = (hora_anterior.minute) * 60
            segundos_anterior = (hora_anterior.second)

            hs_nueva = (hora_nueva.hour) * 3600
            minutos_nueva = (hora_nueva.minute) * 60
            segundos_nueva = (hora_nueva.second)

            s = (hs_nueva + minutos_nueva + segundos_nueva) - (hs_anterior + minutos_anterior + segundos_anterior)

            h = s // 3600
            s = s % 3600

            m = s // 60
            s = s % 60

            hora_anterior = hora_nueva
            dif_pasada = str(h) + ':' + str(m) + ':' + str(s)
            hora_nueva = str(hora_nueva.hour) + ':' + str(hora_nueva.minute) + ':' + str(hora_nueva.second)


        cursor = connection.cursor()

        print(lista)
        cursor.execute((
                           'INSERT INTO "takt_time_it26c" (FECHA, HORA, DIF_PASADAS, CALLE_1, CALLE_2, CALLE_3, CALLE_4, CALLE_5, CALLE_6, CALLE_7, CALLE_8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                       (str(fecha), str(hora_nueva), str(dif_pasada), lista[0], lista[1],
                        lista[2], lista[3], lista[4], lista[5], lista[6],
                        lista[7]))

        connection.commit()

        connection.autocommit = True

    except (Exception, Error) as error:
        print(error)

    if (connection):
        cursor.close()
        connection.close()
        return hora_anterior




