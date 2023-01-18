import sys
import pygame
#import M9_Cycles
#import M5_Network
import M10_PyQt
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

#net = M9_Cycles.Start_window()

ex = M10_PyQt.Start()
ex.show()

#M9_Cycles.Game_body(M5_Network.Network('192.168.0.17'))

pygame.quit()
sys.exit(app.exec())