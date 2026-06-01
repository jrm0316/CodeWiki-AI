from utils import somar
from database import conectar

conectar()
resultado = somar(10, 20)
print(resultado)
