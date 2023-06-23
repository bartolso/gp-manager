'''

GP-MANAGER
El código da puto asco, es un puto mess que sinceramente no sé ordenar
así que si alguien que sepa de verdad le echa un ojo quizá se vomita encima
Advertencia hecha...

QUERESERES
TODO: añadir label con la dificultad día en la vista general
TODO: recuento de notas mensual
TODO: arreglar el conectarse al servidor que no sea una mierda vaya

HAY NO SE QUE PROBLEMA EN GPV.PY EL D1 NO SE ESTÁ CALCULANDO BIEN HAY QUE MIRARLO URGENTE

'''
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QDate, QThread, pyqtSignal
from PyQt6 import uic
from datetime import datetime, timedelta
import qdarktheme
import mysql.connector
import configparser
import queries
import sys

import gpscripts.gp, gpscripts.mbd, gpscripts.drg, gpscripts.config
from gpv import GPV

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.read_ini()
        self.logs = []
        self.current_date = datetime.today()
        self.lbl_current_date.setText(self.current_date.strftime('%d/%m/%Y'))

        #tabla seleccionada en vista general para poder seleccionarla luego en update db from table etc

        self.current_db_table = "gp"
    
        self.db_is_connected = False
        self.log_window_hidden = False

        self.btn_db_connect.clicked.connect(self.db_connect)

        self.btn_commit_mbd.clicked.connect(self.update_db_mbd)
        self.btn_commit_gp.clicked.connect(self.update_db_gp)
        self.btn_commit_drg.clicked.connect(self.update_db_drg)

        self.btn_gp_laura.clicked.connect(lambda: self.toggle_gp_valid("5"))
        self.btn_gp_anton.clicked.connect(lambda: self.toggle_gp_valid("4"))
        self.btn_gp_miranda.clicked.connect(lambda: self.toggle_gp_valid("3"))
        self.btn_gp_nerea.clicked.connect(lambda: self.toggle_gp_valid("9"))
        self.btn_gp_paula.clicked.connect(lambda: self.toggle_gp_valid("10"))
        self.btn_gp_joaquin.clicked.connect(lambda: self.toggle_gp_valid("1"))
        self.btn_gp_sergio.clicked.connect(lambda: self.toggle_gp_valid("2"))
        self.btn_gp_diego.clicked.connect(lambda: self.toggle_gp_valid("8"))
        self.btn_gp_aina.clicked.connect(lambda: self.toggle_gp_valid("7"))
        self.btn_gp_aitor.clicked.connect(lambda: self.toggle_gp_valid("6"))

        self.btn_show_gp_table.clicked.connect(self.show_gp_table)
        self.btn_show_mbd_table.clicked.connect(self.show_mbd_table)
        self.btn_show_drg_table.clicked.connect(self.show_drg_table)
        self.btn_show_faltas_table.clicked.connect(self.show_faltas_table)

        self.btn_move_back.clicked.connect(self.move_back)
        self.btn_move_forward.clicked.connect(self.move_forward)

        self.btn_run_query.clicked.connect(lambda: self.show_query(self.line_query.text()))

        self.chk_enable_gp_btn_colors.clicked.connect(self.toggle_config_gp_btn_colors)

        self.calendarWidget.clicked[QDate].connect(self.selected_date_in_calendar)

        #Añadir datos desde txt
        self.btn_preview_gp.clicked.connect(self.preview_txt_gp)
        self.btn_preview_mbd.clicked.connect(self.preview_txt_mbd)
        self.btn_preview_drg.clicked.connect(self.preview_txt_drg)

        self.btn_calculate_gpv.clicked.connect(self.calculate_gpv_manual)

        self.btn_previsualizar_gpvs.clicked.connect(self.gpv_preview)
        self.btn_commit_gpvs.clicked.connect(self.gpv_commit)

        # ya no existe...
        #self.btn_toggle_console.clicked.connect(self.toggle_console)

        self.btn_show_current_mbd.clicked.connect(self.show_current_mbd)
        self.btn_show_current_drg.clicked.connect(self.show_current_drg)

        self.gb_tabla.setTitle("Tabla")
        self.tableWidget.cellChanged.connect(self.update_database_from_table)

        self.btn_update_ids.clicked.connect(self.update_table_ids)

        # PESTAÑA AÑADIR DATOS
        self.btn_ad_gp.clicked.connect(self.add_gp)
        self.btn_ad_mbd.clicked.connect(self.add_mbd)
        self.btn_ad_drg.clicked.connect(self.add_drg)
        self.btn_ad_falta.clicked.connect(self.add_falta)

        self.run_at_start()

    # PESTAÑA AÑADIR DATOS
    def add_gp(self):
        datetime = self.dt_ad_gp_datetime.dateTime()
        dt_date = datetime.toString("yyyy-MM-dd")
        dt_time = datetime.toString("hh:mm")
        player = self.get_player_id_from_name(self.le_ad_gp_jugador.text())
        message = self.le_ad_gp_mensaje.text()

        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO `gpdb`.`gp` (`persona_id`, `dia`, `hora`, `mensaje`) VALUES ('{player}', '{dt_date}', '{dt_time}', '{message}')")

        mydb.commit()
        self.log("G.P. añadido")
        
    def add_mbd(self):
        datetime = self.dt_ad_mbd_datetime.dateTime()
        dt_date = datetime.toString("yyyy-MM-dd")
        dt_time = datetime.toString("hh:mm")
        profeta = self.get_player_id_from_name(self.le_ad_mbd_profeta.text())
        message = self.le_ad_mbd_texto.text()

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO `gpdb`.`mbd` (`dia`, `hora`, `mensaje`, `persona_id`) VALUES (%s, %s, %s, %s);", (dt_date, dt_time, message, profeta))

        mydb.commit()
        self.log("M.B.D. añadido")

    def add_drg(self):
        datetime = self.dt_ad_drg_datetime.dateTime()
        dt_date = datetime.toString("yyyy-MM-dd")
        dt_time = datetime.toString("hh:mm")
        profeta = self.get_player_id_from_name(self.le_ad_drg_profeta.text())
        message = self.le_ad_drg_texto.text()

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO `gpdb`.`mbd` (`dia`, `hora`, `mensaje`, `persona_id`) VALUES (%s, %s, %s, %s);", (dt_date, dt_time, message, profeta))

        mydb.commit()
        self.log("Drg añadido")

    def add_falta(self):
        datetime = self.dt_ad_drg_datetime.dateTime()
        dt_date = datetime.toString("yyyy-MM-dd")
        dt_time = datetime.toString("hh:mm")
        player = self.get_player_id_from_name(self.le_ad_faltas_jugador.text())
        f_type = self.le_ad_faltas_tipo.text()
        f_motivo = self.le_ad_faltas_motivo.text()

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO `gpdb`.`faltas` (`dia`, `hora`, `persona_id`, `tipo`, `motivo`) VALUES (%s, %s, %s, %s, %s);", (dt_date, dt_time, player, f_type, f_motivo))
    
        mydb.commit()
        self.log("Falta añadida")
    def show_current_mbd(self):
        current_date_formatted = self.current_date.strftime('%Y-%m-%d')
        self.show_query(f"SELECT * FROM gpdb.mbd WHERE dia = '{current_date_formatted}'")
        self.gb_tabla.setTitle("M.B.D. día seleccionado")

    def show_current_drg(self):
        current_date_formatted = self.current_date.strftime('%Y-%m-%d')
        self.show_query(f"SELECT * FROM gpdb.drg WHERE dia = '{current_date_formatted}'")
        self.gb_tabla.setTitle("Drg día seleccionado")

    def show_gp_table(self):
        self.current_db_table = "gp"
        self.show_query("SELECT * FROM gpdb.gp")
        self.log("Mostrando tabla de G.P.")
        self.gb_tabla.setTitle("Todos los G.P.")

    def show_mbd_table(self):
        self.current_db_table = "mbd"
        self.show_query("SELECT * FROM gpdb.mbd")
        self.log("Mostrando tabla de M.B.D.")
        self.gb_tabla.setTitle("Todos los M.B.D.")

    def show_drg_table(self):
        self.current_db_table = "drg"
        self.show_query("SELECT * FROM gpdb.drg")
        self.log("Mostrando tabla de Drg")
        self.gb_tabla.setTitle("Todos los Drg")

    def show_faltas_table(self):
        self.current_db_table = "faltas"
        self.show_query("SELECT * FROM gpdb.faltas")
        self.log("Mostrando tabla de Faltas")
        self.gb_tabla.setTitle("Todas las faltas")
    
    def toggle_config_gp_btn_colors(self):
        print("test")
        if self.chk_enable_gp_btn_colors.isChecked():
            config.set('GP-MANAGER', 'display_gp_button_colors', 'True')
            self.log("Colores activados. El rendimiento va a ser pésimo...")
        else:
            config.set('GP-MANAGER', 'display_gp_button_colors', 'False')
            self.log("Colores desactivados")

            self.btn_gp_laura.setStyleSheet("")
            self.btn_gp_anton.setStyleSheet("")
            self.btn_gp_miranda.setStyleSheet("")
            self.btn_gp_nerea.setStyleSheet("")
            self.btn_gp_paula.setStyleSheet("")
            self.btn_gp_joaquin.setStyleSheet("")
            self.btn_gp_sergio.setStyleSheet("")
            self.btn_gp_diego.setStyleSheet("")
            self.btn_gp_aina.setStyleSheet("")
            self.btn_gp_aitor.setStyleSheet("")
            self.btn_gp_pablo.setStyleSheet("")
    
    def run_at_start(self):
        if config["DATABASE"]["auto_connect"] == "True":
            self.db_connect()

        if config["GP-MANAGER"]["run_initial_query"] == "True":
            self.show_query(queries.initial_query)

    def read_ini(self):
        global config
        config = configparser.ConfigParser()
        config.read("config.ini")

    def toggle_console(self):
        if self.log_window_hidden:
            self.log_window.setHidden(False)
            self.log_window_hidden = False
        else:
            self.log_window.setHidden(True)
            self.log_window_hidden = True

    def run_query(self, query, fetch="one"):
        mycursor = mydb.cursor()
        mycursor.execute(query)

        try:
            if fetch == "one":
                result = mycursor.fetchone()
                mydb.commit()
                return result
            if fetch == "all":
                result = mycursor.fetchall()
                mydb.commit()
                return result
        except Exception as e:
            self.log(e)
    
    def show_query(self, query):
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query)
            rows = mycursor.fetchall()

            column_names = [i[0] for i in mycursor.description]

            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(len(rows[0]))

            self.tableWidget.setHorizontalHeaderLabels(column_names)

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            try:
                self.tableWidget.show()
                #self.log(query)
            except:
                pass
        
        except Exception as e:
            self.log(str(e))    

    def log(self, text, pprint=True, save_to_log_file=True):
        self.logs.append(text + "\n")
        self.update()

        if pprint:
            print(text)

        if save_to_log_file:
            with open("log.txt", "a", encoding="utf-8") as log:
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log.write("[" + dt_string + "]" + " " + text + "\n")

    #Modificar base de datos desde la tabla
    def update_database_from_table(self, row, column):

        if self.chk_edit_table.isChecked():
            item = self.tableWidget.item(row, column)
            new_value = item.text()
            primary_key_item = self.tableWidget.item(row, 0)
            primary_key_value = primary_key_item.text()

            header_item = self.tableWidget.horizontalHeaderItem(column)
            column_name = header_item.text()

            table = self.current_db_table #gp, mbd, drg

            mycursor = mydb.cursor()
            self.log(f"UPDATE gpdb.{table} SET {column_name} = '{new_value}' WHERE {table}_id = {primary_key_value}")
            mycursor.execute(f"UPDATE gpdb.{table} SET {column_name} = '{new_value}' WHERE {table}_id = {primary_key_value}")
            mydb.commit()

            self.chk_edit_table.setChecked(False)
            self.update()
            self.log("Base de datos modificada " + "(" + column_name + ")")

    def update(self):
        #chequear base de datos
        if self.db_is_connected:
            self.lbl_db_status.setText("🟢 Conectado")
        else:
            self.lbl_db_status.setText("🔴 Desconectado")

        self.log_window.setText("".join(self.logs))
        self.log_window2.setText("".join(self.logs))
        self.log_window_notas.setText("".join(self.logs))
        self.log_window_anadir_datos.setText("".join(self.logs))
        self.log_window_ad.setText("".join(self.logs))

        self.lbl_current_date.setText(self.current_date.strftime('%d/%m/%Y'))

        scrollbar = self.log_window.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        scrollbar2 = self.log_window2.verticalScrollBar()
        scrollbar2.setValue(scrollbar.maximum())

        scrollbar_notas = self.log_window_notas.verticalScrollBar()
        scrollbar_notas.setValue(scrollbar.maximum())

        scrollbar_anadir_datos = self.log_window_anadir_datos.verticalScrollBar()
        scrollbar_anadir_datos.setValue(scrollbar.maximum())

        scrollbar_ad = self.log_window_ad.verticalScrollBar()
        scrollbar_ad.setValue(scrollbar.maximum())

        qdate_obj = QDate(self.current_date.year, self.current_date.month, self.current_date.day)
        self.calendarWidget.setSelectedDate(qdate_obj)

        current_date_formatted = self.current_date.strftime('%Y-%m-%d')

        try:
            self.lbl_mbd_info.setText("MBD: " + str(self.run_query(f"SELECT hora FROM gpdb.mbd WHERE dia = '{current_date_formatted}'")[0])[:-3])
            self.lbl_drg_info.setText("Drg: " + str(self.run_query(f"SELECT hora FROM gpdb.drg WHERE dia = '{current_date_formatted}'")[0])[:-3])
        except:
            pass
        # esto es seguramente el peor código escrito jamás en la historia. hay que arreglarlo urgentemente destruye totalmente el rendimiento
        if config["GP-MANAGER"]["display_gp_button_colors"] == "True":
            # ACTUALIZAR BOTONES GP
            current_date = self.current_date.strftime('%Y-%m-%d')

            #joaquin
            gp_id_joaquin = self.get_gp_id_by_player_and_date(1, current_date)
            if gp_id_joaquin:
                if len(gp_id_joaquin) == 1:
                    if self.is_this_gp_valid(gp_id_joaquin[0][0]) == True:
                        self.btn_gp_joaquin.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_joaquin[0][0]) == False:
                        self.btn_gp_joaquin.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_joaquin[0][0]) == "?":
                        self.btn_gp_joaquin.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_joaquin.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_joaquin.setStyleSheet("")

            #sergio
            gp_id_sergio = self.get_gp_id_by_player_and_date(2, current_date)
            if gp_id_sergio:
                if len(gp_id_sergio) == 1:
                    if self.is_this_gp_valid(gp_id_sergio[0][0]) == True:
                        self.btn_gp_sergio.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_sergio[0][0]) == False:
                        self.btn_gp_sergio.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_sergio[0][0]) == "?":
                        self.btn_gp_sergio.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_sergio.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_sergio.setStyleSheet("")

            #miranda
            gp_id_miranda = self.get_gp_id_by_player_and_date(3, current_date)
            if gp_id_miranda:
                if len(gp_id_miranda) == 1:
                    if self.is_this_gp_valid(gp_id_miranda[0][0]) == True:
                        self.btn_gp_miranda.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_miranda[0][0]) == False:
                        self.btn_gp_miranda.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_miranda[0][0]) == "?":
                        self.btn_gp_miranda.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_miranda.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_miranda.setStyleSheet("")

            #anton
            gp_id_anton = self.get_gp_id_by_player_and_date(4, current_date)
            if gp_id_anton:
                if len(gp_id_anton) == 1:
                    if self.is_this_gp_valid(gp_id_anton[0][0]) == True:
                        self.btn_gp_anton.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_anton[0][0]) == False:
                        self.btn_gp_anton.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_anton[0][0]) == "?":
                        self.btn_gp_anton.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_anton.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_anton.setStyleSheet("")

            #laura
            gp_id_laura = self.get_gp_id_by_player_and_date(5, current_date)
            if gp_id_laura:
                if len(gp_id_laura) == 1:
                    if self.is_this_gp_valid(gp_id_laura[0][0]) == True:
                        self.btn_gp_laura.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_laura[0][0]) == False:
                        self.btn_gp_laura.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_laura[0][0]) == "?":
                        self.btn_gp_laura.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_laura.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_laura.setStyleSheet("")

            #aitor
            gp_id_aitor = self.get_gp_id_by_player_and_date(6, current_date)
            if gp_id_aitor:
                if len(gp_id_aitor) == 1:
                    if self.is_this_gp_valid(gp_id_aitor[0][0]) == True:
                        self.btn_gp_aitor.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_aitor[0][0]) == False:
                        self.btn_gp_aitor.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_aitor[0][0]) == "?":
                        self.btn_gp_aitor.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_aitor.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_aitor.setStyleSheet("")

            #aina
            gp_id_aina = self.get_gp_id_by_player_and_date(7, current_date)
            if gp_id_aina:
                if len(gp_id_aina) == 1:
                    if self.is_this_gp_valid(gp_id_aina[0][0]) == True:
                        self.btn_gp_aina.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_aina[0][0]) == False:
                        self.btn_gp_aina.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_aina[0][0]) == "?":
                        self.btn_gp_aina.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_aina.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_aina.setStyleSheet("")

            #diego
            gp_id_diego = self.get_gp_id_by_player_and_date(8, current_date)
            if gp_id_diego:
                if len(gp_id_diego) == 1:
                    if self.is_this_gp_valid(gp_id_diego[0][0]) == True:
                        self.btn_gp_diego.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_diego[0][0]) == False:
                        self.btn_gp_diego.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_diego[0][0]) == "?":
                        self.btn_gp_diego.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_diego.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_diego.setStyleSheet("")

            #nerea
            gp_id_nerea = self.get_gp_id_by_player_and_date(9, current_date)
            if gp_id_nerea:
                if len(gp_id_nerea) == 1:
                    if self.is_this_gp_valid(gp_id_nerea[0][0]) == True:
                        self.btn_gp_nerea.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_nerea[0][0]) == False:
                        self.btn_gp_nerea.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_nerea[0][0]) == "?":
                        self.btn_gp_nerea.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_nerea.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_nerea.setStyleSheet("")

            #paula
            gp_id_paula = self.get_gp_id_by_player_and_date(10, current_date)
            if gp_id_paula:
                if len(gp_id_paula) == 1:
                    if self.is_this_gp_valid(gp_id_paula[0][0]) == True:
                        self.btn_gp_paula.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_paula[0][0]) == False:
                        self.btn_gp_paula.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_paula[0][0]) == "?":
                        self.btn_gp_paula.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_paula.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_paula.setStyleSheet("")

            #pablo
            gp_id_pablo = self.get_gp_id_by_player_and_date(11, current_date)
            if gp_id_pablo:
                if len(gp_id_pablo) == 1:
                    if self.is_this_gp_valid(gp_id_pablo[0][0]) == True:
                        self.btn_gp_pablo.setStyleSheet("background-color : green")
                    if self.is_this_gp_valid(gp_id_pablo[0][0]) == False:
                        self.btn_gp_pablo.setStyleSheet("background-color : red")
                    if self.is_this_gp_valid(gp_id_pablo[0][0]) == "?":
                        self.btn_gp_pablo.setStyleSheet("background-color : purple")
                else:
                    self.btn_gp_pablo.setStyleSheet("background-color : orange")
            else:
                self.btn_gp_pablo.setStyleSheet("")

    def db_full_update(self):
        # actualizar todo y rellenar ids.
        self.update_db_mbd
        self.update_db_gp

    def db_connect(self):
        if config["DATABASE"]["use_default"] == "True":
            host = config["DATABASE"]["host"]
            user = config["DATABASE"]["user"]
            password = config["DATABASE"]["password"]
        else:
            host = self.line_host.text()
            user = self.line_user.text()
            password = self.line_password.text()

        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )

            self.db_is_connected = True
            self.log("Base de datos conectada" + " (" + user + ", " + host + ")")
        except:
            self.db_is_connected = False
            self.log("No se ha podido conectar a la base de datos" + " (" + user + ", " + host + ")")

        self.update()

    def preview_txt_gp(self):
        if self.chk_adt_all_range.isChecked():
            data = gpscripts.gp.read_txt()
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            data = gpscripts.gp.read_txt(all_dates=False, start_date=start_date, end_date=end_date)

        data_string = '\n'.join([' '.join(t) for t in data])
        self.preview_window.setText(data_string)

    def preview_txt_mbd(self):
        if self.chk_adt_all_range.isChecked():
            data = gpscripts.mbd.read_txt(profeta=self.le_profeta_mbd.text())
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            data = gpscripts.mbd.read_txt(profeta=self.le_profeta_mbd.text(), all_dates=False, start_date=start_date, end_date=end_date)

        data_string = '\n'.join([' '.join(t) for t in data])
        self.preview_window.setText(data_string)

    def preview_txt_drg(self):
        if self.chk_adt_all_range.isChecked():
            data = gpscripts.drg.read_txt(profeta=self.le_profeta_drg.text())
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            data = gpscripts.drg.read_txt(profeta=self.le_profeta_drg.text(), all_dates=False, start_date=start_date, end_date=end_date)

        data_string = '\n'.join([' '.join(t) for t in data])
        self.preview_window.setText(data_string)

    def get_player_id_from_name(self, player):
        if player == "Joaquin":
            return 1
        if player == "Sergio":
            return 2
        if player == "Miranda":
            return 3
        if player == "Anton":
            return 4
        if player == "Laura":
            return 5
        if player == "Aitor":
            return 6
        if player == "Aina":
            return 7
        if player == "Diego":
            return 8
        if player == "Nerea":
            return 9
        if player == "Paula":
            return 10
        if player == "Pablo":
            return 11

    def update_db_gp(self):
        if self.chk_adt_all_range.isChecked():
            gp_messages = gpscripts.gp.read_txt()
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            gp_messages = gpscripts.gp.read_txt(all_dates=False, start_date=start_date, end_date=end_date)

        for message in gp_messages:
            date_and_time = message[0].split(", ")

            msg_date = date_and_time[0]
            msg_time = date_and_time[1]
            msg_player = message[1] 
            
            # horrible
            msg_player = self.get_player_id_from_name(msg_player)

            msg_message = message[2]

            date_obj = datetime.strptime(msg_date, '%d/%m/%y')
            msg_date = date_obj.strftime('%Y-%m-%d')

            if self.db_is_connected:
                try:
                    mycursor = mydb.cursor()
                    mycursor.execute(f"INSERT INTO `gpdb`.`gp` (`persona_id`, `dia`, `hora`, `mensaje`) VALUES ('{msg_player}', '{msg_date}', '{msg_time}', '{msg_message}')")
                    mydb.commit()
                except Exception as e:
                    self.log(str(e))
            else:
                self.log("ERROR: Base de datos no conectada")
                break
            
            # ACTUALIZAR IDs - id del mbd correspondiente al gp
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE `gpdb`.`gp` JOIN `gpdb`.`mbd` ON `gpdb`.`gp`.dia = `gpdb`.`mbd`.dia SET `gpdb`.`gp`.mbd_id = `gpdb`.`mbd`.mbd_id")
            mydb.commit()
            self.update()
            
        self.log("Finalizado")
        
    def update_db_mbd(self):
        if self.chk_adt_all_range.isChecked():
            mbd_messages = gpscripts.mbd.read_txt(profeta=self.le_profeta_mbd.text())
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            mbd_messages = gpscripts.mbd.read_txt(profeta=self.le_profeta_mbd.text(), all_dates=False, start_date=start_date, end_date=end_date)

        for message in mbd_messages:
            date_and_time = message[0].split(", ")

            msg_date = date_and_time[0]
            msg_time = date_and_time[1]
            msg_player = message[1] # el profeta EN NOMBRE, NO ID
            msg_player = self.get_player_id_from_name(msg_player)
            msg_message = message[2]

            date_obj = datetime.strptime(msg_date, '%d/%m/%y')
            msg_date = date_obj.strftime('%Y-%m-%d')

            self.log(msg_message)

            if self.db_is_connected:
                try:
                    mycursor = mydb.cursor()
                    # jugador_id es el profeta. en la base de datos tanto profeta como jugador se consideran jugador
                    mycursor.execute("INSERT INTO `gpdb`.`mbd` (`dia`, `hora`, `mensaje`, `persona_id`) VALUES (%s, %s, %s, %s);", (msg_date, msg_time, msg_message, msg_player))
                    mydb.commit()
                except Exception as e:
                    print(e)
            else:
                self.log("ERROR: Base de datos no conectada")

            
            # ACTUALIZAR IDs
            mycursor = mydb.cursor()
            mycursor.nextset()
            mycursor.execute("UPDATE `gpdb`.`mbd` JOIN `gpdb`.`drg` ON `gpdb`.`mbd`.dia = `gpdb`.`drg`.dia SET `gpdb`.`mbd`.drg_id = `gpdb`.`drg`.drg_id")
            mydb.commit()

        self.log("Finalizado")

    def update_db_drg(self):
        if self.chk_adt_all_range.isChecked():
            drg_messages = gpscripts.drg.read_txt(profeta=self.le_profeta_drg.text())
        else:
            # rangos
            start_date = self.de_adt_start_date.date().toString("yy/M/d")
            end_date = self.de_adt_end_date.date().toString("yy/M/d")

            drg_messages = gpscripts.drg.read_txt(profeta=self.le_profeta_drg.text(), all_dates=False, start_date=start_date, end_date=end_date)

        for message in drg_messages:
            date_and_time = message[0].split(", ")

            msg_date = date_and_time[0]
            msg_time = date_and_time[1]
            msg_player = message[1] #jugador en nombre no en numerito
            msg_player = self.get_player_id_from_name(msg_player) #convertido a ID
            msg_message = message[2]

            date_obj = datetime.strptime(msg_date, '%d/%m/%y')
            msg_date = date_obj.strftime('%Y-%m-%d')

            self.log(msg_message)

            
            if self.db_is_connected:
                try:
                    mycursor = mydb.cursor()
                    mycursor.nextset()
                    mycursor.execute("INSERT INTO `gpdb`.`drg` (`dia`, `hora`, `mensaje`, `persona_id`) VALUES (%s, %s, %s, %s);", (msg_date, msg_time, msg_message, msg_player))
                    mydb.commit()
                except Exception as e:
                    print(e)   
            else:
                self.log("ERROR: Base de datos no conectada")

            # ACTUALIZAR IDs
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE `gpdb`.`drg` JOIN `gpdb`.`mbd` ON `gpdb`.`drg`.dia = `gpdb`.`mbd`.dia SET `gpdb`.`drg`.mbd_id = `gpdb`.`mbd`.mbd_id")
            mydb.commit()

            # ACTUALIZAR IDS DEL MBD!!!!!
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE `gpdb`.`mbd` JOIN `gpdb`.`drg` ON `gpdb`.`mbd`.dia = `gpdb`.`drg`.dia SET `gpdb`.`mbd`.drg_id = `gpdb`.`drg`.drg_id")
            mydb.commit()

        self.log("Finalizado")

    def update_table_ids(self):
        mycursor = mydb.cursor()
        # actualizar drg
        mycursor.execute("UPDATE `gpdb`.`drg` JOIN `gpdb`.`mbd` ON `gpdb`.`drg`.dia = `gpdb`.`mbd`.dia SET `gpdb`.`drg`.mbd_id = `gpdb`.`mbd`.mbd_id")
        self.log("drg actualizado")
        # actualizar mbd
        mycursor.execute("UPDATE `gpdb`.`mbd` JOIN `gpdb`.`drg` ON `gpdb`.`mbd`.dia = `gpdb`.`drg`.dia SET `gpdb`.`mbd`.drg_id = `gpdb`.`drg`.drg_id")
        self.log("mbd actualizado")
        # actualizar gp
        mycursor.execute("UPDATE `gpdb`.`gp` JOIN `gpdb`.`mbd` ON `gpdb`.`gp`.dia = `gpdb`.`mbd`.dia SET `gpdb`.`gp`.mbd_id = `gpdb`.`mbd`.mbd_id")
        self.log("gp actualizado")

    def move_back(self):
        current_db_table = "gp"
        self.current_date -= timedelta(days=1)
        self.move_table()
        self.update()

    def move_forward(self):
        current_db_table = "gp"
        self.current_date += timedelta(days=1)
        self.move_table()
        self.update()

    #Poner la tabla al dia seleccionado
    def move_table(self):
        current_db_table = "gp"
        if self.chk_move_table.isChecked():
            current_date = self.current_date.strftime('%Y-%m-%d')
            self.show_query("SELECT gpdb.gp.gp_id, personas.nombre, gpdb.gp.dia, gpdb.gp.hora, gpdb.gp.mbd_id, gpdb.gp.mensaje, gpdb.gp.valido, gpdb.gp.gpv, gpdb.gp.puesto, gpdb.gp.racha FROM gpdb.gp JOIN gpdb.personas ON gpdb.gp.persona_id = personas.persona_id WHERE DATE(gpdb.gp.dia) = '" + str(current_date) + "' ORDER BY gpdb.gp.gp_id ASC")
            self.update()

    def selected_date_in_calendar(self, date):
        current_db_table = "gp"
        date_str = date.toString('yyyy-MM-dd')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        self.current_date = date_obj
        self.move_table()
        self.update()
        self.gb_tabla.setTitle(f"G.P. del día seleccionado")

    def get_gp_id_by_player_and_date(self, jugador_id, date):
        query = "SELECT gpdb.gp.gp_id FROM gpdb.gp WHERE gpdb.gp.persona_id =" + str(jugador_id) + " AND gpdb.gp.dia = '" + str(date) + "'"
        try:
            query_response = self.run_query(query, fetch="all")
            return query_response
        except:
            pass

    def is_this_gp_valid(self, gp_id):
        query = "SELECT gpdb.gp.valido FROM gpdb.gp WHERE gpdb.gp.gp_id =" + str(gp_id)
        try:
            query_response = self.run_query(query)
        except Exception as e:
            return False
        
        if  str(query_response[0]) == "None":
            return "?"
        if "Si" in str(query_response):
            #print("si")
            return True
        if "No" in str(query_response):
            #print("no")
            return False
        else:
            print("else")
            return False

    def toggle_gp_valid(self, player_id):
        current_date = self.current_date.strftime('%Y-%m-%d')
        query = "SELECT gpdb.gp.valido FROM gpdb.gp WHERE gpdb.gp.dia = '" + current_date + "' AND gpdb.gp.persona_id = " + player_id

        query_response = self.run_query(query)
        
        #buscar gp_id dando el player_id
        try:
            gp_id = self.run_query("SELECT gp_id FROM gpdb.gp WHERE gpdb.gp.dia = '" + current_date + "' AND gpdb.gp.persona_id = " + player_id)[0]

            if "Si" in str(query_response):
                self.run_query("UPDATE gpdb.gp SET gpdb.gp.valido='No' WHERE gpdb.gp.gp_id=" + str(gp_id))
            if "No" in str(query_response):
                self.run_query("UPDATE gpdb.gp SET gpdb.gp.valido='Si' WHERE gpdb.gp.gp_id=" + str(gp_id))
            if "None" in str(query_response):
                self.run_query("UPDATE gpdb.gp SET gpdb.gp.valido='Si' WHERE gpdb.gp.gp_id=" + str(gp_id))

        except TypeError as e:
            #self.log(str(e))
            self.log("Estás intentando validar un GP no existente. Puedes crear un G.P. en la pestaña Añadir datos")

        self.move_table()
        self.update()

    def calculate_gpv_manual(self):
        gp_time = self.te_gp_time.time().toString("HH:mm")
        mbd_time = self.te_mbd_time.time().toString("HH:mm")
        drg_time = self.te_drg_time.time().toString("HH:mm")
        streak = self.sb_streak.value()
        rank = self.sb_rank.value()

        gpv = GPV(hora_mbd=mbd_time, hora_drg=drg_time, hora_gp=gp_time, racha=streak, puesto=rank)

        self.lbl_V1.setText("V1 Tiempo de respuesta: " + str(gpv.get_tiempo_respuesta_points()))
        self.lbl_V2.setText("V2 Puesto: " + str(gpv.get_puesto_points()))
        self.lbl_V3.setText("V3 Racha: " + str(gpv.get_racha_points()))
        self.lbl_D1.setText("D1 Dificultad tiempo M.B.D. - Drg: " + str(gpv.get_mbd_drg_difficulty()))
        self.lbl_D2.setText("D2 Dificultad hora M.B.D.: " + str(gpv.get_mbd_time_difficulty()))

        self.lbl_gpv_value.setText(str(gpv.get_gpv()))

    def get_gpvs(self, commit_to_db=False):
        #seleccionar los datos de los gps:
        start_date = self.de_gpv_start_date.date().toString("yyyy-MM-dd")
        end_date = self.de_gpv_end_date.date().toString("yyyy-MM-dd")

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM gpdb.gp WHERE gpdb.gp.dia BETWEEN '{start_date}' AND '{end_date}'")

        gps_ids = [row[0] for row in mycursor]
        self.log("GPs seleccionados: " + str(gps_ids))

        gpvs = []

        for gp_id in gps_ids:
            # hora del mbd
            mycursor.execute(f"SELECT mbd_id FROM gpdb.gp WHERE gp_id = {gp_id}")
            mbd_id = mycursor.fetchone()[0]
            mycursor.execute(f"SELECT hora FROM gpdb.mbd WHERE mbd_id = {mbd_id}")
            mbd_time = str(mycursor.fetchone()[0])[:-3]
            mycursor.nextset()

            # hora del gp
            mycursor.execute(f"SELECT hora FROM gpdb.gp WHERE gp_id = {gp_id}")
            gp_time = str(mycursor.fetchone()[0])[:-3]
            mycursor.nextset()
            
            # hora del drg
            mycursor.execute(f"SELECT hora FROM gpdb.drg WHERE mbd_id = {mbd_id}")
            try:
                drg_time = str(mycursor.fetchone()[0])[:-3]
                mycursor.nextset()
            except:
                # no hay drg
                drg_time = "23:59"
                mycursor.nextset()

            # puesto
            mycursor.execute(f"SELECT puesto FROM gpdb.gp WHERE gp_id = {gp_id}")
            rank = mycursor.fetchone()[0]
            mycursor.nextset()

            # racha
            mycursor.execute(f"SELECT racha FROM gpdb.gp WHERE gp_id = {gp_id}")
            streak = mycursor.fetchone()[0]
            mycursor.nextset()

            # CALCULAR GPV
            gpv = GPV(hora_mbd=mbd_time, hora_gp=gp_time, hora_drg=drg_time, puesto=rank, racha=streak)

            final_gpv = gpv.get_gpv()

            gpvs.append("ID: " + str(gp_id) + " GPV: " + str(final_gpv))

            if commit_to_db == True:
                mycursor.execute(f"UPDATE gpdb.gp SET gpv = '{final_gpv}' WHERE gp_id = '{gp_id}'")
                mydb.commit()
                mycursor.nextset()
            else:
                pass

        return gpvs
        
    def gpv_preview(self):
        gpvs = '\n'.join(self.get_gpvs())
        self.tb_preview_gpvs.setText(gpvs)

    def gpv_commit(self):
        self.get_gpvs(commit_to_db=True)
        self.log("GPVs cargados a la base de datos")

class TaskThread(QThread):
    finished = pyqtSignal()

    def run(self):

        self.finished.emit()
        
app = QApplication([])
#app.setStyle("Windows")
qdarktheme.setup_theme()
window = UI()
window.show()
app.exec()