import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox, QCheckBox, QTextEdit
from PyQt5.QtCore import pyqtSlot
import arrows
from PIL import Image

game = arrows.Map()
def convert(path, inversion):
    img = Image.open(path).convert('1')
    img.save('output.png')

    W = img.size[0]
    H = img.size[1]
    for i in range(H):
        for j in range(W):
            if inversion:
                if img.getpixel((j, i)) == 0:
                    game.set(j, i, arrows.Arrow(type=arrows.ArrowType.Source))
                else:
                    game.set(j, i, arrows.Arrow(type=arrows.ArrowType.Pulse))
            else:
                if img.getpixel((j, i)) == 0:
                    game.set(j, i, arrows.Arrow(type=arrows.ArrowType.Pulse))
                else:
                    game.set(j, i, arrows.Arrow(type=arrows.ArrowType.Source))

    #print(game.export())

    #with open("out.txt", 'w', encoding="utf-8") as file:
    #    file.write(game.export())
    return game.export()

class App(QMainWindow):
 def __init__(self):
     super().__init__()
     self.title = 'img to scheme arrows'
     self.left = 10
     self.top = 10
     self.width = 350
     self.height = 300
     self.initUI()

 def initUI(self):
     self.setWindowTitle(self.title)
     self.setGeometry(self.left, self.top, self.width, self.height)
     self.setFixedSize(self.width, self.height) # set fixed size

     # Create textbox
     self.textbox = QLineEdit(self)
     self.textbox.move(20, 20)
     self.textbox.resize(280,40)

     # Create a button in the window
     self.browse_button = QPushButton('Обзор', self)
     self.browse_button.move(20,80)
     self.browse_button.clicked.connect(self.browse)

     # Create checkbox
     self.checkbox = QCheckBox('Инверсия', self)
     self.checkbox.move(20, 120)

     # Create a button in the window
     self.submit_button = QPushButton('Отправить', self)
     self.submit_button.move(20,150)
     self.submit_button.clicked.connect(self.submit)

     # Create a text box for output
     self.output_box = QTextEdit(self)
     self.output_box.move(20, 180)
     self.output_box.resize(280, 80)
     self.output_box.setReadOnly(True)

     self.show()

 @pyqtSlot()
 def browse(self):
     file_path = QFileDialog.getOpenFileName(self, 'Обзор', '', 'Images (*.png *.xpm *.jpg)')
     if file_path[0]:
         self.textbox.setText(file_path[0])

 @pyqtSlot()
 def submit(self):
     text = self.textbox.text()
     invert = self.checkbox.isChecked()
     result = convert(text, invert)
     self.output_box.setText(result)


if __name__ == '__main__':
 app = QApplication(sys.argv)
 ex = App()
 sys.exit(app.exec_())
