from typing import Optional, Union
import readline

commands = {
    'ni': [],
    'next': [],
    'step': [],
    'step-to': [],
    'start': [],
    'run': [],
    'export': [],
    '?': [],
    'exit': [],
    'quit': [],
    'set': {
        'step-verbose': ['true', 'false']
    },
    'show': ['options'],
    'help': ['options']
}


def completer(text: str, state: int) -> Optional[str]:
    """Completer function for readline to provide command completion.
    
    Args:
        text (str): The current text being completed.
        state (int): The state of the completion, used to iterate through options.

    Returns:
        Optional[str]: The next completion option or None if no more options are available.
    """
    buffer = readline.get_line_buffer().split()
    
    def get_options(cmd_tree: Union[dict, list], tokens: list[str], current_text: str) -> list[str]:
        # we only have a list of valid leaf commands
        if isinstance(cmd_tree, list):
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]
        
        if not tokens:
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]

        token = tokens[0]
        rest = tokens[1:]
        next_branch = cmd_tree.get(token)

        if next_branch is None:
            return [cmd for cmd in cmd_tree if cmd.startswith(current_text)]

        return get_options(next_branch, rest, current_text)
    
    options = get_options(commands, buffer, text)
    if state < len(options):
        return options[state]
    else:
        return None