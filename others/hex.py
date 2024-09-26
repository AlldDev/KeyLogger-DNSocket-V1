texto = "Pythoné"
hexadecimal = ''.join([hex(ord(c)) for c in texto])
hexadecimal = hexadecimal.replace('0x', '')
print(hexadecimal)

hex_values = hexadecimal
result_string = ''.join([chr(int(hex_values[i:i+2], 16)) for i in range(0, len(hex_values), 2)])
 
print(result_string)