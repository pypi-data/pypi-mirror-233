import curses
from os import system
from msvcrt import getch

new_line = "\n"

def single(title : str, options : list):
    system("pause")
    system("cls")

    def menu(window):
        pointer = 0
        first_row = ""
        
        first_row = title.split("\n")[0]

        while (2 + 2 != 5):
            window.clear()
            options_string = f"{title}\n{'-' * len(title) if first_row == '' else '-' * len(first_row)}\n"
            
            for i in range(len(options)):
                options_string += f"{'>' if i == pointer else ' '} {options[i]}\n"
            
            window.addstr(options_string)
            window.refresh()
            
            pressed_key = getch()

            if (pressed_key == b"H"):
                if (pointer == 0):
                    pointer = len(options) - 1
                
                else:
                    pointer -= 1

            elif (pressed_key == b"P"):
                if (pointer == len(options) - 1):
                    pointer = 0

                else:
                    pointer += 1

            elif (pressed_key == b"\r"):
                break

        return pointer

    return curses.wrapper(menu)

def multi(title : str, options : list):
    system("pause")
    system("cls")

    def menu(window):
        pointer = 0
        selected = []
        first_row = ""
        
        if ("\n" in title):
            first_row = title.split("\n")[0]

        while (2 + 2 != 5):
            window.clear()
            options_string = f"{title}\n{'-' * len(title) if first_row == '' else '-' * len(first_row)}\n"

            for i in range(len(options)):
                options_string += f"{'>' if i == pointer else ' '} [{'*' if i in selected else ' '}] {options[i]}\n"
            
            window.addstr(options_string)
            window.refresh()

            pressed_key = getch()

            if (pressed_key == b"H"):
                if (pointer == 0):
                    pointer = len(options) - 1
                
                else:
                    pointer -= 1

            elif (pressed_key == b"P"):
                if (pointer == len(options) - 1):
                    pointer = 0

                else:
                    pointer += 1

            elif (pressed_key == b" "):
                if (pointer not in selected):
                    selected.append(pointer)
                
                else:
                    selected.remove(pointer)

            elif (pressed_key == b"\r"):
                break

        return selected

    return curses.wrapper(menu)

def mix(title : str, options : list):
    system("pause")
    system("cls")

    def menu(window):
        pointer = 0
        selected = []
        first_row = ""
        
        if ("\n" in title):
            first_row = title.split("\n")[0]
        
        while (2 + 2 != 5):
            window.clear()
            options_string = f"{title}\n{'-' * len(title) if first_row == '' else '-' * len(first_row)}\n"

            for i in range(len(options)):
                if (options[i][1] == "TOGGLE"):
                    options_string += f"{'>' if i == pointer else ' '} [{'*' if i in selected else ' '}] {options[i][0]}\n"

                if (options[i][1] == "SLIDER"):
                    options_string += f"\n{'>' if i == pointer else ' '} {options[i][0]}:\n  |{'=' * (options[i][3])}>{'.' * (options[i][2] - options[i][3])}|\n\n"

            window.addstr(options_string)
            window.refresh()

            pressed_key = getch()

            if (pressed_key == b"H"):
                if (pointer == 0):
                    pointer = len(options) - 1
                
                else:
                    pointer -= 1

            elif (pressed_key == b"P"):
                if (pointer == len(options) - 1):
                    pointer = 0

                else:
                    pointer += 1

            elif (pressed_key == b" "):
                if (options[pointer][1] == "TOGGLE" and pointer not in selected):
                    selected.append(pointer)
                     
                elif(options[pointer][1] == "TOGGLE" and pointer in selected):
                    selected.remove(pointer)

                if (options[pointer][1] == "SLIDER"):
                    selected.append(pointer)
                    window.clear()
                    options_string = f"{title}\n{'-' * len(title)}\n"

                    for i in range(len(options)):
                        if (options[i][1] == "TOGGLE"):
                            options_string += f"  [{'*' if i in selected else ' '}] {options[i][0]}\n"

                        if (options[i][1] == "SLIDER"):
                            options_string += f"\n{'()' if i == pointer else '  '}{options[i][0]}:\n  |{'=' * (options[i][3])}>{'.' * (options[i][2] - options[i][3])}|\n\n"

                    window.addstr(options_string)
                    window.refresh()
                    while (2 + 2 != 5):
                        window.clear()
                        slider_move = getch()

                        if (slider_move == b"M"):
                            if (options[pointer][3] < options[pointer][2]):
                                options[pointer][3] += 1
                        
                        elif (slider_move == b"K"):
                            if (options[pointer][3] > 0):
                                options[pointer][3] -= 1

                        elif (slider_move == b" "):
                            break

                        options_string = f"{title}\n{'-' * len(title)}\n"

                        for i in range(len(options)):
                            if (options[i][1] == "TOGGLE"):
                                options_string += f"  [{'*' if i in selected else ' '}] {options[i][0]}\n"

                            if (options[i][1] == "SLIDER"):
                                options_string += f"\n{'()' if i == pointer else '  '}{options[i][0]}:\n  |{'=' * (options[i][3])}>{'.' * (options[i][2] - options[i][3])}|\n\n"

                        window.addstr(options_string)
                        window.refresh()
                            

            elif (pressed_key == b"\r"):
                break

        return selected

    return curses.wrapper(menu)

