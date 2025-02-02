import os
import re
import shutil
import sys

import board_prettyprint
import board_solver
import console_user_input
import user_account_control as uac


title_file = "assets/ascii_title.txt"
help_file = "assets/ascii_instructions.txt"


def validate_login(uname, pwd):
    if not re.search('(?=.*[a-zA-Z0-9])(?=.*[-+_!@#$%^&*.,?])', pwd): # Reegex for checking password validity
        return False, 'Password must contain:\n\
- At least one upper-case character\n\
- At least one lower-case character\n\
- At least one number\n\
- At least one special character'
    
    if len(pwd) < 8:
        return False, 'Password must be at least 8 characters long!'

    if uname == pwd:
        return False, 'Please choose a different password, the username and password should not be the same!'

    return True, None


def get_logininfo():
    uname = input("Enter a username: ")
    if uac.check_existing_user(uname):
        print(f"Hello {uname}! Please enter your password.")
        
        while True:
            pwd = input('Enter Password: ')            
            pwd_hash = uac.hash_sha256(pwd)
            if pwd_hash == uac.hash_sha256(''):
                res = False, None
                break

            res = uac.login(uname, pwd_hash)
            if res[0]:
                break
            print('Invalid password! Please try again, or press ENTER to sign up / choose a different account.')

    else:
        print("Welcome new user! Please create a password. (Minimum 8 characters long)")
        print('Password must contain:\n\
- At least one upper-case character\n\
- At least one lower-case character\n\
- At least one number\n\
- At least one special character')

        while True:
            pwd = input('Enter password: ')
            validation = validate_login(uname, pwd)
            if not validation[0]:
                print(validation[1])
                continue
                    
            pwd_hash = uac.hash_sha256(pwd)
            pwd1_hash = uac.hash_sha256(input('Re-enter password: '))
            if pwd_hash == pwd1_hash:
                break

            print('Passwords do not match!')

        uac.signup(uname, pwd_hash, hashed=True)
        res = uac.login(uname, pwd_hash)

    return res


def print_title():
    cols, _ = shutil.get_terminal_size()
    with open(title_file, encoding="utf-8") as tf:
        lines = tf.readlines()
        tf.seek(0)

        max_length = max([len(l) for l in lines])
        if cols < max_length:
            os.system(f'mode con: cols={max_length} lines=40')

        print(tf.read())


def print_help():
    with open(help_file, encoding="utf-8") as hf:
        print(hf.read())
    input()


def run_cli_solving_sequence():
    os.system("cls" if os.name == "nt" else "clear")
    board = console_user_input.get_input()
    solve_state, solved_board = board_solver.solve(board)

    if solve_state:
        print("\n\n\n")
        print("SOLVED! Here's the solution to the entered board:\n\n\n")
        board_prettyprint.prettyprint(solved_board)
        return

    print("\n\n\n")
    print(
        "The entered board cannot be solved! This may be because of a repeated"
        " number or other invalidity in the entered configuration."
    )
    return


# def construct_prompt(name, message, choices):
#     return [inquirer.List(name, message, choices)]


# def prompt_user(prompt, name):
#     return inquirer.prompt(prompt)[name]


if __name__ == "__main__":
    try:
        print_title()
        print("\n\n\n")

        help_yn = input("Print help file? (Y/N): ").strip().lower()
        if help_yn == "y":
            print_help()

        while True:
            info = get_logininfo()
            if info[0]:
                break
        print(f'\n\nHey {info[1][0]}, welcome to SudoSOLVE! Here are your user details:\n')
        print(f'Username: {info[1][0]}\nData folder: {info[1][1]}\n\n')
        input('Press ENTER to continue...')
                

        app_mode = "cli" 
        if app_mode == "cli":
            while True:
                run_cli_solving_sequence()

                solve_another = input('Solve another puzzle? (Y/N): ').strip().lower()

                if solve_another == "y":
                    continue

                with open("assets/ascii_thanks.txt", encoding="utf-8") as thxf:
                    print(thxf.read())
                break
    
        
    except:
        sys.exit()
    