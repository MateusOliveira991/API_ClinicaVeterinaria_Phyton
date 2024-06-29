from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTabWidget, QListWidget, QFormLayout, QListWidgetItem
import requests

class TelaConsulta(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Cadastro e Consulta de Consultas')
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tab_cadastro = QWidget()
        self.tab_consulta = QWidget()
        
        self.tabs.addTab(self.tab_cadastro, 'Cadastro')
        self.tabs.addTab(self.tab_consulta, 'Consulta')
        
        self.initTabCadastro()
        self.initTabConsulta()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def initTabCadastro(self):
        layout = QFormLayout()
        
        self.label_id_animal_cadastro = QLabel('ID do Animal:')
        self.input_id_animal_cadastro = QLineEdit()
        self.label_id_veterinario_cadastro = QLabel('ID do Veterinário:')
        self.input_id_veterinario_cadastro = QLineEdit()
        self.label_id_estagiario_cadastro = QLabel('ID do Estagiário (opcional):')
        self.input_id_estagiario_cadastro = QLineEdit()
        self.label_data_cadastro = QLabel('Data:')
        self.input_data_cadastro = QLineEdit()
        self.label_hora_cadastro = QLabel('Hora:')
        self.input_hora_cadastro = QLineEdit()
        
        self.btn_cadastrar = QPushButton('Cadastrar')
        
        layout.addRow(self.label_id_animal_cadastro, self.input_id_animal_cadastro)
        layout.addRow(self.label_id_veterinario_cadastro, self.input_id_veterinario_cadastro)
        layout.addRow(self.label_id_estagiario_cadastro, self.input_id_estagiario_cadastro)
        layout.addRow(self.label_data_cadastro, self.input_data_cadastro)
        layout.addRow(self.label_hora_cadastro, self.input_hora_cadastro)
        layout.addRow(self.btn_cadastrar)
        
        self.tab_cadastro.setLayout(layout)
        
        self.btn_cadastrar.clicked.connect(self.cadastrar_consulta)
    
    def initTabConsulta(self):
        layout = QFormLayout()
        
        self.lista_consultas = QListWidget()
        self.lista_consultas.itemClicked.connect(self.item_selecionado)
        
        self.label_id_animal_consulta = QLabel('ID do Animal:')
        self.input_id_animal_consulta = QLineEdit()
        self.label_id_veterinario_consulta = QLabel('ID do Veterinário:')
        self.input_id_veterinario_consulta = QLineEdit()
        self.label_id_estagiario_consulta = QLabel('ID do Estagiário (opcional):')
        self.input_id_estagiario_consulta = QLineEdit()
        self.label_data_consulta = QLabel('Data:')
        self.input_data_consulta = QLineEdit()
        self.label_hora_consulta = QLabel('Hora:')
        self.input_hora_consulta = QLineEdit()
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setEnabled(False)
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.setEnabled(False)
        
        layout.addRow(self.lista_consultas)
        layout.addRow(self.label_id_animal_consulta, self.input_id_animal_consulta)
        layout.addRow(self.label_id_veterinario_consulta, self.input_id_veterinario_consulta)
        layout.addRow(self.label_id_estagiario_consulta, self.input_id_estagiario_consulta)
        layout.addRow(self.label_data_consulta, self.input_data_consulta)
        layout.addRow(self.label_hora_consulta, self.input_hora_consulta)
        layout.addRow(self.btn_editar, self.btn_excluir)
        
        self.tab_consulta.setLayout(layout)
        
        self.btn_editar.clicked.connect(self.editar_consulta)
        self.btn_excluir.clicked.connect(self.excluir_consulta)
        
        self.carregar_consultas()
        self.apply_styles()
    
    def clear_inputs_cadastro(self):
        self.input_id_animal_cadastro.clear()
        self.input_id_veterinario_cadastro.clear()
        self.input_id_estagiario_cadastro.clear()
        self.input_data_cadastro.clear()
        self.input_hora_cadastro.clear()
    
    def clear_inputs_consulta(self):
        self.input_id_animal_consulta.clear()
        self.input_id_veterinario_consulta.clear()
        self.input_id_estagiario_consulta.clear()
        self.input_data_consulta.clear()
        self.input_hora_consulta.clear()
    
    def carregar_consultas(self):
        self.lista_consultas.clear()
        
        try:
            response = requests.get('http://127.0.0.1:5000/consultas/consultas')
            
            if response.status_code == 200:
                consultas = response.json()
                for consulta in consultas:
                    estagiario_info = f" Estagiário: {consulta['id_estagiario']}" if consulta['id_estagiario'] else " Sem estagiário"
                    item = QListWidgetItem(f"Consulta {consulta['id']} - Animal: {consulta['id_animal']} Veterinário: {consulta['id_veterinario']}{estagiario_info}")
                    item.consulta_id = consulta['id']
                    self.lista_consultas.addItem(item)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao carregar consultas: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def item_selecionado(self, item):
        consulta_id = item.consulta_id
        
        try:
            response = requests.get(f'http://127.0.0.1:5000/consultas/consultas/{consulta_id}')
            
            if response.status_code == 200:
                consulta = response.json()
                self.input_id_animal_consulta.setText(str(consulta['id_animal']))
                self.input_id_veterinario_consulta.setText(str(consulta['id_veterinario']))
                self.input_id_estagiario_consulta.setText(str(consulta['id_estagiario']) if consulta['id_estagiario'] else '')
                self.input_data_consulta.setText(consulta['data'])
                self.input_hora_consulta.setText(consulta['hora'])
                self.btn_editar.setEnabled(True)
                self.btn_excluir.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao selecionar consulta: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def cadastrar_consulta(self):
        data = {
            'id_animal': self.input_id_animal_cadastro.text(),
            'id_veterinario': self.input_id_veterinario_cadastro.text(),
            'id_estagiario': self.input_id_estagiario_cadastro.text() if self.input_id_estagiario_cadastro.text() else None,
            'data': self.input_data_cadastro.text(),
            'hora': self.input_hora_cadastro.text()
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/consultas/consultas', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Sucesso', 'Consulta cadastrada com sucesso!')
                self.clear_inputs_cadastro()
                self.carregar_consultas()
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar consulta: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def editar_consulta(self):
        consulta_id = self.lista_consultas.currentItem().consulta_id
        
        data = {
            'id_animal': self.input_id_animal_consulta.text(),
            'id_veterinario': self.input_id_veterinario_consulta.text(),
            'id_estagiario': self.input_id_estagiario_consulta.text() if self.input_id_estagiario_consulta.text() else None,
            'data': self.input_data_consulta.text(),
            'hora': self.input_hora_consulta.text(),
        }
        
        try:
            response = requests.put(f'http://127.0.0.1:5000/consultas/consultas/{consulta_id}', json=data)
            
            if response.status_code == 200:
                QMessageBox.information(self, 'Sucesso', 'Consulta editada com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_consultas()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao editar consulta: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def excluir_consulta(self):
        consulta_id = self.lista_consultas.currentItem().consulta_id
        
        try:
            response = requests.delete(f'http://127.0.0.1:5000/consultas/consultas/{consulta_id}')
            
            if response.status_code == 204:
                QMessageBox.information(self, 'Sucesso', 'Consulta excluída com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_consultas()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao excluir consulta: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def apply_styles(self):
        style = """
        QWidget {
            background-image: url('img/vet.png');
            background-repeat: no-repeat;
            background-position: center;
        }
        """
        self.lista_consultas.setStyleSheet(style)