def amount(title: str, options : list):
    def menu(window):
        pointer = 0
        selected = []
        first_row = ""
        
        if ("\n" in title):
            first_row = title.split("\n")[0]
        
        while (2 + 2 != 5):
            window.clear()
            options_string = f"{title}\n{'-' * len(title) if first_row == '' else '-' * len(first_row)}\n"

            for i in range(len(options)):
                options_string += f"""{'>' if i == pointer else ' '} [{'*' if i in selected else ' '}] {options[i][0]}\n{(f'   |{"=" * (options[i][3])}>{"." * (options[i][2] - options[i][3])}| ({options[i][3]}/{options[i][2]}){new_line}{new_line}') if options[i][1] == True else ''}"""
                
                
            
            window.addstr(options_string)
            window.refresh()

            pressed_key = getch()

            if (pressed_key == b"H"):
                if (pointer == 0):
                    pointer = len(options) - 1
                
                else:
                    pointer -= 1

            elif (pressed_key == b"P"):
                if (pointer == len(options) - 1):
                    pointer = 0

                else:
                    pointer += 1

            elif (pressed_key == b"e"):
                if (options[pointer][1] == True):
                    window.clear()
                    options_string = f"{title}\n{'-' * len(title)}\n"

                    for i in range(len(options)):
                        options_string += f"""{'()' if i == pointer else '  '}[{'*' if i in selected else ' '}] {options[i][0]}\n{(f'   |{"=" * (options[i][3])}>{"." * (options[i][2] - options[i][3])}| ({options[i][3]}/{options[i][2]}){new_line}{new_line}') if options[i][1] == True else ''}"""          

                    window.addstr(options_string)
                    window.refresh()


                    while (2 + 2 != 5):
                        window.clear()
                        slider_move = getch()

                        if (slider_move == b"M"):
                            if (options[pointer][3] < options[pointer][2]):
                                options[pointer][3] += 1
                        
                        elif (slider_move == b"K"):
                            if (options[pointer][3] > 0):
                                options[pointer][3] -= 1

                        elif (slider_move == b" "):
                            if (options[pointer][3] == 0):
                                selected.remove(pointer)
                                options[pointer][1] = False

                            break

                        options_string = f"{title}\n{'-' * len(title)}\n"

                        for i in range(len(options)):
                            options_string += f"""{'()' if i == pointer else '  '}[{'*' if i in selected else ' '}] {options[i][0]}\n{(f'   |{"=" * (options[i][3])}>{"." * (options[i][2] - options[i][3])}| ({options[i][3]}/{options[i][2]}){new_line}{new_line}') if options[i][1] == True else ''}"""          

                        window.addstr(options_string)
                        window.refresh()

                else:
                    continue

            elif (pressed_key == b" "):
                if (pointer not in selected):
                    options[pointer][1] = True
                    options[pointer][3] = 1
                    selected.append(pointer)

                    window.clear()
                    options_string = f"{title}\n{'-' * len(title)}\n"

                    for i in range(len(options)):
                        options_string += f"""{'()' if i == pointer else '  '}[{'*' if i in selected else ' '}] {options[i][0]}\n{(f'   |{"=" * (options[i][3])}>{"." * (options[i][2] - options[i][3])}| ({options[i][3]}/{options[i][2]}){new_line}{new_line}') if options[i][1] == True else ''}"""          

                    window.addstr(options_string)
                    window.refresh()


                    while (2 + 2 != 5):
                        window.clear()
                        slider_move = getch()

                        if (slider_move == b"M"):
                            if (options[pointer][3] < options[pointer][2]):
                                options[pointer][3] += 1
                        
                        elif (slider_move == b"K"):
                            if (options[pointer][3] > 0):
                                options[pointer][3] -= 1

                        elif (slider_move == b" "):
                            if (options[pointer][3] == 0):
                                selected.remove(pointer)
                                options[pointer][1] = False

                            break

                        options_string = f"{title}\n{'-' * len(title)}\n"

                        for i in range(len(options)):
                            options_string += f"""{'()' if i == pointer else '  '}[{'*' if i in selected else ' '}] {options[i][0]}\n{(f'   |{"=" * (options[i][3])}>{"." * (options[i][2] - options[i][3])}| ({options[i][3]}/{options[i][2]}){new_line}{new_line}') if options[i][1] == True else ''}"""          

                        window.addstr(options_string)
                        window.refresh()
                
                else:
                    selected.remove(pointer)
                    options[pointer][1] = False

            elif (pressed_key == b"\r"):
                break

        return selected

    return curses.wrapper(menu)

if (__name__ == "__main__"):
    single("Welcome to [ENTER NAME] Bank!\n\nWhat would you like to do?", ["See amount", "Withdraw", "Deposit", "Exit"])
    multi("General", ["Legacy Controls", "Fullscreen", "Unlock FPS", "VSync"])
    mix("Audio", [["Dynamic sounds", "TOGGLE"], ["Master Volume", "SLIDER", 20, 10], ["Music", "SLIDER", 20, 20], ["Subtitles", "TOGGLE"]])
    amount("Market", [["Meth", False, 20, 1], ["Weed", False, 20, 1]])
    pass