import re
from datetime import datetime
from .exceptions import ValidationError

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, str(cpf)))   # Não aceita caracteres não numéricos
    if len(cpf) != 11 or not cpf.isdigit():        # CPF deve ter 11 dígitos
        raise ValidationError("CPF inválido.")     
    if cpf == cpf[0] * len(cpf):
        raise ValidationError("CPF inválido.")
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i))) # O calculo dos dígitos verificadores precisa ser valido
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError("CPF inválido.")
    return cpf

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d') #Data precisa ser no formato americano
    except ValueError:
        raise ValidationError("Data inválida. Use o formato YYYY-MM-DD.")

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' #O e-mail precisa ter um @ e um .
    if not re.match(email_regex, email):
        raise ValidationError("E-mail inválido.")
    return email

def validate_phone(phone):
    phone_regex = r'^\+?[1-9]\d{1,14}$'     #O telefone precisa ter pelo menos 1 dígito e até 15 dígitos
    if not re.match(phone_regex, phone):    #Não aceita caracteres não numéricos
        raise ValidationError("Telefone inválido.")
    return phone

def validate_nome(nome):
    if not nome or len(nome) < 2:                # O nome precisa ter pelo menos 2 caracteres
        raise ValidationError("Nome inválido.")
    if any(char.isdigit() for char in nome):     # O nome não pode conter dígito numérico
        raise ValidationError("Nome não pode conter números.")
    return nome

def validate_endereco(endereco):     
    if not endereco or len(endereco) < 5:           #O endereço precisa ter pelo menos 5 caracteres
        raise ValidationError("Endereço inválido.")
    return endereco
