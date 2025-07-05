# Mapping of ANSI color codes to their respective escape sequences.
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
    """Returns a string with the given text colored according to the specified attributes.
    
    Args:
        text (str): The text to color.
        attrs (str): A space-separated string of attributes to apply, e.g., "red bold underline".
    Returns:
        str: The colored text string.
    """
    msg = [colors[attr] for attr in attrs.split() if attr in colors]
    msg.append(str(text))
    if colors["highlight"] in msg:   msg.append(colors["highlight_off"])
    if colors["underline"] in msg:   msg.append(colors["underline_off"])
    if colors["blink"] in msg:       msg.append(colors["blink_off"])
    msg.append(colors["normal"])
    return "".join(msg)


### Color-specific functions for convenience ###
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


def color_by_type(element, strip_comma=False) -> str:
    """Returns a string representation of an element with color based on its type.
    
    The following types are linked to specific colors:
    - str or bytes: pink
    - dict: cyan
    - int or float: cyan
    - list or tuple: yellow
    - None: blue
    - Other types: yellow
    
    Args:
        element: The element to colorize.
    Returns:
        str: The colored string representation of the element.
    """
    if strip_comma:
        end = ''
    else:
        end = ', '

    if type(element) == str or type(element) == bytes:
        return pinkify(ascii(element))+end

    elif type(element) == dict:
        return colorize_dict(element)+end

    elif type(element) == int or type(element) == float:
        return cyanify(ascii(element))+end

    elif type(element) == list or type(element) == tuple:
        return colorize_array(element)+end

    elif element == None:
        return blueify(ascii(element))+end

    else:
        return yellowify(ascii(element))+end


def colorize_array(arr: list|tuple) -> str:
    """Returns a string representation of an array or tuple with colored elements.

    Args:
        arr (list|tuple): The array or tuple to colorize.
    Returns:
        str: The colored string representation of the array or tuple.
    """
    if type(arr) == list:
        BEGIN = '['
        END = ']'
    elif type(arr) == tuple:
        BEGIN = '('
        END = ')'

    retval = BEGIN

    for element in arr:
        retval += color_by_type(element)

    # remove the last comma and space
    if retval != BEGIN:
        retval = retval[:-2]+END
    else:
        retval += END

    return retval


def colorize_dict(arr: dict) -> str:
    """Returns a string representation of a dictionary with colored keys and values.

    Args:
        arr (dict): The dictionary to colorize.
    Returns:
        str: The colored string representation of the dictionary.
    """
    retval = '{'

    for key, value in arr.items():
        retval += color_by_type(key, strip_comma=True)+': '
        retval += color_by_type(value)

    if retval != '{':
        retval = retval[:-2]+'}'
    else:
        retval += '}'

    return retval


def header(hdr_name: str, terminal_width: int) -> str:
    """Returns a header with the given name, formatted for the terminal width.
    
    Args:
        hdr_name (str): The name of the header to print.
        terminal_width (int): The width of the terminal.
    Returns:
        str: The formatted header string.
    """
    header = grayify(''.join(['─' for _ in range(terminal_width-5-len(hdr_name))])) +\
            cyanify(' '+hdr_name+' ') +\
            grayify('───')
    return header