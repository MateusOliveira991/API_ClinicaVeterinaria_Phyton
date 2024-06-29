#Os controladores são responsáveis por receber as requisições dos clientes, roteá-las para o serviço apropriado e retornar as respostas adequadas. Eles atuam como intermediários entre as requisições HTTP e a lógica de negócios da aplicação. Os controladores geralmente realizam a validação dos dados de entrada, chamam os métodos apropriados nos serviços para realizar as operações necessárias e formatam as respostas para serem retornadas ao cliente. 

from .tutor_controller import tutor_bp
from .veterinario_controller import veterinario_bp
from .consulta_controller import consulta_bp
from .animal_controller import animal_bp
from .estagiario_controller import estagiario_bp