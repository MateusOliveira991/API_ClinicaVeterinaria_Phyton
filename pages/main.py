import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStackedWidget, QMessageBox
from animal.animal import TelaAnimal
from consulta.consulta import TelaConsulta
from estagiario.estagiario import TelaEstagiario
from tutor.tutor import TelaTutor
from veterinario.veterinario import TelaVeterinario

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(170, 110, 850, 650)
        
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.tela_animal = TelaAnimal()
        self.tela_tutor = TelaTutor()
        self.tela_estagiario = TelaEstagiario()
        self.tela_veterinario = TelaVeterinario()
        self.tela_consulta = TelaConsulta()
        
        self.stacked_widget.addWidget(self.tela_animal)
        self.stacked_widget.addWidget(self.tela_tutor)
        self.stacked_widget.addWidget(self.tela_estagiario)
        self.stacked_widget.addWidget(self.tela_veterinario)
        self.stacked_widget.addWidget(self.tela_consulta)
        
        self.create_menu()
        self.apply_styles()
    
    def create_menu(self):
        menubar = self.menuBar()
        
        menu_animal = menubar.addMenu('Animal')
        menu_tutor = menubar.addMenu('Tutor')
        menu_estagiario = menubar.addMenu('Estagiário')
        menu_veterinario = menubar.addMenu('Veterinário')
        menu_consulta = menubar.addMenu('Consulta')
        
        act_animal = QAction('Gerenciar Animais', self)
        act_tutor = QAction('Gerenciar Tutores', self)
        act_estagiario = QAction('Gerenciar Estagiários', self)
        act_veterinario = QAction('Gerenciar Veterinários', self)
        act_consulta = QAction('Gerenciar Consultas', self)
        
        act_animal.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tela_animal))
        act_tutor.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tela_tutor))
        act_estagiario.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tela_estagiario))
        act_veterinario.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tela_veterinario))
        act_consulta.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tela_consulta))
        
        menu_animal.addAction(act_animal)
        menu_tutor.addAction(act_tutor)
        menu_estagiario.addAction(act_estagiario)
        menu_veterinario.addAction(act_veterinario)
        menu_consulta.addAction(act_consulta)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
            background-image: url('img/vet2.jpg');
            background-repeat: no-repeat;
            background-position: center;
        }
        QMenuBar {
            background-color: #2e2e2e;
            color: white;
        }
        QMenuBar::item {
            background-color: #2e2e2e;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #505050;
        }
        QMenu {
            background-color: #2e2e2e;
            color: white;
        }
        QMenu::item:selected {
            background-color: #505050;
        }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
