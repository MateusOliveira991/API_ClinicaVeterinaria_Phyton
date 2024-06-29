from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTabWidget, QListWidget, QFormLayout, QListWidgetItem
import requests

class TelaTutor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Cadastro e Consulta de Tutores')
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
        
        self.label_nome_cadastro = QLabel('Nome:')
        self.input_nome_cadastro = QLineEdit()
        self.label_cpf_cadastro = QLabel('CPF:')
        self.input_cpf_cadastro = QLineEdit()
        self.label_telefone_cadastro = QLabel('Telefone:')
        self.input_telefone_cadastro = QLineEdit()
        self.label_email_cadastro = QLabel('Email:')
        self.input_email_cadastro = QLineEdit()
        self.label_endereco_cadastro = QLabel('Endereço:')
        self.input_endereco_cadastro = QLineEdit()
        self.label_data_nascimento_cadastro = QLabel('Data de Nascimento:')
        self.input_data_nascimento_cadastro = QLineEdit()
        
        self.btn_cadastrar = QPushButton('Cadastrar')
        
        layout.addRow(self.label_nome_cadastro, self.input_nome_cadastro)
        layout.addRow(self.label_cpf_cadastro, self.input_cpf_cadastro)
        layout.addRow(self.label_telefone_cadastro, self.input_telefone_cadastro)
        layout.addRow(self.label_email_cadastro, self.input_email_cadastro)
        layout.addRow(self.label_endereco_cadastro, self.input_endereco_cadastro)
        layout.addRow(self.label_data_nascimento_cadastro, self.input_data_nascimento_cadastro)
        layout.addRow(self.btn_cadastrar)
        
        self.tab_cadastro.setLayout(layout)
        
        self.btn_cadastrar.clicked.connect(self.cadastrar_tutor)
    
    def initTabConsulta(self):
        layout = QFormLayout()
        
        self.lista_tutores = QListWidget()
        self.lista_tutores.itemClicked.connect(self.item_selecionado)
        
        self.label_nome_consulta = QLabel('Nome:')
        self.input_nome_consulta = QLineEdit()
        self.label_cpf_consulta = QLabel('CPF:')
        self.input_cpf_consulta = QLineEdit()
        self.label_telefone_consulta = QLabel('Telefone:')
        self.input_telefone_consulta = QLineEdit()
        self.label_email_consulta = QLabel('Email:')
        self.input_email_consulta = QLineEdit()
        self.label_endereco_consulta = QLabel('Endereço:')
        self.input_endereco_consulta = QLineEdit()
        self.label_data_nascimento_consulta = QLabel('Data de Nascimento:')
        self.input_data_nascimento_consulta = QLineEdit()
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setEnabled(False)
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.setEnabled(False)
        
        layout.addRow(self.lista_tutores)
        layout.addRow(self.label_nome_consulta, self.input_nome_consulta)
        layout.addRow(self.label_cpf_consulta, self.input_cpf_consulta)
        layout.addRow(self.label_telefone_consulta, self.input_telefone_consulta)
        layout.addRow(self.label_email_consulta, self.input_email_consulta)
        layout.addRow(self.label_endereco_consulta, self.input_endereco_consulta)
        layout.addRow(self.label_data_nascimento_consulta, self.input_data_nascimento_consulta)
        layout.addRow(self.btn_editar, self.btn_excluir)
        
        self.tab_consulta.setLayout(layout)
        
        self.btn_editar.clicked.connect(self.editar_tutor)
        self.btn_excluir.clicked.connect(self.excluir_tutor)
        
        self.carregar_tutores()
    
    def clear_inputs_cadastro(self):
        self.input_nome_cadastro.clear()
        self.input_cpf_cadastro.clear()
        self.input_telefone_cadastro.clear()
        self.input_email_cadastro.clear()
        self.input_endereco_cadastro.clear()
        self.input_data_nascimento_cadastro.clear()
    
    def clear_inputs_consulta(self):
        self.input_nome_consulta.clear()
        self.input_cpf_consulta.clear()
        self.input_telefone_consulta.clear()
        self.input_email_consulta.clear()
        self.input_endereco_consulta.clear()
        self.input_data_nascimento_consulta.clear()
    
    def carregar_tutores(self):
        self.lista_tutores.clear()
        self.apply_styles()
        
        try:
            response = requests.get('http://127.0.0.1:5000/tutores/tutores')
            
            if response.status_code == 200:
                tutores = response.json()
                for tutor in tutores:
                    item = QListWidgetItem(f"{tutor['id']} - {tutor['nome']} ({tutor['cpf']})")
                    item.tutor_id = tutor['id']
                    self.lista_tutores.addItem(item)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao carregar tutores: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def item_selecionado(self, item):
        tutor_id = item.tutor_id
        
        try:
            response = requests.get(f'http://127.0.0.1:5000/tutores/tutores/{tutor_id}')
            
            if response.status_code == 200:
                tutor = response.json()
                self.input_nome_consulta.setText(tutor['nome'])
                self.input_cpf_consulta.setText(tutor['cpf'])
                self.input_telefone_consulta.setText(tutor['telefone'])
                self.input_email_consulta.setText(tutor['email'])
                self.input_endereco_consulta.setText(tutor['endereco'])
                self.input_data_nascimento_consulta.setText(tutor['data_nascimento'])
                self.btn_editar.setEnabled(True)
                self.btn_excluir.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao selecionar tutor: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def cadastrar_tutor(self):
        data = {
            'nome': self.input_nome_cadastro.text(),
            'cpf': self.input_cpf_cadastro.text(),
            'telefone': self.input_telefone_cadastro.text(),
            'email': self.input_email_cadastro.text(),
            'endereco': self.input_endereco_cadastro.text(),
            'data_nascimento': self.input_data_nascimento_cadastro.text(),
            'tipo': 'tutor'
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/tutores/tutores', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Sucesso', 'Tutor cadastrado com sucesso!')
                self.clear_inputs_cadastro()
                self.carregar_tutores()
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar tutor: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def editar_tutor(self):
        tutor_id = self.lista_tutores.currentItem().tutor_id
        
        data = {
            'nome': self.input_nome_consulta.text(),
            'cpf': self.input_cpf_consulta.text(),
            'telefone': self.input_telefone_consulta.text(),
            'email': self.input_email_consulta.text(),
            'endereco': self.input_endereco_consulta.text(),
            'data_nascimento': self.input_data_nascimento_consulta.text()
        }
        
        try:
            response = requests.put(f'http://127.0.0.1:5000/tutores/tutores/{tutor_id}', json=data)
            
            if response.status_code == 200:
                QMessageBox.information(self, 'Sucesso', 'Tutor editado com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_tutores()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao editar tutor: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def excluir_tutor(self):
        tutor_id = self.lista_tutores.currentItem().tutor_id
        
        try:
            response = requests.delete(f'http://127.0.0.1:5000/tutores/tutores/{tutor_id}')
            
            if response.status_code == 204:
                QMessageBox.information(self, 'Sucesso', 'Tutor excluído com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_tutores()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao excluir tutor: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')

    def apply_styles(self):
        style = """
        QListWidget {
            background-image: url('img/vet.png');
            background-repeat: no-repeat;
            background-position: center;
        }
        """
        self.lista_tutores.setStyleSheet(style)
