colors = {
    "normal"         : "\033[0m",
    "gray"           : "\033[1;38;5;240m",
    "light_gray"     : "\033[0;37m",
    "red"            : "\033[31m",
    "green"          : "\033[32m",
    "yellow"         : "\033[33m",
    "blue"           : "\033[34m",
    "pink"           : "\033[35m",
    "cyan"           : "\033[36m",
    "bold"           : "\033[1m",
    "underline"      : "\033[4m",
    "underline_off"  : "\033[24m",
    "highlight"      : "\033[3m",
    "highlight_off"  : "\033[23m",
    "blink"          : "\033[5m",
    "blink_off"      : "\033[25m",
}


def colorify(text: str, attrs: str) -> str:
    msg = [colors[attr] for attr in attrs.split() if attr in colors]
    msg.append(str(text))
    if colors["highlight"] in msg:   msg.append(colors["highlight_off"])
    if colors["underline"] in msg:   msg.append(colors["underline_off"])
    if colors["blink"] in msg:       msg.append(colors["blink_off"])
    msg.append(colors["normal"])
    return "".join(msg)

def redify(msg: str) -> str:        return colorify(msg, "red")

def greenify(msg: str) -> str:      return colorify(msg, "green")

def blueify(msg: str) -> str:       return colorify(msg, "blue")

def yellowify(msg: str) -> str:     return colorify(msg, "yellow")

def grayify(msg: str) -> str:       return colorify(msg, "gray")

def light_grayify(msg: str) -> str: return colorify(msg, "light_gray")

def pinkify(msg: str) -> str:       return colorify(msg, "pink")

def cyanify(msg: str) -> str:       return colorify(msg, "cyan")

def boldify(msg: str) -> str:       return colorify(msg, "bold")

def underlinify(msg: str) -> str:   return colorify(msg, "underline")

def highlightify(msg: str) -> str:  return colorify(msg, "highlight")

def blinkify(msg: str) -> str:      return colorify(msg, "blink")

def colorize_array(arr: list|tuple) -> str:
    if type(arr) == list:
        BEGIN = '['
        END = ']'
    elif type(arr) == tuple:
        BEGIN = '('
        END = ')'

    retval = BEGIN

    for element in arr:
        if type(element) == str or type(element) == bytes:
            retval += pinkify(ascii(element))+", "
        elif type(element) == dict:
            retval += ascii(element)+", "
        elif type(element) == int or type(element) == float:
            retval += cyanify(ascii(element))+", "
        elif type(element) == list or type(element) == tuple:
            retval += colorize_array(element)+", "
        elif type(element) == dict:
            retval += colorize_dict(arr[element])+", "
        elif element == None:
            retval += blueify(ascii(element))+", "
        else:
            retval += yellowify(ascii(element))+", "

    if retval != BEGIN:
        retval = retval[:-2]+END
    else:
        retval += END

    return retval

def colorize_dict(arr: dict) -> str:
    retval = '{'

    for element in arr:
        retval += ascii(element)+": "


        if type(arr[element]) == str or type(arr[element]) == bytes:
            retval += pinkify(ascii(arr[element]))+", "
        elif type(arr[element]) == dict:
            retval += ascii(arr[element])+", "
        elif type(arr[element]) == int or type(arr[element]) == float:
            retval += cyanify(ascii(arr[element]))+", "
        elif type(arr[element]) == list or type(arr[element]) == tuple:
            retval += colorize_array(arr[element])+", "
        elif type(arr[element]) == dict:
            retval += colorize_dict(arr[element])+", "
        elif arr[element] == None:
            retval += blueify(ascii(arr[element]))+", "
        else:
            retval += yellowify(ascii(arr[element]))+", "

    if retval != '{':
        retval = retval[:-2]+'}'
    else:
        retval += '}'

    return retval