import google.generativeai as genai
import os
import textwrap
import scapy.all as scapy

# Configura tu clave de API de Gemini desde una variable de entorno
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise KeyError("La variable de entorno no está configurada.")
    
    genai.configure(api_key=api_key)
except KeyError as e:
    print(f"Error: {e}")
    print("Por favor, configura tu clave de API para continuar.")
    exit()

def cesar_decrypt(text, shift):
    """Desencripta un texto con un desplazamiento de César"""
    resultado = []
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            resultado.append(chr((ord(char) - ord(base) - shift) % 26 + ord(base)))
        else:
            resultado.append(char)
    return "".join(resultado)

def analizar_texto(texto):
    """Pregunta a la IA si el texto está en claro o cifrado con César"""
    prompt = f"""
Analiza el siguiente texto: "{texto}"

1. Si ya es un texto en español claro, responde: "El texto ya está en claro".
2. Si parece estar cifrado con un cifrado César, responde: "El texto está cifrado con César".
Solo responde con una de esas dos frases.
"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error al contactar con la API: {e}"

def descifrar_cesar_con_ia(texto):
    """Genera los 26 posibles descifrados y deja que la IA elija el correcto"""
    candidatos = [f"Shift {s}: {cesar_decrypt(texto, s)}" for s in range(26)]

    prompt = f"""
Este texto parece estar cifrado con César.
Aquí tienes los 26 posibles descifrados. 
Elige cuál es el texto válido en español y devuelve:
1. El desplazamiento correcto.
2. El texto descifrado.

Candidatos:
{chr(10).join(candidatos)}
"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error al contactar con la API: {e}"

def leer_pcap_y_obtener_payload(nombre_archivo):
    """
    Lee un archivo .pcap o .pcapng, busca paquetes ICMP y concatena
    la carga útil de todos ellos para reconstruir el mensaje completo.
    """
    try:
        print(f"[*] Leyendo el archivo de captura: {nombre_archivo}")
        paquetes = scapy.rdpcap(nombre_archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
        print("Asegúrate de que está en la misma carpeta que el script.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

    mensaje_partes = []
    for paquete in paquetes:
        # Filtra para obtener solo paquetes ICMP de tipo Echo Request (tipo 8)
        if paquete.haslayer(scapy.ICMP) and paquete[scapy.ICMP].type == 8:
            if paquete.haslayer(scapy.Raw):
                try:
                    # Intenta decodificar la carga útil como texto y añadirla a la lista.
                    payload = paquete[scapy.ICMP].load.decode('utf-8')
                    mensaje_partes.append(payload)
                except UnicodeDecodeError:
                    # Ignora los paquetes que no tienen texto UTF-8.
                    continue
    
    if not mensaje_partes:
        print("[!] No se encontró un paquete ICMP con datos de texto en el archivo.")
        return None
    
    # Une todas las partes para formar el mensaje completo.
    mensaje_completo = "".join(mensaje_partes)
    return mensaje_completo

if __name__ == "__main__":
    # Nombre del archivo de captura de Wireshark.
    archivo_pcap = "mensaje.pcapng"

    mensaje_extraido = leer_pcap_y_obtener_payload(archivo_pcap)

    if mensaje_extraido:
        print(f"\n[+] Texto extraído de la 'carga útil del paquete': {mensaje_extraido}\n")
    
        estado = analizar_texto(mensaje_extraido)
    
        if "cifrado con César" in estado:
            print("[*] El texto parece estar cifrado con César. Descifrando...\n")
            resultado = descifrar_cesar_con_ia(mensaje_extraido)
            print("[✓] Resultado de Gemini:")
            print(textwrap.fill(resultado, width=80))
        elif "El texto ya está en claro" in estado:
            print("[✓] El texto ya está en claro:")
            print(mensaje_extraido)
        else:
            print("[!] No se pudo determinar el estado del texto.")
            print(f"Respuesta de la IA: {estado}")
    else:
        print("[!] Proceso terminado. No se pudo obtener el mensaje.")
