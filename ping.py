from scapy.all import IP, ICMP, sr1
import time

def send_string_icmp(target_ip, text):
    print(f"[+] Enviando el string '{text}' hacia {target_ip} usando ICMP...")
    
    for idx, char in enumerate(text):
        # Crear paquete con un solo caracter en el payload
        pkt = IP(dst=target_ip)/ICMP()/char.encode()

        print(f"[*] Enviando letra {idx+1}/{len(text)}: '{char}'")
        reply = sr1(pkt, timeout=2, verbose=0)

        if reply:
            print(f"[✓] Llegó respuesta desde {reply.src} (letra: '{char}')")
        else:
            print(f"[x] No se recibió respuesta para la letra '{char}'")

        time.sleep(0.5)  # pequeña pausa para no saturar

if __name__ == "__main__":
    destino = "8.8.8.8"   # Cambia al host de destino
    mensaje = input("Escriba su mensaje")
    send_string_icmp(destino, mensaje)
