import readline

def create_list_completer(values):
    """ 
    This is a closure that creates a method that autocompletes from
    the given list. Must set readline options to allow tab completions with:

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(create_list_completer(values))
    """
    def list_completer(text, state):
        line = readline.get_line_buffer()
        if not line:
            return [x for x in values][state]
        else:
            return [x for x in values if x.startswith(line)][state]
    return list_completer

if __name__=="__main__":
    players = ["Lebron James","Chris Paul", "Kobe Bryant"]
    readline.set_completer(create_list_completer(players))
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")

    response = raw_input("Input player name?\n")
    print response
