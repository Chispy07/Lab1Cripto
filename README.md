# Lab1Cripto
Este es el Readme del Lab 1 de Criptografia y Seguridad de Redes el cual se dividira en 3 secciones la cual habla de cada codigo en este Repositorio de Github

- "cifrado.py": Este codigo no tiene ninguna particularidad solo se ejecuta y el programa pedira una palabra para cifrar en cesar y luego pide el desplazamiento y devuelve la palabra encriptada

- "ping.py":Este codigo tiene la gran particularidad de que funciona solo si se le aplica un "sudo" previamente para tener permisos de administrador y poder enviar los paquetes ICMP de la palabra que requerira el programa cabe destacar que las letras se envian de forma secuencial y con un delay entre ellas para que no se pierdan en el camino o no queden encolados

- "MitM.py": Este codigo tiene dos grandes particularidades

1. Funciona solo con un "sudo"

2. Funciona con un archivo ".pcapng" el cual debera tener paquetes ICMP en la captura de Wireshark

   Su funcionamiento es de la siguiente manera se entrega y dentro del codigo se anota cual es la captura a revisar y este revisa la captura ICMP junta las letras y itera todas las formas posibles del cesar en todos los desplazamientos y la API de Gemini se encarga de seleccionar la que sea el mensaje cabe recalcar que tomara el mensaje que mas sentido tenga y que puede tener fallos ya que tampoco es una version muy buena de Gemini esta es la version Gemini-1.5-Flash.
