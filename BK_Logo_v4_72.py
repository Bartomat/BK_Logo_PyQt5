# coding=utf-8

# region    imports...

# Standard-Packages
import sys
import os
# PIP-Packages
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from qtrangeslider import QRangeSlider  # erscheint hier unbenutzt, weil ich den QRangeSlider mit exec benutze
import random as rnd
import math
from functools import partial  # erscheint hier unbenutzt, weil ich das mit exec benutze
import pprint
import ast
from docx import Document
from htmldocx import HtmlToDocx
# Meine Klassen
from class_paths import bkPaths

# endregion

# region   Globale Konstanten

ANZAHL_ELEMENTE: int = 11
# Goldener Schnitt Phi
PHI: float = (1 + math.sqrt(5)) / 2
# MY_ICON_POLSKA: str = 'ui_files/Polska.png'


# endregion


# noinspection PyUnresolvedReferences
class MeineGUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Designer-Mopped importieren
        self.ui = uic.loadUi(
                bkPaths.ui_file('layout_Logo_Editor_v4_53.ui'),
                self)
        self.setWindowIcon(QIcon(
                bkPaths.icon('Polska.png')
                ))
        self.setWindowTitle("Barteks Logo Editor v4.71")
        #
        # self.verticalLayout_farben.setAlignment( Qt.AlignTop )
        self.verticalLayout_LogoElemente.setAlignment(Qt.AlignTop)
        
        self.horizontalLayout_3.setAlignment(Qt.AlignTop)
        
        self.verticalLayout_3.setAlignment(Qt.AlignRight)
        # self.horizontalLayout_2.setAlignment(Qt.AlignJustify)
        self.bk_graphicsView.setRenderHint(QPainter.Antialiasing)
        self.my_scene = None
        # region   Logo-spezifische Parameter innerhalb dieser Klasse
        
        # Einstellungen für die Pfeile (Dict, welche Pfeile gemalt werden sollen)
        # Dieses Dict wird zu Laufzeit verändert
        self.wo_pfeile_dict: dict = {0 : False,  # B
                                     1 : False,  # B
                                     2 : False,  # B
                                     3 : False,  # B
                                     4 : False,  # B
                                     5 : False,  # B
                                     6 : False,  # B
                                     7 : False,  # B
                                     8 : False,  # B
                                     9 : False,  # B
                                     10: False,  # B
                                     11: False,  # B
                                     12: False,  # B
                                     13: True,  # B
                                     14: False,  # K
                                     15: True,  # K
                                     16: False,  # K
                                     17: False,  # K
                                     18: False,  # K
                                     19: True,  # K
                                     20: False,  # K
                                     21: False,  # K
                                     }
        # Das Dict bleibt unangetastet und das brauche ich, um alles zu resetten
        self.wo_pfeile_dict_original: dict = {
                0 : False,  # B
                1 : False,  # B
                2 : False,  # B
                3 : False,  # B
                4 : False,  # B
                5 : False,  # B
                6 : False,  # B
                7 : False,  # B
                8 : False,  # B
                9 : False,  # B
                10: False,  # B
                11: False,  # B
                12: False,  # B
                13: True,  # B
                14: False,  # K
                15: True,  # K
                16: False,  # K
                17: False,  # K
                18: False,  # K
                19: True,  # K
                20: False,  # K
                21: False,  # K
                }
        # endregion
        # region # GUI Elemente erstellen
        self.rangesliders_erstellen()
        
        # QMenus erstellen
        self.menu_info = QMenu("Info")
        self.menuLogo_load = QMenu("Logo laden")
        self.menuLogo_save = QMenu("Logo speichern")
        # endregion
        
        # region    Die ganzen QActions für die QMenus:
        self.act_Logo_Einstellungen_speichern = QAction(
                QIcon(
                        bkPaths.icon('Save_24x24.png')
                        ),
                "Alle Logo-Einstellungen speichern")
        self.act_Logo_Farben_speichern = QAction(
                QIcon(
                        bkPaths.icon('chromatic.png')
                        ),
                "Nur Logo-Farben speichern")
        self.act_Farben_als_Word_speichern_speichern = QAction(
                QIcon(
                        bkPaths.icon('SaveColors_as_docx.png')
                        ),
                "Farben in ein Word-Dokument speichern")
        self.act_Logo_als_Bild_speichern = QAction(
                QIcon(
                        bkPaths.icon('Picture_24x24.png')
                        ),
                "Logo als Bild speichern"
                )
        self.act_Ende = QAction(
                QIcon(
                        bkPaths.icon('logout.png')
                        ),
                "Beenden"
                )
        self.act_Logo_Einstellungen_laden = QAction(
                QIcon(
                        bkPaths.icon('Open_24x24.png')
                        ),
                "Alle Logo-Einstellungen laden"
                )
        self.act_Logo_Farben_laden = QAction(
                QIcon(
                        bkPaths.icon('Open_24x24_onlyColors.png')
                        ),
                "Nur die Farben des Logos laden")
        self.act_Info = QAction(
                QIcon(
                        bkPaths.icon('clipart150731.png')
                        ),
                "Info"
                )
        # Die Menus und Actions zusammenbasteln
        self.main_menu_erstellen()
        # endregion
        
        # region   Connect all the Widget-Signals with the corresponding Slots/Methods
        # und die Werte in den dazugehörigen Labels setzen
        self.button_ende.clicked.connect(self.btn_ende)
        self.button_neue_farben.clicked.connect(self.btn_neue_farben)
        self.button_reset.clicked.connect(self.btn_reset)
        
        self.slider_dicke.valueChanged.connect(self.slider_dicke_change)
        self.label_dicke_wert.setText(f"{self.slider_dicke.value()}")
        
        self.slider_laenge.valueChanged.connect(self.slider_laenge_change)
        self.label_laenge_wert.setText(f"{self.slider_laenge.value()}")
        
        self.slider_khoehe.valueChanged.connect(self.slider_khoehe_change)
        self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
        
        self.slider_pfeilspitzen_dicke.valueChanged.connect(self.slider_pfeilspitzen_dicke_change)
        self.label_pfeilspitzen_dicke_wert.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
        
        self.slider_pfeilspitzen_laenge.valueChanged.connect(self.slider_pfeilspitzen_laenge_change)
        self.label_pfeilspitzen_laenge_wert.setText(f"{self.slider_pfeilspitzen_laenge.value()}")
        
        self.slider_pfeilspitzen_hoehe.valueChanged.connect(self.slider_pfeilspitzen_hoehe_change)
        self.label_pfeilspitzen_hoehe_wert.setText(f"{self.slider_pfeilspitzen_hoehe.value()}")
        
        self.slider_abstand.valueChanged.connect(self.slider_abstand_change)
        self.label_abstand_wert.setText(f"{self.slider_abstand.value()}")
        #  logo_malen wenn die Cbx Beschriftung geändert wurde --> Keine Klammen!!!!
        
        self.checkBox_beschriftung.stateChanged.connect(self.checkBox_beschriftung_change)
        
        # region   Die Checkboxen mit exec verbinden und mit den Werten aus dem dict befüllen
        # Zuerst die Werte setzen, dann die Verbindung...sonst macht jedes setzen ein Signal und ich ordne das dict neu
        for nr in range(len(self.wo_pfeile_dict)):
            if self.wo_pfeile_dict[nr]:
                exec(f"self.checkBox_pfeil_{nr}.setChecked(True)")
            exec(f"self.checkBox_pfeil_{nr}.stateChanged.connect(self.cbx_pfeilspitzen_change)")
            # CBX-Texte nach dem Schema 1 (0), 1 (1), 2 (0), 2 (1), ... basteln
            if nr % 2 != 0:
                txt_1: str = f"{str(int((nr - 1) / 2))} ({str(0)})"
                txt_2: str = f"{str(int((nr - 1) / 2))} ({str(1)})"
                exec(f"self.checkBox_pfeil_{nr - 1}.setText('Pfeilspitze ' + '{txt_1}')")
                exec(f"self.checkBox_pfeil_{nr}.setText('Pfeilspitze ' + '{txt_2}')")
        # endregion
        # endregion
    
    # region   RangeSliders mit Anzeige-Labels basteln
    def rangesliders_erstellen(self):
        """Erstellt 3 Paare von Label und Range-Slider
        Namens-Konvention:
        rangeslider_{slider_code}
        label_slider_{slider_code}_werte
        """
        for slider_code in ['r', 'g', 'b']:
            exec(f"self.range_slider_{slider_code} = QRangeSlider(Qt.Horizontal)")
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            exec(f"sizePolicy.setHeightForWidth(self.range_slider_{slider_code}.sizePolicy().hasHeightForWidth())")
            exec(f"self.range_slider_{slider_code}.setSizePolicy(sizePolicy)")
            exec(f"self.range_slider_{slider_code}.setOrientation(Qt.Horizontal)")
            exec(f"self.range_slider_{slider_code}.setTickPosition(QSlider.TicksBelow)")
            exec(f"self.range_slider_{slider_code}.setTickInterval(5)")
            
            exec(f"self.range_slider_{slider_code}.setMinimum(0)")
            exec(f"self.range_slider_{slider_code}.setMaximum(255)")
            exec(f"self.range_slider_{slider_code}.setSliderPosition((0,255))")
            
            exec(f"self.range_slider_{slider_code}._setBarColor(QColor('black'))")
            exec(f"self.range_slider_{slider_code}.setBarIsRigid(False)")
            
            exec(f"self.range_slider_{slider_code}.sliderMoved.connect(self.rangeslider_{slider_code}_werte_change)")
            
            exec(f"self.label_slider_{slider_code}_werte = QLabel()")
            font = QFont()
            font.setFamily("Verdana")
            font.setPointSize(9)
            font.setStyleStrategy(QFont.PreferAntialias)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(255)
            sizePolicy.setVerticalStretch(255)
            exec(
                    f"sizePolicy.setHeightForWidth(self.label_slider_{slider_code}_werte.sizePolicy().hasHeightForWidth())")
            exec(f"self.label_slider_{slider_code}_werte.setFont(font)")
            exec(f"self.label_slider_{slider_code}_werte.setAlignment(Qt.AlignLeft)")
            exec(f"self.label_slider_{slider_code}_werte.setText('Farbgrenzen {slider_code}: (0, 255)')")
            
            # Den ganzen Kram (Slider + Label) in das vLayout packen
            exec(f"self.verticalLayout_farben.addWidget(self.label_slider_{slider_code}_werte)")
            exec(f"self.verticalLayout_farben.addWidget(self.range_slider_{slider_code})")
    
    # endregion
    
    def main_menu_erstellen(self):
        
        # Namen für die QSS-Kacke
        self.menuLogo_save.setAccessibleName("QSS_SAVE")
        self.menuLogo_load.setAccessibleName("QSS_LOAD")
        self.menu_info.setAccessibleName("QSS_INFO")
        
        # region    Die QActions zu den entsprechenden QMenus hinzufügen
        self.menuLogo_save.addAction(self.act_Logo_Einstellungen_speichern)
        self.menuLogo_save.addAction(self.act_Logo_Farben_speichern)
        self.menuLogo_save.addAction(self.act_Farben_als_Word_speichern_speichern)
        self.menuLogo_save.addSeparator()
        self.menuLogo_save.addAction(self.act_Logo_als_Bild_speichern)
        self.menuLogo_save.addSeparator()
        self.menuLogo_save.addAction(self.act_Ende)
        
        self.menuLogo_load.addAction(self.act_Logo_Einstellungen_laden)
        self.menuLogo_load.addAction(self.act_Logo_Farben_laden)
        self.menuLogo_load.addSeparator()
        
        self.menu_info.addAction(self.act_Info)
        self.menu_info.addSeparator()
        # endregion
        # region Die QMenus mit den QActions zur QMenuBar hinzufügen
        self.menubar_main.addAction(self.menuLogo_save.menuAction())
        self.menubar_main.addAction(self.menuLogo_load.menuAction())
        self.menubar_main.addAction(self.menu_info.menuAction())
        # endregion
        
        # QActions mit Methoden verbinden
        self.act_Ende.triggered.connect(self.btn_ende)
        self.act_Logo_Einstellungen_speichern.triggered.connect(self.logo_einstellungen_speichern)
        self.act_Logo_Einstellungen_laden.triggered.connect(self.logo_einstellungen_laden)
        self.act_Farben_als_Word_speichern_speichern.triggered.connect(self.farben_als_word_speichern)
        self.act_Logo_Farben_speichern.triggered.connect(self.logo_farben_speichern)
        self.act_Logo_Farben_laden.triggered.connect(self.logo_farben_laden)
        self.act_Logo_als_Bild_speichern.triggered.connect(self.logo_speichern)
        self.act_Info.triggered.connect(self.app_info)
    
    # region    Methoden zum Speichern und Laden des Logos
    def logo_einstellungen_speichern(self):
        filename = QFileDialog.getSaveFileName(caption="Alle Logo-Einstellungen speichern",
                                               directory="./My_Logo.bklogo",
                                               filter="BkLogo-File (*.bklogo)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            # region   RangeSliders Werte auslesen und in ein eigenes dict speichern
            rgb_values: dict = {}
            for slider_code in ['r', 'g', 'b']:
                exec(f"rgb_values['{slider_code}'] = self.range_slider_{slider_code}.value()")
            # endregion
            
            # region    elemente_dict_partial erstellen und mit aktuellen zValues und Colors füllen
            elemente_dict_partial: dict = {}
            # partielles elemente_dict mit den relevanten Werten vorab erstellen
            for xx in self.my_scene.elemente_dict:
                elemente_dict_partial[xx] = {
                        'color'      : None,
                        'color_flag' : True,
                        'zValue'     : 0,
                        'zValue_flag': True,
                        }
            #   elemente_dict_partial mit den aktuellen Werten befüllen
            for xx in self.my_scene.elemente_dict:
                elemente_dict_partial[xx]['color'] = self.my_scene.elemente_dict[xx]['color']
                elemente_dict_partial[xx]['color_flag'] = self.my_scene.elemente_dict[xx]['color_flag']
                elemente_dict_partial[xx]['zValue'] = self.my_scene.elemente_dict[xx]['zValue']
                elemente_dict_partial[xx]['zValue_flag'] = self.my_scene.elemente_dict[xx]['zValue_flag']
            
            # pprint.pprint(elemente_dict_partial, sort_dicts=False) #DEBUG
            # endregion
            
            # Das dict zum speichern zusammenbasteln
            
            dict_4_save: dict = {
                    'slider_dicke'              : self.slider_dicke.value(),
                    'slider_laenge'             : self.slider_laenge.value(),
                    'slider_pfeilspitzen_dicke' : self.slider_pfeilspitzen_dicke.value(),
                    'slider_pfeilspitzen_hoehe' : self.slider_pfeilspitzen_hoehe.value(),
                    'slider_pfeilspitzen_laenge': self.slider_pfeilspitzen_laenge.value(),
                    'slider_khoehe'             : self.slider_khoehe.value(),
                    'slider_abstand'            : self.slider_abstand.value(),
                    'rgb_values'                : rgb_values,
                    'wo_pfeile_dict'            : self.wo_pfeile_dict,
                    'checkBox_dicken_link'      : self.checkBox_dicken_link.isChecked(),
                    'checkBox_beschriftung'     : self.checkBox_beschriftung.isChecked(),
                    'elemente_dict_partial'     : elemente_dict_partial,
                    }
            
            # Dict mit pprint schön formatieren bevor es gespeichert wird
            formatted_dict: str = pprint.pformat(dict_4_save, sort_dicts=False)  # alphabetische sortierung dict raus
            # pprint.pprint(formatted_dict) # DEBUG
            with open(filename[0], 'w', encoding='utf-8') as savefile:
                savefile.write(formatted_dict)
    
    def logo_einstellungen_laden(self):
        filename = QFileDialog.getOpenFileName(caption="Alle Logo-Einstellungen laden",
                                               directory=".",
                                               filter="BkLogo-File (*.bklogo)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            with open(filename[0], 'r', encoding='utf-8') as readfile:
                my_txt = readfile.read()
            
            dict_4_update: dict = ast.literal_eval(my_txt)  # ast.literal_eval wegen SECURITY -> https://docs.python.org/3.10/library/ast.html#ast-helpers
            # pprint.pprint( dict_4_update, sort_dicts=False ) # DEBUG
            
            # Hier die Werte aller Widgets auf die Werte aus dem (neuen) Dict setzen
            
            # region   Alle 7 normalen Slider und deren Label auf die Werte aus dem (neuen) Dict setzen
            self.slider_dicke.blockSignals(True)
            self.slider_dicke.setProperty("value", dict_4_update['slider_dicke'])
            self.label_dicke_wert.setText(f"{self.slider_dicke.value()}")
            self.slider_dicke.blockSignals(False)
            
            self.slider_laenge.blockSignals(True)
            self.slider_laenge.setProperty("value", dict_4_update['slider_laenge'])
            self.label_laenge_wert.setText(f"{self.slider_laenge.value()}")
            self.slider_laenge.blockSignals(False)
            
            self.slider_pfeilspitzen_hoehe.blockSignals(True)
            self.slider_pfeilspitzen_hoehe.setProperty("value", dict_4_update['slider_pfeilspitzen_hoehe'])
            self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
            self.slider_pfeilspitzen_hoehe.blockSignals(False)
            
            self.slider_khoehe.blockSignals(True)
            self.slider_khoehe.setProperty("value", dict_4_update['slider_khoehe'])
            self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
            self.slider_khoehe.blockSignals(False)
            
            self.slider_pfeilspitzen_dicke.blockSignals(True)
            self.slider_pfeilspitzen_dicke.setProperty("value", dict_4_update['slider_pfeilspitzen_dicke'])
            self.label_pfeilspitzen_dicke_wert.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
            self.slider_pfeilspitzen_dicke.blockSignals(False)
            
            self.slider_pfeilspitzen_laenge.blockSignals(True)
            self.slider_pfeilspitzen_laenge.setProperty("value", dict_4_update['slider_pfeilspitzen_laenge'])
            self.label_pfeilspitzen_laenge_wert.setText(f"{self.slider_pfeilspitzen_laenge.value()}")
            self.slider_pfeilspitzen_laenge.blockSignals(False)
            
            self.slider_abstand.blockSignals(True)
            self.slider_abstand.setProperty("value", dict_4_update['slider_abstand'])
            self.label_abstand_wert.setText(f"{self.slider_abstand.value()}")
            self.slider_abstand.blockSignals(False)
            # endregion
            
            # region   RangeSliders Standardwerte setzen auch mit blockSignals(True)
            for slider_code in ['r', 'g', 'b']:
                exec(f"self.range_slider_{slider_code}.blockSignals( True )")
                
                exec(f"self.range_slider_{slider_code}.setSliderPosition({dict_4_update['rgb_values'][slider_code]})")
                # print(f"self.range_slider_{slider_code}.setSliderPosition({dict_4_update['rgb_values'][slider_code]})")  # DEBUG
                # print(f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen {slider_code}: {{self.range_slider_{slider_code}.value()}}' )")  # DEBUG
                exec(f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen {slider_code}: {{self.range_slider_{slider_code}.value()}}' )")
                
                exec(f"self.range_slider_{slider_code}.blockSignals( False )")
            # endregion
            
            # region   Checkboxen Pfeile auf die Werte aus der Datei setzen
            self.wo_pfeile_dict = dict_4_update['wo_pfeile_dict']
            
            for nr in range(len(self.wo_pfeile_dict)):
                if self.wo_pfeile_dict[nr]:
                    exec(f"self.checkBox_pfeil_{nr}.blockSignals( True )")
                    exec(f"self.checkBox_pfeil_{nr}.setChecked(True)")
                    exec(f"self.checkBox_pfeil_{nr}.blockSignals( False )")
                else:
                    exec(f"self.checkBox_pfeil_{nr}.blockSignals( True )")
                    exec(f"self.checkBox_pfeil_{nr}.setChecked(False)")
                    exec(f"self.checkBox_pfeil_{nr}.blockSignals( False )")
            # endregion
            
            # region   Cbx Beschriftung & Cbx Dicken setzen
            self.checkBox_beschriftung.blockSignals(True)
            self.checkBox_beschriftung.setChecked(dict_4_update['checkBox_beschriftung'])
            self.checkBox_beschriftung.blockSignals(False)
            
            # Cbx Dicken verknüpfen setzem
            self.checkBox_dicken_link.setChecked(dict_4_update['checkBox_dicken_link'])
            # endregion
            
            # region    Die Werte im elemente_dict mit den Werten aus elemente_dict_partial ersetzen
            # das relevante dict aus dem geladenen dict herausfischen, sodass es beim Loopen übersichtlicher ist
            elemente_dict_partial: dict = dict_4_update['elemente_dict_partial']
            # pprint.pprint(elemente_dict_partial, sort_dicts=False) # DEBUG
            for nr in self.my_scene.elemente_dict:
                self.my_scene.elemente_dict[nr]['color'] = elemente_dict_partial[nr]['color']
                self.my_scene.elemente_dict[nr]['color_flag'] = elemente_dict_partial[nr]['color_flag']
                self.my_scene.elemente_dict[nr]['zValue'] = elemente_dict_partial[nr]['zValue']
                self.my_scene.elemente_dict[nr]['zValue_flag'] = elemente_dict_partial[nr]['zValue_flag']
            # endregion

            self.my_scene.logo_malen(farben_neu=False)
            self.textEdit_farben.clear()
            self.textEdit_farben.setHtml(self.my_scene.textedit_fill())
    
    def logo_farben_speichern(self):
        filename = QFileDialog.getSaveFileName(caption="Nur die Logo-Farben speichern",
                                               directory="./My_Logo_Colours.bklogoc",
                                               filter="BkLogo-ColourFile (*.bklogoc)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            # region   RangeSliders Werte auslesen und in ein eigenes dict speichern
            rgb_values: dict = {}
            for slider_code in ['r', 'g', 'b']:
                exec(f"rgb_values['{slider_code}'] = self.range_slider_{slider_code}.value()")
            # endregion
            
            # region    elemente_dict_partial erstellen und mit aktuellen zValues und Colors füllen
            elemente_dict_partial: dict = {}
            # partielles elemente_dict mit den relevanten Werten vorab erstellen
            for xx in self.my_scene.elemente_dict:
                elemente_dict_partial[xx] = {
                        'color'     : None,
                        'color_flag': True,
                        # 'zValue'     : 0,
                        # 'zValue_flag': True,
                        }
            #   elemente_dict_partial mit den aktuellen Werten befüllen
            for xx in self.my_scene.elemente_dict:
                elemente_dict_partial[xx]['color'] = self.my_scene.elemente_dict[xx]['color']
                elemente_dict_partial[xx]['color_flag'] = True  # self.my_scene.elemente_dict[ xx ][ 'color_flag' ]
                # elemente_dict_partial[ xx ][ 'zValue' ] = self.my_scene.elemente_dict[ xx ][ 'zValue' ]
                # elemente_dict_partial[ xx ][ 'zValue_flag' ] = self.my_scene.elemente_dict[ xx ][ 'zValue_flag' ]
            
            # pprint.pprint(elemente_dict_partial, sort_dicts=False) #DEBUG
            # endregion
            
            # Das dict zum speichern zusammenbasteln
            
            dict_4_save: dict = {
                    'rgb_values'           : rgb_values,
                    'elemente_dict_partial': elemente_dict_partial,
                    }
            
            # Dict mit pprint schön formatieren bevor es gespeichert wird
            formatted_dict: str = pprint.pformat(dict_4_save, sort_dicts=False)  # alphabetische sortierung dict raus
            # pprint.pprint(formatted_dict) # DEBUG
            with open(filename[0], 'w', encoding='utf-8') as savefile:
                savefile.write(formatted_dict)
    
    def logo_farben_laden(self):
        filename = QFileDialog.getOpenFileName(caption="Nur die Logo-Farben laden",
                                               directory="./My_Logo_Colours.bklogoc",
                                               filter="BkLogo-ColourFile (*.bklogoc)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            with open(filename[0], 'r', encoding='utf-8') as readfile:
                my_txt = readfile.read()
            
            dict_4_update: dict = ast.literal_eval(my_txt)  # ast.literal_eval wegen SECURITY ->
            # https://docs.python.org/3.10/library/ast.html#ast-helpers
            # pprint.pprint( dict_4_update, sort_dicts=False ) # DEBUG
            
            # Hier die Werte aller Widgets auf die Werte aus dem (neuen) Dict setzen
            
            # region   RangeSliders Standardwerte setzen auch mit blockSignals(True)
            for slider_code in ['r', 'g', 'b']:
                exec(f"self.range_slider_{slider_code}.blockSignals( True )")
                
                exec(f"self.range_slider_{slider_code}.setSliderPosition("
                     f"{dict_4_update['rgb_values'][slider_code]})")
                # print(f"self.range_slider_{slider_code}.setSliderPos"
                #       f"ition({dict_4_update['rgb_values'][slider_code]})")  # DEBUG
                # print(f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen {slider_code}: {{"
                #       f"self.range_slider_{slider_code}.value()}}' )")  # DEBUG
                exec(f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen {slider_code}: {{"
                     f"self.range_slider_{slider_code}.value()}}' )")
                
                exec(f"self.range_slider_{slider_code}.blockSignals( False )")
            # endregion
            
            # region    Die Werte im elemente_dict mit den Werten aus elemente_dict_partial ersetzen
            # das relevante dict aus dem geladenen dict herausfischen, so dass es beim Loopen übersichtlicher ist
            elemente_dict_partial: dict = dict_4_update['elemente_dict_partial']
            # pprint.pprint(elemente_dict_partial, sort_dicts=False) # DEBUG
            for nr in self.my_scene.elemente_dict:
                self.my_scene.elemente_dict[nr]['color'] = elemente_dict_partial[nr]['color']
                self.my_scene.elemente_dict[nr]['color_flag'] = elemente_dict_partial[nr]['color_flag']
                # self.my_scene.elemente_dict[ nr ][ 'zValue' ] = elemente_dict_partial[ nr ][ 'zValue' ]
                # self.my_scene.elemente_dict[ nr ][ 'zValue_flag' ] = elemente_dict_partial[ nr ][ 'zValue_flag' ]
            # endregion

            self.my_scene.logo_malen(farben_neu=False)
            self.textEdit_farben.clear()
            self.textEdit_farben.setHtml(self.my_scene.textedit_fill())
    
    def farben_als_word_speichern(self):
        filename = QFileDialog.getSaveFileName(caption="Logo-Farben in einer Word-Datei speichern",
                                               directory="./My_Logo_Colors.docx",
                                               filter="Word-Document (*.docx)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            html_parser = HtmlToDocx()
            my_docx = Document()
            
            html_parser.add_html_to_document(self.textEdit_farben.toHtml(), my_docx)
            my_docx.save(filename[0])
    
    def logo_speichern(self):
        filename = QFileDialog.getSaveFileName(caption="Logo als Bild speichern",
                                               directory="./My_Logo.png",
                                               filter="PNG (*.png)",
                                               options=QFileDialog.DontUseNativeDialog)
        # Check, ob eine Datei ausgewählt wurde
        if filename[0] != '':
            image: QImage = self.my_scene.scene_to_image()
            image.save(filename[0])
    
    # endregion
    
    @staticmethod
    def app_info():
        # ToDo #    Hier etwas mehr content rein und evtl ein QWidget um mehr anzuzeigen
        #           Ich will auch über die Gefahr beim Laden von Dateien informieren
        #           Und den ganzen Lizenz-Kram hier reinpacken
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Info")
        msgbox.setText("Info Text...")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowIcon(QIcon(
                bkPaths.icon('Polska.png')
                ))
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
    
    # region   Die 3 Buttons mit Aktionen versehen
    def btn_neue_farben(self):
        self.my_scene.logo_malen()
        self.textEdit_farben.clear()
        self.textEdit_farben.setHtml(self.my_scene.textedit_fill())
    
    def btn_reset(self):
        # Hier die Standardwerte aller Widgets neu setzen
        
        # region   Alle 7 normalen Slider und deren Label auf Ausgangswerte setzen,
        # dafür blockSignals(True) setzen,
        # damit die connecteden Methoden nicht ausgelöst werden und ich jedes Mal das Logo neu zeichne
        self.slider_dicke.blockSignals(True)
        self.slider_dicke.setProperty("value", 30)
        self.label_dicke_wert.setText(f"{self.slider_dicke.value()}")
        self.slider_dicke.blockSignals(False)
        
        self.slider_laenge.blockSignals(True)
        self.slider_laenge.setProperty("value", 90)
        self.label_laenge_wert.setText(f"{self.slider_laenge.value()}")
        self.slider_laenge.blockSignals(False)
        
        self.slider_pfeilspitzen_hoehe.blockSignals(True)
        self.slider_pfeilspitzen_hoehe.setProperty("value", 30)
        self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
        self.slider_pfeilspitzen_hoehe.blockSignals(False)
        
        self.slider_khoehe.blockSignals(True)
        self.slider_khoehe.setProperty("value", 30)
        self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
        self.slider_khoehe.blockSignals(False)
        
        self.slider_pfeilspitzen_dicke.blockSignals(True)
        self.slider_pfeilspitzen_dicke.setProperty("value", 30)
        self.label_pfeilspitzen_dicke_wert.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
        self.slider_pfeilspitzen_dicke.blockSignals(False)
        
        self.slider_pfeilspitzen_laenge.blockSignals(True)
        self.slider_pfeilspitzen_laenge.setProperty("value", 30)
        self.label_pfeilspitzen_laenge_wert.setText(f"{self.slider_pfeilspitzen_laenge.value()}")
        self.slider_pfeilspitzen_laenge.blockSignals(False)
        
        self.slider_abstand.blockSignals(True)
        self.slider_abstand.setProperty("value", 90)
        self.label_abstand_wert.setText(f"{self.slider_abstand.value()}")
        self.slider_abstand.blockSignals(False)
        # endregion
        
        # region   RangeSliders Standardwerte setzen auch mit blockSignals(True)
        for slider_code in ['r', 'g', 'b']:
            exec(f"self.range_slider_{slider_code}.blockSignals( True )")
            exec(f"self.range_slider_{slider_code}.setSliderPosition((0,255))")
            # print( f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen r: {{self.range_slider_{
            # slider_code}.value()}}' )" )  # DEBUG
            exec(f"self.label_slider_{slider_code}_werte.setText( f'Farbgrenzen {slider_code}: {{self.range_slider_"
                 f"{slider_code}.value()}}' )")
            exec(f"self.range_slider_{slider_code}.blockSignals( False )")
        # endregion
        
        # region   Checkboxen Pfeile auf den Ausgangszustand bringen
        # Auch hier blockSignals(True)
        self.wo_pfeile_dict = self.wo_pfeile_dict_original
        for nr in range(len(self.wo_pfeile_dict)):
            if self.wo_pfeile_dict[nr]:
                exec(f"self.checkBox_pfeil_{nr}.blockSignals( True )")
                exec(f"self.checkBox_pfeil_{nr}.setChecked(True)")
                exec(f"self.checkBox_pfeil_{nr}.blockSignals( False )")
            else:
                exec(f"self.checkBox_pfeil_{nr}.blockSignals( True )")
                exec(f"self.checkBox_pfeil_{nr}.setChecked(False)")
                exec(f"self.checkBox_pfeil_{nr}.blockSignals( False )")
        # endregion
        
        # region   Cbx Beschriftung & Cbx Dicken verknüpfen aus
        self.checkBox_beschriftung.blockSignals(True)
        self.checkBox_beschriftung.setChecked(False)
        self.checkBox_beschriftung.blockSignals(False)
        
        # Cbx Dicken verknüpfen aus
        self.checkBox_dicken_link.setChecked(False)
        # Hier keine blockSignals, weil diese Cbx keine Signale hat
        # endregion

        self.my_scene.logo_malen(alles_neu=True)
        self.textEdit_farben.clear()
        self.textEdit_farben.setHtml(self.my_scene.textedit_fill())
    
    def btn_ende(self):
        # DEBUG: self.textEdit_farben.setText("Button-Klick: Neuer Text mit .setText")
        msgbox = QMessageBox()
        msgbox.setWindowTitle("ByeBye...?")
        msgbox.setText("Wollens wirklich beenden?")
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setWindowIcon(QIcon(
                bkPaths.icon('Polska.png')
                ))
        msgbox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msgbox_erg = msgbox.exec_()
        # DEBUG: self.textEdit_farben.append(f"\n{msgbox_erg}")
        if msgbox_erg == QMessageBox.Ok:
            self.close()  # Beendet die App
    
    # endregion
    
    # region   Klassen-Methoden für die Aktivität der GUI-Elemente/-Widgets
    def rangeslider_r_werte_change(self):
        # DEBUG: self.textEdit_farben.setText(
        #    f"{self.range_slider_r.value()}\n _getBarColor() = {eval('self.range_slider_r._getBarColor()')}")
        self.label_slider_r_werte.setText(f"Farbgrenzen r: {self.range_slider_r.value()}")
    
    def rangeslider_g_werte_change(self):
        # DEBUG: self.textEdit_farben.setText(f"{self.range_slider_g.value()}")
        self.label_slider_g_werte.setText(f"Farbgrenzen g: {self.range_slider_g.value()}")
    
    def rangeslider_b_werte_change(self):
        # DEBUG: self.textEdit_farben.setText(f"{self.range_slider_b.value()}")
        self.label_slider_b_werte.setText(f"Farbgrenzen b: {self.range_slider_b.value()}")
    
    def slider_dicke_change(self):
        self.label_dicke_wert.setText(f"{self.slider_dicke.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_dicke.value()}")
        # DEBUG: self.textEdit_farben.append(eval(f"str(type(self.slider_dicke.value()))"))
        if self.checkBox_dicken_link.isChecked():
            self.label_pfeilspitzen_dicke_wert.setText(f"{self.slider_dicke.value()}")
            self.slider_pfeilspitzen_dicke.setValue(self.slider_dicke.value())

        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_laenge_change(self):
        self.label_laenge_wert.setText(f"{self.slider_laenge.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_laenge.value()}")
        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_khoehe_change(self):
        self.label_khoehe_wert.setText(f"{self.slider_khoehe.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_khoehe.value()}")
        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_pfeilspitzen_dicke_change(self):
        self.label_pfeilspitzen_dicke_wert.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
        if self.checkBox_dicken_link.isChecked():
            self.label_dicke_wert.setText(f"{self.slider_pfeilspitzen_dicke.value()}")
            self.slider_dicke.setValue(self.slider_pfeilspitzen_dicke.value())
        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_pfeilspitzen_laenge_change(self):
        self.label_pfeilspitzen_laenge_wert.setText(f"{self.slider_pfeilspitzen_laenge.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_pfeilspitzen_laenge.value()}")
        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_pfeilspitzen_hoehe_change(self):
        self.label_pfeilspitzen_hoehe_wert.setText(f"{self.slider_pfeilspitzen_hoehe.value()}")
        # DEBUG: self.textEdit_farben.setText(f"{self.slider_pfeilspitzen_hoehe.value()}")
        self.my_scene.logo_malen(farben_neu=False)
    
    def slider_abstand_change(self):
        self.label_abstand_wert.setText(f"{self.slider_abstand.value()}")
        # DEBUG: print(self.screen().size())
        self.my_scene.logo_malen(farben_neu=False)
    
    def cbx_pfeilspitzen_change(self):
        # DEBUG: self.textEdit_farben.setText('')
        for nr in range(len(self.wo_pfeile_dict)):
            if eval(f"self.checkBox_pfeil_{nr}.isChecked()"):
                self.wo_pfeile_dict[nr] = True
            elif not eval(f"self.checkBox_pfeil_{nr}.isChecked()"):
                self.wo_pfeile_dict[nr] = False
            else:
                self.wo_pfeile_dict[nr] = False
        # DEBUG: self.textEdit_farben.append(f"{self.wo_pfeile_dict}")
        self.my_scene.logo_malen(farben_neu=False)
    
    def checkBox_beschriftung_change(self):
        self.my_scene.logo_malen(farben_neu=False)
    # endregion


# Klasse für die Elemente-Malerei...
class BK_GScene(QGraphicsScene):
    def __init__(self):  # , parent=None
        super().__init__()  # super(BK_GScene, self).__init__(parent)
        self.setBackgroundBrush(Qt.white) # Für MacOS, da dort alles grau ist, wenn man keine Farbe setzt
        # Definition des Gerüstes des elemente_dict, gefüllt mit Dummies,
        # bis auf Richtungen und Nr und zValues
        self.elemente_dict: dict = {
                0 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'W',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'O',
                     'element_nr': 0,
                     'zValue'    : 0, 'zValue_flag': False,
                     },
                1 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'N',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'S',
                     'element_nr': 1,
                     'zValue'    : 1, 'zValue_flag': False,
                     },
                2 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'N',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'S',
                     'element_nr': 2,
                     'zValue'    : 2, 'zValue_flag': False,
                     },
                3 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'W',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'O',
                     'element_nr': 3,
                     'zValue'    : 3, 'zValue_flag': False,
                     },
                4 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'N',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'S',
                     'element_nr': 4,
                     'zValue'    : 4, 'zValue_flag': False,
                     },
                5 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'N',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'S',
                     'element_nr': 5,
                     'zValue'    : 5, 'zValue_flag': False,
                     },
                6 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'W',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'O',
                     'element_nr': 6,
                     'zValue'    : 6, 'zValue_flag': False,
                     },
                7 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'S',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'N',
                     'element_nr': 7,
                     'zValue'    : 7, 'zValue_flag': False,
                     },
                8 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'N',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'S',
                     'element_nr': 8,
                     'zValue'    : 8, 'zValue_flag': False,
                     },
                9 : {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'SW',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'NO',
                     'element_nr': 9,
                     'zValue'    : 9, 'zValue_flag': False,
                     },
                10: {'p1'        : QPointF(), 'p2': QPointF(),
                     'color'     : QColor('white'), 'color_flag': False,
                     'pfeil_p1'  : False, 'pfeil_p1_richtung': 'NW',
                     'pfeil_p2'  : False, 'pfeil_p2_richtung': 'SO',
                     'element_nr': 10,
                     'zValue'    : 10, 'zValue_flag': False,
                     },
                }
        self.my_pen = QPen()
        self.my_pen.setCapStyle(Qt.RoundCap)  # Qt.FlatCap
        # Liste für die Zufalls-Farben
        self.farbliste: list = []
        # region    Alle Attribute für die Elemente dynamisch erzeugen
        for nr in range(ANZAHL_ELEMENTE):
            exec(f"self.my_item_{nr} = None")
            # print(f"self.my_item_{nr} = None")  # DEBUG
            exec(f"self.my_pfeil_{nr}_0  = None")
            # print(f"self.my_pfeil_{nr}_0  = None")  # DEBUG
            exec(f"self.my_pfeil_{nr}_1  = None")
            # print(f"self.my_pfeil_{nr}_1  = None")  # DEBUG
            exec(f"self.my_text_{nr} = None")
            # print(f"self.my_text_{nr} = None")  # DEBUG
            exec(f"self.my_group_{nr} = None")
        # endregion
        # Farben generieren
        self.rndcolors()
    
    def rndcolors(self):
        self.farbliste = []
        for _ in range(ANZAHL_ELEMENTE):
            g = rnd.randint(my_gui.range_slider_g.value()[0], my_gui.range_slider_g.value()[1])
            r = rnd.randint(my_gui.range_slider_r.value()[0], my_gui.range_slider_r.value()[1])
            b = rnd.randint(my_gui.range_slider_b.value()[0], my_gui.range_slider_b.value()[1])
            self.farbliste.append((r, g, b, 255))
    
    def update_elemente_dict(self):
        h = my_gui.slider_dicke.value()
        w = my_gui.slider_laenge.value()
        ab = my_gui.slider_abstand.value()
        hk = my_gui.slider_khoehe.value()
        beschriftung = my_gui.checkBox_beschriftung.isChecked()
        
        # region   p1 und p2 neu setzen für alle Elemente im Dict
        self.elemente_dict[0]['p1'] = QPointF(0, 0)
        self.elemente_dict[0]['p2'] = QPointF(w, 0)
        
        self.elemente_dict[1]['p1'] = QPointF(0, 0)
        self.elemente_dict[1]['p2'] = QPointF(0, w)
        
        self.elemente_dict[2]['p1'] = QPointF(w, 0)
        self.elemente_dict[2]['p2'] = QPointF(w, w)
        
        self.elemente_dict[3]['p1'] = QPointF(0, w)
        self.elemente_dict[3]['p2'] = QPointF(w + h, w)
        
        self.elemente_dict[4]['p1'] = QPointF(0, w)
        self.elemente_dict[4]['p2'] = QPointF(0, 2 * w)
        
        self.elemente_dict[5]['p1'] = QPointF(w + h, w)
        self.elemente_dict[5]['p2'] = QPointF(w + h, 2 * w)
        
        self.elemente_dict[6]['p1'] = QPointF(0, 2 * w)
        self.elemente_dict[6]['p2'] = QPointF(w + h, 2 * w)
        
        self.elemente_dict[7]['p1'] = QPointF(w + h + ab, w)
        self.elemente_dict[7]['p2'] = QPointF(w + h + ab, -hk)
        
        self.elemente_dict[8]['p1'] = QPointF(w + h + ab, w)
        self.elemente_dict[8]['p2'] = QPointF(w + h + ab, 2 * w)
        
        self.elemente_dict[9]['p1'] = QPointF(w + h + ab, w)
        self.elemente_dict[9]['p2'] = QPointF(2 * w + h + ab, 0)
        
        self.elemente_dict[10]['p1'] = QPointF(w + h + ab, w)
        self.elemente_dict[10]['p2'] = QPointF(2 * w + h + ab, 2 * w)
        # endregion
        
        # region   Pfeilspitzen, Farben, zValue im dict setzen
        for nr in range(2 * ANZAHL_ELEMENTE):
            nr_halb = math.floor(nr / 2)
            if nr % 2 != 0:
                # Pfeilspitzen
                self.elemente_dict[nr_halb]['pfeil_p1'] = eval(f"my_gui.checkBox_pfeil_{nr - 1}.isChecked()")
                self.elemente_dict[nr_halb]['pfeil_p2'] = eval(f"my_gui.checkBox_pfeil_{nr}.isChecked()")
                # zValue
                if not self.elemente_dict[nr_halb]['zValue_flag']:
                    self.elemente_dict[nr_halb]['zValue'] = nr_halb
                # Farben
                if not self.elemente_dict[nr_halb]['color_flag']:
                    self.elemente_dict[nr_halb]['color'] = self.farbliste[nr_halb]
        # endregion
    
    def logo_malen(self, alles_neu: bool = False, farben_neu: bool = True):
        if alles_neu:
            self.reset_flags()
        if farben_neu:
            self.rndcolors()
        
        self.clear()
        
        h = my_gui.slider_dicke.value()
        w = my_gui.slider_laenge.value()
        ab = my_gui.slider_abstand.value()
        hk = my_gui.slider_khoehe.value()
        beschriftung = my_gui.checkBox_beschriftung.isChecked()
        
        self.update_elemente_dict()
        
        self.my_pen.setWidth(h)
        
        for nr in self.elemente_dict:
            # Leere ItemGroups erstellen und zu Scene hinzufügen
            # Wenn ich das in __init__mache, dann wird die erstellte ItemGroup durch clear () auch gelöscht!!!
            exec(f"self.my_group_{nr} = self.createItemGroup([])")
            # Jeder Group customData '0' : nr mitgeben
            exec(f"self.my_group_{nr}.setData( 0, {nr} )")
            # print( f"self.my_group_{nr} = self.createItemGroup([])" )  # DEBUG
            # print( f"self.my_group_{nr}.setData( 0, {nr} )" )  # DEBUG
            
            self.my_pen.setColor(QColor(*self.elemente_dict[nr]['color']))
            # Erst LineItems basteln und dann diese der entsprechenden Gruppe hinzufügen und als Attribute speichern
            # dann ItemIsSelectable + ItemIsFocusable setzen für die ItemGroup
            # siehe scratch_1.py
            
            exec(f"self.my_item_{nr} = QGraphicsLineItem("
                 f"QLineF("
                 f"self.elemente_dict[nr]['p1'], "
                 f"self.elemente_dict[nr]['p2']"
                 f")"
                 f")"
                 )
            exec(f"self.my_item_{nr}.setPen(self.my_pen)")
            exec(f"self.my_item_{nr}.setData( 0, {nr} )")  # Jedem Item customData '0' : nr mitgeben
            exec(f"self.my_group_{nr}.addToGroup( self.my_item_{nr} )")
            # ZValue manuell setzen
            exec(f"self.my_group_{nr}.setZValue(self.elemente_dict[{nr}]['zValue'])")
            
            if self.elemente_dict[nr]['pfeil_p1']:
                self.pfeilspitze_malen(p1=self.elemente_dict[nr]['p1'],
                                       richt=self.elemente_dict[nr]['pfeil_p1_richtung'],
                                       nr=self.elemente_dict[nr]['element_nr'],
                                       color=self.elemente_dict[nr]['color'])
            if self.elemente_dict[nr]['pfeil_p2']:
                self.pfeilspitze_malen(p1=self.elemente_dict[nr]['p2'],
                                       richt=self.elemente_dict[nr]['pfeil_p2_richtung'],
                                       nr=self.elemente_dict[nr]['element_nr'],
                                       color=self.elemente_dict[nr]['color'])
            if beschriftung:
                self.beschriften(nr=self.elemente_dict[nr]['element_nr'],
                                 p1=self.elemente_dict[nr]['p1'],
                                 p2=self.elemente_dict[nr]['p2'],
                                 color=self.elemente_dict[nr]['color'], h=h)
        
        self.textedit_fill()
        my_gui.bk_graphicsView.centerOn(0, 0)
    
    def pfeilspitze_malen(self, p1: QPointF, richt, nr: int, color: tuple = (0, 0, 0, 255)):
        # region   Hier müsste ich noch die Vorzeichen ändern...um  unabhängig von NW,S,SW,.. zu sein
        # je nachdem,in welche Richtung (pos, neg) der Pfeil zeigen soll
        #       Konvention:
        #           Linie p1 -> p2
        #           - Pfeil(an p2) in der Richtung p1->p2 ist positiv
        #           - Pfeil(an p1) in der Richtung p2->p1 ist negativ
        # endregion # ABER: NW,SW,NO,SO tut's auch ;-)
        sh = my_gui.slider_pfeilspitzen_hoehe.value()
        sl = my_gui.slider_pfeilspitzen_laenge.value()
        sd = my_gui.slider_pfeilspitzen_dicke.value()
        
        my_pen_s = QPen(QColor(*color))
        my_pen_s.setWidth(sd)
        my_pen_s.setCapStyle(Qt.RoundCap)
        
        alpha: float = 0
        x_p1 = p1.x()
        y_p1 = p1.y()
        # region   Formeln für die Punkte der Pfeilspitzen
        if richt == "S":
            alpha = 90 * math.pi / 180
        elif richt == "O":
            alpha = 0
        elif richt == "N":
            alpha = -90 * math.pi / 180
        elif richt == "W":
            alpha = -180 * math.pi / 180
        
        elif richt == "SO":
            alpha = 45 * math.pi / 180  # math.atan(y_p1 / x_p1)
        elif richt == "NO":
            alpha = -45 * math.pi / 180
        elif richt == "SW":
            alpha = 135 * math.pi / 180
        elif richt == "NW":
            alpha = -135 * math.pi / 180
        
        if x_p1 < 0:
            x_p2 = x_p1 + sl * math.cos(alpha) - sh * math.sin(alpha)
            y_p2 = y_p1 + sl * math.sin(alpha) + sh * math.cos(alpha)
            
            x_p3 = x_p1 + sl * math.cos(alpha) + sh * math.sin(alpha)
            y_p3 = y_p1 + sl * math.sin(alpha) - sh * math.cos(alpha)
        else:
            x_p2 = x_p1 - sl * math.cos(alpha) + sh * math.sin(alpha)
            y_p2 = y_p1 - sl * math.sin(alpha) - sh * math.cos(alpha)
            
            x_p3 = x_p1 - sl * math.cos(alpha) - sh * math.sin(alpha)
            y_p3 = y_p1 - sl * math.sin(alpha) + sh * math.cos(alpha)
        # endregion
        p2 = QPointF(x_p2, y_p2)
        p3 = QPointF(x_p3, y_p3)
        
        # siehe scratch_1.py
        exec(f"self.my_pfeil_{nr}_0 = QGraphicsLineItem( QLineF( p1, p2 ) )")
        exec(f"self.my_pfeil_{nr}_0.setPen( my_pen_s )")
        exec(f"self.my_pfeil_{nr}_0.setData( 0, {nr} )")  # # Jedem Item customData '0' : nr mitgeben
        exec(f"self.my_pfeil_{nr}_1 = QGraphicsLineItem( QLineF( p1, p3 ) )")
        exec(f"self.my_pfeil_{nr}_1.setPen( my_pen_s )")
        exec(f"self.my_pfeil_{nr}_1.setData( 0, {nr} )")  # # Jedem Item customData '0' : nr mitgeben
        exec(f"self.my_group_{nr}.addToGroup( self.my_pfeil_{nr}_0 )")
        exec(f"self.my_group_{nr}.addToGroup( self.my_pfeil_{nr}_1 )")
    
    def beschriften(self, nr: int, p1: QPointF, p2: QPointF, color: tuple, h: int):
        exec(f"self.my_text_{nr} = QGraphicsTextItem()")
        # exec( f"self.my_text_{nr}.setDefaultTextColor( {color} )")
        exec(f"self.my_text_{nr}.setFont( QFont( 'Times', h, QFont.Bold ) ) ")
        exec(f"self.my_text_{nr}.setHtml(f'<span style = \"color:{QColor(*color).name()}\">{nr}</span>')")
        # region   Formeln für die Position der Beschriftungen
        if (p2.y() - p1.y()) == 0:
            p_beschriftung = QPointF(0.5 * abs(p2.x() - p1.x()),
                                     -2 * h + abs(p1.y()))
        elif (p2.x() - p1.x()) == 0:
            if p2.y() > 0 and p1.y() > 0:
                p_beschriftung = QPointF(-1.5 * h + abs(p1.x()),
                                         1.5 * abs(p2.y() - p1.y())
                                         )
            elif p2.y() < 0 and p1.y() < 0:
                p_beschriftung = QPointF(-1.5 * h + abs(p1.x()),
                                         1.5 * (abs(p2.y()) - abs(p1.y()))
                                         )
            elif p2.y() <= 0 < p1.y():
                p_beschriftung = QPointF(-1.5 * h + abs(p1.x()),
                                         -0.5 * abs(p2.y() - p1.y())
                                         )
            elif p2.y() > 0 >= p1.y():
                p_beschriftung = QPointF(-1.5 * h + abs(p1.x()),
                                         0.5 * (abs(p2.y()) - abs(p1.y()))
                                         )
        else:
            p_beschriftung = QPointF(h + p2.x(),
                                     1.5 * h + 0.3 * p2.y()
                                     )
        # endregion
        exec(f"self.my_text_{nr}.setPos(p_beschriftung)")
        exec(f"self.my_text_{nr}.setData( 0, {nr} )")  # Jedem Item customData '0' : nr mitgeben" )
        
        # Z-value ist wie der der Group, in das die Beschriftung reinkommt
        exec(f"self.my_group_{nr}.addToGroup( self.my_text_{nr} )")
    
    def textedit_fill(self):  # 4 CHANGES_OUTSIDE_CLASS
        ll = 0
        text2insert = "<span style=\" font-family:'Verdana'; font-size:8pt; "\
                      "font-style:normal;font-weight: bold;\"> "
        for nr in self.elemente_dict:
            text2insert += f"<span style = \"color:{QColor(*self.elemente_dict[nr]['color']).name()}\">"
            text2insert += f"{ll}: RGB: {str(self.elemente_dict[nr]['color'])} "
            text2insert += f"Hex: {QColor(*self.elemente_dict[nr]['color']).name()}"
            text2insert += "</span><br>"
            ll += 1
        text2insert += "</span>"
        return text2insert
    
    def reset_flags(self):
        for nr in self.elemente_dict:
            self.elemente_dict[nr]['color_flag'] = False
            self.elemente_dict[nr]['zValue_flag'] = False
    
    def contextMenuEvent(self, sceneEvent):
        super().contextMenuEvent(sceneEvent)
        pp = sceneEvent.scenePos()
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QGraphicsScene.html#PySide2.PySide2.QGraphicsScene.items
        aktuelle_items = self.items(pp)  # Alle Items an der aktuellen Postion
        # zuvor : aktuelles_item = self.itemAt( pp, QTransform() )
        # Jetzt checken, ob und wie viele Items an der Position sind
        # Meine Items, die an der aktuellen Pos sind, sind "einzigartig". Sprich jedes Item(data = Nr) kommt nur
        # einmal vor.
        # Es sind zwar immer mindestens 2 Items an der Stelle, weil es immer zB ein Item(0) und eine ItemGroup(0) gibt.
        # Das habe ich ja so gebaut...
        # Somit brauche ich  "if len(aktuelle_items) == 1:" NICHT ;-) Entweder keins oder mindestens 2
        if len(aktuelle_items) == 0:
            my_menu = QMenu()
            act_info_nr = QAction("Hier is NÜSCHT")
            act_info_nr.setIcon(QIcon(
                    bkPaths.icon('Remove_24x24.png')
                    ))
            my_menu.addAction(act_info_nr)
            my_menu.setAccessibleName('BKMENU')
            my_menu.exec(sceneEvent.screenPos())
        else:
            # Hier fische ich mir erstmal nur die ItemGroups heraus
            
            # Liste für meine ItemGroups
            items_distinct_list: list = []
            
            # Alle ItemGroup-Objekte in eine Liste packen
            for it in aktuelle_items:
                # print( type(it), it.data( 0 ) ) # DEBUG
                if type(it) == QGraphicsItemGroup:  # Ich brauche nur die ItemGroups
                    # print( "Dadda brauchisch: ", type( it ), it.data( 0 ), "type(it.data( 0 ))= ", type(it.data( 0 )) ) # DEBUG
                    items_distinct_list.append(it)  # ItemGroup hinzufügen
            # print("-------------") # DEBUG
            # print(items_distinct_list) # DEBUG
            
            if len(items_distinct_list) == 1:
                # region   Hier habe ich nur 1 Item, also das normale Menü
                my_menu = QMenu()
                aktuelle_farbe = QColor(*self.elemente_dict[items_distinct_list[0].data(0)]['color'])
                act_info_nr = QAction("Element Nr " + str(aktuelle_items[0].data(0)))
                nu_pixmap: QPixmap = self.make_color_rect_pixmap(aktuelle_farbe)
                act_info_nr.setIcon(QIcon(nu_pixmap))  # QIcon( 'ui_files/Information_24x24.png' )
                info_font = act_info_nr.font()
                info_font.setBold(True)
                info_font.setUnderline(True)
                act_info_nr.setFont(info_font)
                my_menu.setDefaultAction(act_info_nr)
                stylen = f"QMenu::item:default "\
                         f"{{color: '{QColor(*self.elemente_dict[aktuelle_items[0].data(0)]['color']).name()}'}}"
                my_menu.setStyleSheet(stylen)
                
                list_zvalues: list = []
                for nr in self.elemente_dict:
                    list_zvalues.append(int(self.elemente_dict[nr]['zValue']))
                zvalue_max = max(list_zvalues)
                zvalue_min = min(list_zvalues)
                
                text_act_zvalue: str = "Ebene: "
                text_act_zvalue += str(int(self.elemente_dict[aktuelle_items[0].data(0)]['zValue']))
                text_act_zvalue += "  (" + str(zvalue_min) + " - " + str(zvalue_max) + ")"
                
                act_info_zvalue = QAction(text_act_zvalue)
                act_info_zvalue.setIcon(QIcon(
                        bkPaths.icon('Information_24x24.png')
                        ))
                
                act_zvalue_max = QAction("Ganz nach vorne")
                act_zvalue_max.setIcon(QIcon(
                        bkPaths.icon('Stock Index Up_24x24__top.png')
                        ))
                act_zvalue_max.triggered.connect(lambda: self.item_zValue_max(aktuelle_items[0]))
                
                act_zvalue_plus = QAction("Eine Ebene nach vorne")
                act_zvalue_plus.setIcon(QIcon(
                        bkPaths.icon('Stock Index Up_24x24.png')
                        ))
                act_zvalue_plus.triggered.connect(lambda: self.item_zValue_plus(aktuelle_items[0]))
                
                # Das Icon für die CBX hierzu ist im stylesheet (QMenu::indicator:non-exclusive:unchecked)
                act_zvalue_fix = QAction("Die aktuelle Ebene immer beibehalten/fixieren")
                act_zvalue_fix.setCheckable(True)
                act_zvalue_fix.setChecked(self.elemente_dict[items_distinct_list[0].data(0)]['zValue_flag'])
                act_zvalue_fix.toggled.connect(lambda: self.item_zvalue_toggle(aktuelle_items[0]))
                
                act_zvalue_minus = QAction("Eine Ebene nach hinten")
                act_zvalue_minus.setIcon(QIcon(
                        bkPaths.icon('Stock Index Down_24x24.png')
                        ))
                act_zvalue_minus.triggered.connect(lambda: self.item_zValue_minus(aktuelle_items[0]))
                
                act_zvalue_min = QAction("Ganz nach hinten")
                act_zvalue_min.setIcon(QIcon(
                        bkPaths.icon('Stock Index Down_24x24__down.png')
                        ))
                act_zvalue_min.triggered.connect(lambda: self.item_zValue_min(aktuelle_items[0]))
                
                # https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
                act_neue_Farbe = QAction("Neue Farbe für Item " + str(aktuelle_items[0].data(0)))
                act_neue_Farbe.setIcon(QIcon(
                        bkPaths.icon('chromatic.png')
                        ))
                act_neue_Farbe.triggered.connect(lambda: self.item_neue_farbe(aktuelle_items[0]))
                
                act_Farbe_fix = QAction("Diese Farbe immer beibehalten/fixieren")
                act_Farbe_fix.setCheckable(True)
                act_Farbe_fix.setChecked(self.elemente_dict[items_distinct_list[0].data(0)]['color_flag'])
                # act_Farbe_fix.triggered.connect( lambda: self.item_Farbe_fix_toggle( aktuelle_items[ 0 ] ) )
                act_Farbe_fix.toggled.connect(lambda: self.item_Farbe_fix_toggle(aktuelle_items[0]))
                
                my_menu.setSeparatorsCollapsible(False)
                my_menu.addSeparator()
                my_menu.addAction(act_info_nr)
                my_menu.addAction(act_info_zvalue)
                my_menu.addSeparator()
                my_menu.addAction(act_zvalue_max)
                my_menu.addAction(act_zvalue_plus)
                my_menu.addAction(act_zvalue_fix)
                my_menu.addAction(act_zvalue_minus)
                my_menu.addAction(act_zvalue_min)
                my_menu.addSeparator()
                my_menu.addAction(act_neue_Farbe)
                my_menu.addAction(act_Farbe_fix)
                my_menu.addSeparator()
                
                my_menu.exec(sceneEvent.screenPos())
                # endregion
            else:
                # Mit den ItemGroups in meiner Liste die QMenus bauen
                my_menu_top = QMenu()
                
                # region   Min und Max der aktuell bestehenden zValues aus elemente_dict ermitteln
                list_zvalues: list = []
                for nr in self.elemente_dict:
                    list_zvalues.append(int(self.elemente_dict[nr]['zValue']))
                zvalue_max = max(list_zvalues)
                zvalue_min = min(list_zvalues)
                # endregion
                
                # region   SubMenüs bauen
                # Meine "dynamischen" Variablen erstellen
                my_menu_sub = 'my_menu_sub_'
                act_info_nr = 'act_info_nr_'
                act_info_zvalue = 'act_info_zvalue_'
                act_zvalue_max = 'act_zvalue_max_'
                act_zvalue_plus = 'act_zvalue_plus_'
                act_zvalue_minus = 'act_zvalue_minus_'
                act_zvalue_min = 'act_zvalue_min_'
                act_neue_Farbe = 'act_neue_Farbe_'
                act_zvalue_fix = 'act_zvalue_fix_'
                act_Farbe_fix = 'act_Farbe_fix_'
                # Durch die vorliegenden GroupItems loopen und daraus die SubMenüs und die Einträge basteln ... ÄCHZ...
                for itti in range(len(items_distinct_list)):
                    # Eigene Pixmap für Icon mit der aktuellen Farbe
                    aktuelle_farbe = QColor(*self.elemente_dict[items_distinct_list[itti].data(0)]['color'])
                    nu_pixmap: QPixmap = self.make_color_rect_pixmap(aktuelle_farbe)
                    # Untermenüs anlegen (mit dem Icon)
                    exec(f"{my_menu_sub + str(itti)} ="
                         f" my_menu_top.addMenu( QIcon( nu_pixmap ), "
                         f"'Element Nr ' + str( {items_distinct_list[itti].data(0)} ) )"
                         )
                    # Ich will Separators auch am Anfang und Ende sehen
                    # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMenu.html?highlight=qmenu%20separator#PySide2.PySide2.QMenu.setSeparatorsCollapsible
                    exec(f"{my_menu_sub + str(itti)}.setSeparatorsCollapsible( False )")
                    # Die Actions für das aktuelle Submenü bauen
                    # region Infos: ItemNr und zValue
                    exec(f"{act_info_nr + str(itti)} = QAction(QIcon( nu_pixmap ), 'Element Nr ' + str( {items_distinct_list[itti].data(0)} ) ) ")
                    # region   Font für den 1. SubMenü-Eintrag FETT machen
                    info_font = eval(f"{act_info_nr + str(itti)}.font() ")
                    info_font.setBold(True)
                    info_font.setUnderline(True)
                    info_font = eval(f"{act_info_nr + str(itti)}.setFont( info_font ) ")
                    
                    exec(
                            f"{my_menu_sub + str(itti)}.setDefaultAction( {act_info_nr + str(itti)} )"
                            )
                    
                    stylen = f"QMenu::item:default "\
                             f"{{color: '"\
                             f"{QColor(*self.elemente_dict[items_distinct_list[itti].data(0)]['color']).name()}'}}"
                    exec(
                            f"{my_menu_sub + str(itti)}.setStyleSheet( stylen )"
                            )
                    # endregion
                    
                    text_act_zvalue: str = "Ebene: "
                    text_act_zvalue += str(int(  # zValue ist n Float, ich will int
                            self.elemente_dict[items_distinct_list[itti].data(0)]['zValue']))
                    text_act_zvalue += "  (" + str(zvalue_min) + " - " + str(zvalue_max) + ")"
                    
                    # Ich muss wohl auch die Namen der Actions dynamisch generieren....
                    exec(f"{act_info_zvalue + str(itti)} = QAction( QIcon( '{bkPaths.icon('Information_24x24.png').replace(chr(92), chr(92) + chr(92))}' ), '{text_act_zvalue}' ) ")
                    # endregion
                    
                    exec(f"{act_zvalue_max + str(itti)} = QAction( QIcon( '{bkPaths.icon('Stock Index Up_24x24__top.png').replace(chr(92), chr(92) + chr(92))}' ), 'Ganz nach vorne' ) ")
                    exec(f"{act_zvalue_max + str(itti)}.triggered.connect( partial( self.item_zValue_max, items_distinct_list[{itti}] ) ) ")
                    
                    exec(f"{act_zvalue_plus + str(itti)} = QAction( QIcon( '{bkPaths.icon('Stock Index Up_24x24.png').replace(chr(92), chr(92) + chr(92))}' ), 'Eine Ebene nach vorne' ) ")
                    exec(f"{act_zvalue_plus + str(itti)}.triggered.connect( partial( self.item_zValue_plus, items_distinct_list[{itti}] ) ) ")
                    # Lambda ging hier nicht, und die 2. Alternative ist ja functools.partial, was ich nur zur hälfte verstanden habe, aber egal :-)
                    
                    exec(f"{act_zvalue_fix + str(itti)} = QAction('Die aktuelle Ebene immer beibehalten/fixieren')")
                    exec(f"{act_zvalue_fix + str(itti)}.setCheckable( True )")
                    exec(f"{act_zvalue_fix + str(itti)}.setChecked(self.elemente_dict[ items_distinct_list[ {itti} ].data( 0 ) ][ 'zValue_flag' ] ) ")
                    exec(f"{act_zvalue_fix + str(itti)}.toggled.connect( partial( self.item_zvalue_toggle, items_distinct_list[{itti}] ) ) ")
                    
                    exec(f"{act_zvalue_minus + str(itti)} = QAction( QIcon( '{bkPaths.icon('Stock Index Down_24x24.png').replace(chr(92), chr(92) + chr(92))}' ), 'Eine Ebene nach hinten' ) ")
                    exec(f"{act_zvalue_minus + str(itti)}.triggered.connect( partial( self.item_zValue_minus, items_distinct_list[{itti}] ) ) ")
                    
                    exec(f"{act_zvalue_min + str(itti)} = QAction( QIcon( '{bkPaths.icon('Stock Index Down_24x24__down.png').replace(chr(92), chr(92) + chr(92))}' ), 'Ganz nach hinten' ) ")
                    exec(f"{act_zvalue_min + str(itti)}.triggered.connect( partial( self.item_zValue_min, items_distinct_list[{itti}] ) ) ")
                    
                    exec(f"{act_neue_Farbe + str(itti)} = QAction( QIcon( '{bkPaths.icon('chromatic.png').replace(chr(92), chr(92) + chr(92))}' ), 'Neue Farbe für Item ' + str( {items_distinct_list[itti].data(0)} ) ) ")
                    exec(f"{act_neue_Farbe + str(itti)}.triggered.connect( partial( self.item_neue_farbe, items_distinct_list[{itti}] ) ) ")
                    
                    exec(f"{act_Farbe_fix + str(itti)} = QAction('Diese Farbe immer beibehalten/fixieren') ")
                    exec(f"{act_Farbe_fix + str(itti)}.setCheckable( True ) ")
                    exec(f"{act_Farbe_fix + str(itti)}.setChecked(self.elemente_dict[ items_distinct_list[ {itti} ].data( 0 ) ][ 'color_flag' ])")
                    exec(f"{act_Farbe_fix + str(itti)}.toggled.connect( partial( self.item_Farbe_fix_toggle, items_distinct_list[{itti}] ) ) ")
                    
                    # region   Die ganzen Aktionen zum aktuellen SubMenü hinzufügen
                    exec(
                            f"{my_menu_sub + str(itti)}.addSeparator()"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_info_nr + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_info_zvalue + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addSeparator()"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_zvalue_max + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_zvalue_plus + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_zvalue_fix + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_zvalue_minus + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_zvalue_min + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addSeparator()"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_neue_Farbe + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addAction( {act_Farbe_fix + str(itti)} )"
                            )
                    exec(
                            f"{my_menu_sub + str(itti)}.addSeparator()"
                            )
                my_menu_top.exec_(sceneEvent.screenPos())
                # endregion
    
    # region   Methoden für die Kontext-Menü-Aktkionen
    def item_zValue_plus(self, aktuelles_item: QGraphicsItem):
        if aktuelles_item.parentItem():
            aktuelles_item.parentItem().setZValue(aktuelles_item.parentItem().zValue() + 1)
            # Den neuen zValue des parents auch ins dict schreiben
            self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.parentItem().data(0)][
                'zValue'] = aktuelles_item.parentItem().zValue()
        else:
            aktuelles_item.setZValue(aktuelles_item.zValue() + 1)
            # Den neuen zValue auch ins dict schreiben
            self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.data(0)]['zValue'] = aktuelles_item.zValue()
    
    def item_zValue_max(self, aktuelles_item: QGraphicsItem):
        # region   Max der aktuell bestehenden zValues aus elemente_dict ermitteln
        list_zvalues: list = []
        for nr in self.elemente_dict:
            list_zvalues.append(int(self.elemente_dict[nr]['zValue']))
        zvalue_max = max(list_zvalues)
        # endregion
        if aktuelles_item.parentItem():
            aktuelles_item.parentItem().setZValue(zvalue_max + 1)
            # Den neuen zValue des parents auch ins dict schreiben
            self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.parentItem().data(0)][
                'zValue'] = aktuelles_item.parentItem().zValue()
        else:
            aktuelles_item.setZValue(zvalue_max + 1)
            # Den neuen zValue auch ins dict schreiben
            self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.data(0)]['zValue'] = aktuelles_item.zValue()
    
    def item_zValue_minus(self, aktuelles_item: QGraphicsItem):
        if aktuelles_item.parentItem():
            aktuelles_item.parentItem().setZValue(aktuelles_item.parentItem().zValue() - 1)
            # Den neuen zValue des parents auch ins dict schreiben
            self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.parentItem().data(0)][
                'zValue'] = aktuelles_item.parentItem().zValue()
        else:
            aktuelles_item.setZValue(aktuelles_item.zValue() - 1)
            # Den neuen zValue auch ins dict schreiben
            self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.data(0)]['zValue'] = aktuelles_item.zValue()
    
    def item_zValue_min(self, aktuelles_item: QGraphicsItem):
        # region   Min der aktuell bestehenden zValues aus elemente_dict ermitteln
        list_zvalues: list = []
        for nr in self.elemente_dict:
            list_zvalues.append(int(self.elemente_dict[nr]['zValue']))
        zvalue_min = min(list_zvalues)
        # endregion
        if aktuelles_item.parentItem():
            aktuelles_item.parentItem().setZValue(zvalue_min - 1)
            # Den neuen zValue des parents auch ins dict schreiben
            self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.parentItem().data(0)][
                'zValue'] = aktuelles_item.parentItem().zValue()
        else:
            aktuelles_item.setZValue(zvalue_min - 1)
            # Den neuen zValue auch ins dict schreiben
            self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = True
            self.elemente_dict[aktuelles_item.data(0)]['zValue'] = aktuelles_item.zValue()
    
    def item_neue_farbe(self, aktuelles_item: QGraphicsItem):
        new_color = QColorDialog()
        new_color.setOption(QColorDialog.DontUseNativeDialog, on=True)
        new_color.setOption(QColorDialog.ShowAlphaChannel, on=True)
        # Die bestehenden Farben aller Elemente als Custom Colors in den QColorDialog einfügen
        for nr in self.elemente_dict:
            new_color.setCustomColor(nr, QColor(*self.elemente_dict[nr]['color']))
        new_color.setWindowIcon(QIcon(bkPaths.icon('Polska.png')))
        new_color.setWindowTitle("Farbe des aktuellen Items bestimmen. Aktuelles Item = Item Nr_" + str(
                aktuelles_item.data(0)))
        new_color.setCurrentColor(QColor(*self.elemente_dict[aktuelles_item.data(0)]['color']))
        new_color.exec_()
        
        if new_color.selectedColor().isValid():
            self.elemente_dict[aktuelles_item.data(0)]['color'] = new_color.selectedColor().getRgb()
            
            print(new_color.selectedColor().getRgb())
            
            self.elemente_dict[aktuelles_item.data(0)]['color_flag'] = True
            if aktuelles_item.parentItem():
                self.my_pen.setColor(new_color.selectedColor())
                for child in aktuelles_item.parentItem().childItems():
                    # Checken, ob das ein TextItem ist, dann muss ich Farbe (und Text) anders setzen als mit QPen
                    if type(child) == QGraphicsTextItem:
                        child.setHtml(f"<span style = \"color:{new_color.selectedColor().name()}\">{aktuelles_item.data(0)}</span>")
                    else:
                        child.setPen(self.my_pen)
            else:
                self.my_pen.setColor(new_color.selectedColor())
                for child in aktuelles_item.childItems():
                    # Checken, ob das ein TextItem ist, dann muss ich Farbe (und Text) anders setzen als mit QPen
                    if type(child) == QGraphicsTextItem:
                        child.setHtml(f"<span style = \"color:{new_color.selectedColor().name()}\">"
                                      f"{aktuelles_item.data(0)}</span>")
                    else:
                        child.setPen(self.my_pen)
    
    def item_Farbe_fix_toggle(self, aktuelles_item: QGraphicsItem):
        if aktuelles_item.parentItem():
            if self.elemente_dict[aktuelles_item.parentItem().data(0)]['color_flag']:
                self.elemente_dict[aktuelles_item.parentItem().data(0)]['color_flag'] = False
            else:
                self.elemente_dict[aktuelles_item.parentItem().data(0)]['color_flag'] = True
        else:
            if self.elemente_dict[aktuelles_item.data(0)]['color_flag']:
                self.elemente_dict[aktuelles_item.data(0)]['color_flag'] = False
            else:
                self.elemente_dict[aktuelles_item.data(0)]['color_flag'] = True
    
    def item_zvalue_toggle(self, aktuelles_item: QGraphicsItem):
        if aktuelles_item.parentItem():
            if self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag']:
                self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = False
            else:
                self.elemente_dict[aktuelles_item.parentItem().data(0)]['zValue_flag'] = True
        else:
            if self.elemente_dict[aktuelles_item.data(0)]['zValue_flag']:
                self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = False
            else:
                self.elemente_dict[aktuelles_item.data(0)]['zValue_flag'] = True
    
    # endregion
    
    @staticmethod
    def make_color_rect_pixmap(color: QColor):
        # Methode, die aus einem kleinen Rechteck eine pixmap für n Icon macht
        # Brauche ich für die Qmenu-Icons und übergebe nur die Farbe
        # des ausgewählten Elements
        
        # Item=bloeckle erstellen
        bloeckle = QGraphicsRectItem(0, 0, 40, 40)
        penn = QPen(QColor(Qt.black), 1)
        penn.setCapStyle(Qt.SquareCap)
        bloeckle.setPen(penn)
        bloeckle.setBrush(
                QBrush(color, Qt.BrushStyle(Qt.SolidPattern))
                )
        # Die eigentliche Umwandlung
        pixmap = QPixmap(bloeckle.boundingRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.translate(-bloeckle.boundingRect().x(), -bloeckle.boundingRect().y())
        painter.setRenderHint(QPainter.Antialiasing, True)
        opt = QStyleOptionGraphicsItem()
        bloeckle.paint(painter, opt)
        
        return pixmap
    
    def scene_to_image(self):
        # Zum Speichern Background auf transparent, wegen MacOS
        self.setBackgroundBrush(Qt.transparent)
        # Get region of scene to capture from somewhere.
        areaF = self.sceneRect()  # Return type: QRectF
        # Create a QImage to render to and fix up a QPainter for it.
        image = QImage(areaF.toRect().size(),
                       QImage.Format_ARGB32_Premultiplied)
        # MUSICAmente :-)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        # MUSICAmente :-)
        painter.setRenderHint(painter.Antialiasing, True)
        # Render the region of interest to the QImage.
        self.render(painter,
                    QRectF(image.rect()),  # target
                    areaF)  # source
        painter.end()
        # # Für MacOS wieder auf white setzen
        self.setBackgroundBrush(Qt.white)
        return image


my_app = QApplication(sys.argv)

# region   Stylesheet einbinden

# root/base-dir festlegen
root = bkPaths.base_dir
# mit QDir einen Suchpfad =  addSearchPath festlegen,
# und den kann ich dann auch im QSS verwenden (siehe HIER)
QDir.addSearchPath('style', os.path.join(root, 'style'))
QDir.addSearchPath('icons', os.path.join(root, 'style/icons'))


qss = QFile('style:_BK_WordOffice2.qss')
qss.open(QFile.ReadOnly | QFile.Text)
my_app.setStyleSheet(str(qss.readAll(), 'utf-8'))
qss.close()


# File = open("style/_BK_WordOffice2.qss", 'r')
# with File:
#     dqss = File.read()
# my_app.setStyleSheet(dqss)
# endregion

my_gui = MeineGUI()

my_gui.my_scene = BK_GScene()
my_gui.bk_graphicsView.setScene(my_gui.my_scene)
my_gui.my_scene.logo_malen()
my_gui.textEdit_farben.setHtml(my_gui.my_scene.textedit_fill())

my_gui.show()

sys.exit(my_app.exec())
