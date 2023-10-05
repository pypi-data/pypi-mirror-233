import random


def encode(cadena):
    nueva_cadena = ""
    for caracter in cadena:
        if caracter == 'a':
          caracter_nuevo = '$'
          nueva_cadena += caracter_nuevo
        elif caracter == 'e':
          caracter_nuevo = '@'
          nueva_cadena += caracter_nuevo
        elif caracter == 'i':
          caracter_nuevo = '#'
          nueva_cadena += caracter_nuevo
        elif caracter == 'o':
          caracter_nuevo = '!'
          nueva_cadena +=caracter_nuevo
        elif caracter == 'u':
          caracter_nuevo = '%'
          nueva_cadena +=caracter_nuevo
        elif caracter == '1':
          caracter_nuevo = '&'
          nueva_cadena += caracter_nuevo
        elif caracter == '2':
          caracter_nuevo = '^'
          nueva_cadena += caracter_nuevo
        elif caracter == '3':
          caracter_nuevo = '?'
          nueva_cadena += caracter_nuevo
        elif caracter == '4':
          caracter_nuevo = '-'
          nueva_cadena += caracter_nuevo
        elif caracter == '5':
          caracter_nuevo = '{'
          nueva_cadena += caracter_nuevo
        elif caracter == '6':
          caracter_nuevo = '}'
          nueva_cadena += caracter_nuevo
        elif caracter == '7':
          caracter_nuevo = '['
          nueva_cadena += caracter_nuevo
        elif caracter == '8':
          caracter_nuevo = ']'
          nueva_cadena += caracter_nuevo
        elif caracter == '9':
          caracter_nuevo = '¿'
          nueva_cadena += caracter_nuevo
        else:
          nueva_cadena+=caracter
    
    secret_key = random.choice('01')+random.choice('df')+random.choice('hj')+random.choice('$^')+random.choice('%')+random.choice('#@')+random.choice('!?')+random.choice('-_')+random.choice('&f')+random.choice('vb')+'.'+'L0123'
    encripted = nueva_cadena+'.'+secret_key
    return encripted



def decode(cadena):
    nueva_cadena = ""
    for caracter in cadena:
        if caracter == '$':
          caracter_nuevo = 'a'
          nueva_cadena += caracter_nuevo
        elif caracter == '@':
          caracter_nuevo = 'e'
          nueva_cadena += caracter_nuevo
        elif caracter == '#':
          caracter_nuevo = 'i'
          nueva_cadena += caracter_nuevo
        elif caracter == '!':
          caracter_nuevo = 'o'
          nueva_cadena +=caracter_nuevo
        elif caracter == '%':
          caracter_nuevo = 'u'
          nueva_cadena +=caracter_nuevo
        elif caracter == '&':
          caracter_nuevo = '1'
          nueva_cadena += caracter_nuevo
        elif caracter == '^':
          caracter_nuevo = '2'
          nueva_cadena += caracter_nuevo
        elif caracter == '?':
          caracter_nuevo = '3'
          nueva_cadena += caracter_nuevo
        elif caracter == '-':
          caracter_nuevo = '4'
          nueva_cadena += caracter_nuevo
        elif caracter == '{':
          caracter_nuevo = '5'
          nueva_cadena += caracter_nuevo
        elif caracter == '}':
          caracter_nuevo = '6'
          nueva_cadena += caracter_nuevo
        elif caracter == '[':
          caracter_nuevo = '7'
          nueva_cadena += caracter_nuevo
        elif caracter == ']':
          caracter_nuevo = '8'
          nueva_cadena += caracter_nuevo
        elif caracter == '¿':
          caracter_nuevo = '9'
          nueva_cadena += caracter_nuevo
        elif caracter == '.':
          break
        else:
          nueva_cadena+=caracter

    return nueva_cadena
