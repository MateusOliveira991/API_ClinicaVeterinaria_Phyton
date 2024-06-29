from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTabWidget, QListWidget, QFormLayout, QListWidgetItem
import requests

class TelaAnimal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Cadastro e Consulta de Animais')
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
        
        self.label_id_tutor_cadastro = QLabel('ID do Tutor:')
        self.input_id_tutor_cadastro = QLineEdit()
        self.label_nome_cadastro = QLabel('Nome:')
        self.input_nome_cadastro = QLineEdit()
        self.label_especie_cadastro = QLabel('Espécie:')
        self.input_especie_cadastro = QLineEdit()
        self.label_raca_cadastro = QLabel('Raça:')
        self.input_raca_cadastro = QLineEdit()
        self.label_sexo_cadastro = QLabel('Sexo:')
        self.input_sexo_cadastro = QLineEdit()
        self.label_data_nascimento_cadastro = QLabel('Data de Nascimento:')
        self.input_data_nascimento_cadastro = QLineEdit()
        self.label_descricao_cadastro = QLabel('Descrição:')
        self.input_descricao_cadastro = QLineEdit()
        
        self.btn_cadastrar = QPushButton('Cadastrar')
        
        layout.addRow(self.label_id_tutor_cadastro, self.input_id_tutor_cadastro)
        layout.addRow(self.label_nome_cadastro, self.input_nome_cadastro)
        layout.addRow(self.label_especie_cadastro, self.input_especie_cadastro)
        layout.addRow(self.label_raca_cadastro, self.input_raca_cadastro)
        layout.addRow(self.label_sexo_cadastro, self.input_sexo_cadastro)
        layout.addRow(self.label_data_nascimento_cadastro, self.input_data_nascimento_cadastro)
        layout.addRow(self.label_descricao_cadastro, self.input_descricao_cadastro)
        layout.addRow(self.btn_cadastrar)
        
        self.tab_cadastro.setLayout(layout)
        
        self.btn_cadastrar.clicked.connect(self.cadastrar_animal)
    
    def initTabConsulta(self):
        layout = QFormLayout()
        
        self.lista_animais = QListWidget()
        self.lista_animais.itemClicked.connect(self.item_selecionado)
        
        self.label_id_tutor_consulta = QLabel('ID do Tutor:')
        self.input_id_tutor_consulta = QLineEdit()
        self.label_nome_consulta = QLabel('Nome:')
        self.input_nome_consulta = QLineEdit()
        self.label_especie_consulta = QLabel('Espécie:')
        self.input_especie_consulta = QLineEdit()
        self.label_raca_consulta = QLabel('Raça:')
        self.input_raca_consulta = QLineEdit()
        self.label_sexo_consulta = QLabel('Sexo:')
        self.input_sexo_consulta = QLineEdit()
        self.label_data_nascimento_consulta = QLabel('Data de Nascimento:')
        self.input_data_nascimento_consulta = QLineEdit()
        self.label_descricao_consulta = QLabel('Descrição:')
        self.input_descricao_consulta = QLineEdit()
        
        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setEnabled(False)
        self.btn_excluir = QPushButton('Excluir')
        self.btn_excluir.setEnabled(False)
        
        layout.addRow(self.lista_animais)
        layout.addRow(self.label_id_tutor_consulta, self.input_id_tutor_consulta)
        layout.addRow(self.label_nome_consulta, self.input_nome_consulta)
        layout.addRow(self.label_especie_consulta, self.input_especie_consulta)
        layout.addRow(self.label_raca_consulta, self.input_raca_consulta)
        layout.addRow(self.label_sexo_consulta, self.input_sexo_consulta)
        layout.addRow(self.label_data_nascimento_consulta, self.input_data_nascimento_consulta)
        layout.addRow(self.label_descricao_consulta, self.input_descricao_consulta)
        layout.addRow(self.btn_editar, self.btn_excluir)
        
        self.tab_consulta.setLayout(layout)
        
        self.btn_editar.clicked.connect(self.editar_animal)
        self.btn_excluir.clicked.connect(self.excluir_animal)
        
        self.carregar_animais()
    
    def clear_inputs_cadastro(self):
        self.input_id_tutor_cadastro.clear()
        self.input_nome_cadastro.clear()
        self.input_especie_cadastro.clear()
        self.input_raca_cadastro.clear()
        self.input_sexo_cadastro.clear()
        self.input_data_nascimento_cadastro.clear()
        self.input_descricao_cadastro.clear()
    
    def clear_inputs_consulta(self):
        self.input_id_tutor_consulta.clear()
        self.input_nome_consulta.clear()
        self.input_especie_consulta.clear()
        self.input_raca_consulta.clear()
        self.input_sexo_consulta.clear()
        self.input_data_nascimento_consulta.clear()
        self.input_descricao_consulta.clear()
    
    def carregar_animais(self):
        self.lista_animais.clear()
        self.apply_styles()
        
        try:
            response = requests.get('http://127.0.0.1:5000/animais/animais')
            
            if response.status_code == 200:
                animais = response.json()
                for animal in animais:
                    item = QListWidgetItem(f"{animal['id']} - {animal['nome']} ({animal['especie']})")
                    item.animal_id = animal['id']
                    self.lista_animais.addItem(item)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao carregar animais: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def item_selecionado(self, item):
        animal_id = item.animal_id
        
        try:
            response = requests.get(f'http://127.0.0.1:5000/animais/animais/{animal_id}')
            
            if response.status_code == 200:
                animal = response.json()
                self.input_id_tutor_consulta.setText(str(animal['id_tutor']))
                self.input_nome_consulta.setText(animal['nome'])
                self.input_especie_consulta.setText(animal['especie'])
                self.input_raca_consulta.setText(animal['raca'])
                self.input_sexo_consulta.setText(animal['sexo'])
                self.input_data_nascimento_consulta.setText(animal['data_nascimento'])
                self.input_descricao_consulta.setText(animal['descricao'])
                self.btn_editar.setEnabled(True)
                self.btn_excluir.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao selecionar animal: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def cadastrar_animal(self):
        data = {
            'id_tutor': self.input_id_tutor_cadastro.text(),
            'nome': self.input_nome_cadastro.text(),
            'especie': self.input_especie_cadastro.text(),
            'raca': self.input_raca_cadastro.text(),
            'sexo': self.input_sexo_cadastro.text(),
            'data_nascimento': self.input_data_nascimento_cadastro.text(),
            'descricao': self.input_descricao_cadastro.text()
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/animais/animais', json=data)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Sucesso', 'Animal cadastrado com sucesso!')
                self.clear_inputs_cadastro()
                self.carregar_animais()
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao cadastrar animal: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def editar_animal(self):
        animal_id = self.lista_animais.currentItem().animal_id
        
        data = {
            'id_tutor': self.input_id_tutor_consulta.text(),
            'nome': self.input_nome_consulta.text(),
            'especie': self.input_especie_consulta.text(),
            'raca': self.input_raca_consulta.text(),
            'sexo': self.input_sexo_consulta.text(),
            'data_nascimento': self.input_data_nascimento_consulta.text(),
            'descricao': self.input_descricao_consulta.text()
        }
        
        try:
            response = requests.put(f'http://127.0.0.1:5000/animais/animais/{animal_id}', json=data)
            
            if response.status_code == 200:
                QMessageBox.information(self, 'Sucesso', 'Animal editado com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_animais()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao editar animal: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def excluir_animal(self):
        animal_id = self.lista_animais.currentItem().animal_id
        
        try:
            response = requests.delete(f'http://127.0.0.1:5000/animais/animais/{animal_id}')
            
            if response.status_code == 204:
                QMessageBox.information(self, 'Sucesso', 'Animal excluído com sucesso!')
                self.clear_inputs_consulta()
                self.carregar_animais()
                self.btn_editar.setEnabled(False)
                self.btn_excluir.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Erro', f'Erro ao excluir animal: {response.text}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Erro', 'Falha ao conectar ao servidor. Verifique se o servidor está rodando e acessível.')
    
    def apply_styles(self):
        style = """
       QWidget{
            background-image: url('img/vet.png');
            background-repeat: no-repeat;
            background-position: center;
    }
    """
        self.lista_animais.setStyleSheet(style)

