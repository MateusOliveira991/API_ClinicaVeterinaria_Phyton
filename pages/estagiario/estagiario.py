from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTabWidget, QListWidget, QFormLayout, QListWidgetItem
import requests

class TelaEstagiario(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Cadastro e Consulta de Estagiários')
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
        
        self.btn_cadastrar = QPushButton('Cadastrar')
        
        layout.addRow(self.label_nome_cadastro, self.input_nome_cadastro)
        layout.addRow(self.label_cpf_cadastro, self.input_cpf_cadastro)
        layout.addRow(self.label_telefone_cadastro, self.input_telefone_cadastro)
        layout.addRow(self.label_email_cadastro, self.input_email_cadastro)
        layout.addRow(self.btn_cadastrar)
        
        self.tab_cadastro.setLayout(layout)
        
        self.btn_cadastrar.clicked.connect(self.cadastrar_estagiario)
    
    def initTabConsulta(self):
        layout = QFormLayout()
        
        self.lista_estagiarios = QListWidget()
        self.lista_estagiarios.itemClicked.connect(self.item_selecionado)
        
        self.label_nome_consulta = QLabel('Nome:')
        self.input_nome_consulta = QLineEdit()
        self.label_cpf_consulta = QLabel('CPF:')
        self.input_cpf_consulta = QLineEdit()
        self.label_telefone_consulta = QLabel('Telefone:')
        self.input_telefone_consulta = QLineEdit()
        self.label_email_consulta = QLabel('Email:')
        self.input_email_consulta = QLineEdit()
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setEnabled(False)
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.setEnabled(False)
        
        layout.addRow(self.lista_estagiarios)
        layout.addRow(self.label_nome_consulta, self.input_nome_consulta)
        layout.addRow(self.label_cpf_consulta, self.input_cpf_consulta)
        layout.addRow(self.label_telefone_consulta, self.input_telefone_consulta)
        layout.addRow(self.label_email_consulta, self.input_email_consulta)
        layout.addRow(self.btn_editar, self.btn_excluir)
        
        self.tab_consulta.setLayout(layout)
        
        self.btn_editar.clicked.connect(self.editar_estagiario)
        self.btn_excluir.clicked.connect(self.excluir_estagiario)
        
        self.carregar_estagiarios()
    
    def clear_inputs_cadastro(self):
        self.input_nome_cadastro.clear()
        self.input_cpf_cadastro.clear()
        self.input_telefone_cadastro.clear()
        self.input_email_cadastro.clear()
    
    def clear_inputs_consulta(self):
        self.input_nome_consulta.clear()
        self.input_cpf_consulta.clear()
        self.input_telefone_consulta.clear()
        self.input_email_consulta.clear()
    
    def carregar_estagiarios(self):
        self.lista_estagiarios.clear()
        self.apply_styles()
        
        try:
            response = requests.get('http://127.0.0.1:5000/estagiarios/estagiarios')
            
            if response.status_code == 200:
                estagiarios = response.json()
                for estagiario in estagiarios:
                    item = QListWidgetItem(f"{estagiario['id']} - {estagiario['nome']} ({estagiario['cpf']})")
                    item.estagiario_id = estagiario['id']
                    self.lista_estagiarios.addItem(item)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao carregar estagiários: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def item_selecionado(self, item):
        estagiario_id = item.estagiario_id
        
        try:
            response = requests.get(f'http://127.0.0.1:5000/estagiarios/estagiarios/{estagiario_id}')
            
            if response.status_code == 200:
                estagiario = response.json()
                self.input_nome_consulta.setText(estagiario['nome'])
                self.input_cpf_consulta.setText(estagiario['cpf'])
                self.input_telefone_consulta.setText(estagiario['telefone'])
                self.input_email_consulta.setText(estagiario['email'])
                self.btn_editar.setEnabled(True)
                self.btn_excluir.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao selecionar estagiário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def cadastrar_estagiario(self):
        data = {
            'nome': self.input_nome_cadastro.text(),
            'cpf': self.input_cpf_cadastro.text(),
            'telefone': self.input_telefone_cadastro.text(),
            'email': self.input_email_cadastro.text(),
            'tipo': 'estagiario'
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/estagiarios/estagiarios', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Sucesso', 'Estagiário cadastrado com sucesso!')
                self.clear_inputs_cadastro()
                self.carregar_estagiarios()
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar estagiário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def editar_estagiario(self):
        estagiario_id = self.lista_estagiarios.currentItem().estagiario_id
        
        data = {
            'nome': self.input_nome_consulta.text(),
            'cpf': self.input_cpf_consulta.text(),
            'telefone': self.input_telefone_consulta.text(),
            'email': self.input_email_consulta.text()
        }
        
        try:
            response = requests.put(f'http://127.0.0.1:5000/estagiarios/estagiarios/{estagiario_id}', json=data)
            
            if response.status_code == 200:
                QMessageBox.information(self, 'Sucesso', 'Estagiário editado com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_estagiarios()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao editar estagiário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def excluir_estagiario(self):
        estagiario_id = self.lista_estagiarios.currentItem().estagiario_id
        
        try:
            response = requests.delete(f'http://127.0.0.1:5000/estagiarios/estagiarios/{estagiario_id}')
            
            if response.status_code == 204:
                QMessageBox.information(self, 'Sucesso', 'Estagiário excluído com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_estagiarios()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao excluir estagiário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')

    def apply_styles(self):
        self.lista_estagiarios.setStyleSheet("""
        QWidget {
            background-image: url('img/vet.png');
            background-repeat: no-repeat;
            background-position: center;
        }
        """)

        

