def cifrado_cesar(palabra, desplazamiento):
    resultado = ""

    for caracter in palabra:
        if 'a' <= caracter <= 'z':
            # Para minúsculas
            nueva_letra = chr(((ord(caracter) - ord('a') + desplazamiento) % 26) + ord('a'))
            resultado += nueva_letra
        elif 'A' <= caracter <= 'Z':
            # Para mayúsculas
            nueva_letra = chr(((ord(caracter) - ord('A') + desplazamiento) % 26) + ord('A'))
            resultado += nueva_letra
        else:
            # Otros caracteres se dejan igual (números, signos, espacios, etc.)
            resultado += caracter

    return resultado

# Solicita entrada al usuario
palabra = input("Ingresa la palabra a cifrar: ")
desplazamiento = int(input("Ingresa el número de desplazamiento: "))

# Llama a la función y muestra el resultado
resultado_cifrado = cifrado_cesar(palabra, desplazamiento)
print("Texto cifrado:", resultado_cifrado)
