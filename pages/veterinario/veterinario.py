from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTabWidget, QFormLayout, QListWidget, QListWidgetItem, QHBoxLayout
import requests

class TelaVeterinario(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Cadastro e Consulta de Veterinários')
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tab_cadastro = QWidget()
        self.tab_consulta = QWidget()
        
        self.tabs.addTab(self.tab_cadastro, 'Cadastro')
        self.tabs.addTab(self.tab_consulta, 'Consulta')
        
        self.init_tab_cadastro()
        self.init_tab_consulta()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def init_tab_cadastro(self):
        layout = QFormLayout()
        
        self.label_nome_cad = QLabel('Nome:')
        self.input_nome_cad = QLineEdit()
        self.label_cpf_cad = QLabel('CPF:')
        self.input_cpf_cad = QLineEdit()
        self.label_telefone_cad = QLabel('Telefone:')
        self.input_telefone_cad = QLineEdit()
        self.label_email_cad = QLabel('Email:')
        self.input_email_cad = QLineEdit()
        
        layout.addRow(self.label_nome_cad, self.input_nome_cad)
        layout.addRow(self.label_cpf_cad, self.input_cpf_cad)
        layout.addRow(self.label_telefone_cad, self.input_telefone_cad)
        layout.addRow(self.label_email_cad, self.input_email_cad)
        
        self.btn_cadastrar_cad = QPushButton('Cadastrar')
        self.btn_cadastrar_cad.clicked.connect(self.cadastrar_veterinario)
        
        layout.addRow(self.btn_cadastrar_cad)
        
        self.tab_cadastro.setLayout(layout)
    
    def init_tab_consulta(self):
        layout = QVBoxLayout()
        
        self.lista_veterinarios = QListWidget()
        self.lista_veterinarios.itemClicked.connect(self.item_selecionado_consulta)
        
        self.carregar_veterinarios()
        self.apply_styles()
        
        layout.addWidget(self.lista_veterinarios)
        
        form_layout = QFormLayout()
        
        self.label_nome_cons = QLabel('Nome:')
        self.input_nome_cons = QLineEdit()
        self.label_cpf_cons = QLabel('CPF:')
        self.input_cpf_cons = QLineEdit()
        self.label_telefone_cons = QLabel('Telefone:')
        self.input_telefone_cons = QLineEdit()
        self.label_email_cons = QLabel('Email:')
        self.input_email_cons = QLineEdit()
        
        form_layout.addRow(self.label_nome_cons, self.input_nome_cons)
        form_layout.addRow(self.label_cpf_cons, self.input_cpf_cons)
        form_layout.addRow(self.label_telefone_cons, self.input_telefone_cons)
        form_layout.addRow(self.label_email_cons, self.input_email_cons)
        
        botoes_layout = QHBoxLayout()
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setEnabled(False)
        self.btn_editar.clicked.connect(self.editar_veterinario)
        
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.setEnabled(False)
        self.btn_excluir.clicked.connect(self.excluir_veterinario)
        
        botoes_layout.addWidget(self.btn_editar)
        botoes_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(form_layout)
        layout.addLayout(botoes_layout)
        
        self.tab_consulta.setLayout(layout)
    
    def clear_inputs(self):
        self.input_nome_cad.clear()
        self.input_cpf_cad.clear()
        self.input_telefone_cad.clear()
        self.input_email_cad.clear()
    
    def carregar_veterinarios(self):
        self.lista_veterinarios.clear()
        
        try:
            response = requests.get('http://127.0.0.1:5000/veterinarios/veterinarios')
            
            if response.status_code == 200:
                veterinarios = response.json()
                for veterinario in veterinarios:
                    item = QListWidgetItem(f"{veterinario['id']} - {veterinario['nome']} ({veterinario['cpf']})")
                    item.veterinario_id = veterinario['id']  
                    self.lista_veterinarios.addItem(item)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao carregar veterinários: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def item_selecionado_consulta(self, item):
        self.veterinario_selecionado = item.veterinario_id
        
        try:
            response = requests.get(f'http://127.0.0.1:5000/veterinarios/veterinarios/{self.veterinario_selecionado}')
            
            if response.status_code == 200:
                veterinario = response.json()
                self.input_nome_cons.setText(veterinario['nome'])
                self.input_cpf_cons.setText(veterinario['cpf'])
                self.input_telefone_cons.setText(veterinario['telefone'])
                self.input_email_cons.setText(veterinario['email'])
                self.btn_editar.setEnabled(True)
                self.btn_excluir.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao selecionar veterinário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def editar_veterinario(self):
        data = {
            'nome': self.input_nome_cons.text(),
            'cpf': self.input_cpf_cons.text(),
            'telefone': self.input_telefone_cons.text(),
            'email': self.input_email_cons.text(),
        }
        
        try:
            response = requests.put(f'http://127.0.0.1:5000/veterinarios/veterinarios/{self.veterinario_selecionado}', json=data)
            
            if response.status_code == 200:
                QMessageBox.information(self, 'Sucesso', 'Veterinário editado com sucesso!')
                self.carregar_veterinarios() 
                self.clear_inputs()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao editar veterinário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def excluir_veterinario(self):
        try:
            response = requests.delete(f'http://127.0.0.1:5000/veterinarios/veterinarios/{self.veterinario_selecionado}')
            
            if response.status_code == 204:
                QMessageBox.information(self, 'Sucesso', 'Veterinário excluído com sucesso!')
                self.carregar_veterinarios()  
                self.clear_inputs()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao excluir veterinário: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def cadastrar_veterinario(self):
        data = {
            'nome': self.input_nome_cad.text(),
            'cpf': self.input_cpf_cad.text(),
            'telefone': self.input_telefone_cad.text(),
            'email': self.input_email_cad.text(),
            'tipo': 'veterinario'
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/veterinarios/veterinarios', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Sucesso', 'Veterinário cadastrado com sucesso!')
                self.clear_inputs()
                self.carregar_veterinarios()  
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar veterinário: {response.text}')
        
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
        self.lista_veterinarios.setStyleSheet(style)
