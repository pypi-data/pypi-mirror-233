colors = {
    'none': "\033[0m",
    'black': "\033[0;30m",
    'dark_gray': "\033[1;30m",
    'blue': "\033[0;34m",
    'light_blue': "\033[1;34m",
    'green': "\033[0;32m",
    'light_green': "\033[1;32m",
    'cyan': "\033[0;36m",
    'light_cyan': "\033[1;36m",
    'red': "\033[0;31m",
    'light_red': "\033[1;31m",
    'purple': "\033[0;35m",
    'light_purple': "\033[1;35m",
    'brown': "\033[0;33m",
    'yellow': "\033[1;33m",
    'light_gray': "\033[0;37m",
    'white': "\033[1;37m",
}


def info(color, message):
    result = 'info: '
    if (color in colors) and isinstance(message, str):
        result += colors[color] + message + '\033[0m'
        print(result)
    else:
        return False
    return True


if __name__ == '__main__':
    info('blue', 'hello')
