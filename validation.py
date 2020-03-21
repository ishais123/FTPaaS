from validate_email import validate_email
import re
import config


# define custom exception
class FTPIncorrectSyntax(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FTPIncorrectSyntax, {0} '.format(self.message)
        else:
            return 'FTPIncorrectSyntax has been raised'


# parse message
def parse_message(msg):
    # check if string is empty
    if not msg:
        raise FTPIncorrectSyntax("Empty String")
    # split the message and ensure correct number of arguments
    split_command = msg.split()
    if not len(split_command) == config.NUMBER_OF_ARGUMENTS:
        raise FTPIncorrectSyntax("Incorrect number of arguments")
    command = split_command[1].lower()
    folder = split_command[2].lower()
    receive = split_command[3].lower()
    if receive[0] == "<":
        split1 = receive.split(":")
        if split1[0] == "<mailto":
            split1_res = split1[1]
            split2 = split1_res.split("|")
            email = split2[0]
        else:
            raise FTPIncorrectSyntax("Invalid email address")
    else:
        raise FTPIncorrectSyntax("Invalid email address")
    # this is a create command
    if command == "create":
        # validate folder name
        pattern = re.compile("[A-Za-z0-9\-\_]{3,20}")
        if not pattern.fullmatch(folder):
            raise FTPIncorrectSyntax("Folder name must be between 3 and 20 valid characters")
        # validate email address
        if not validate_email(email):
            raise FTPIncorrectSyntax("Invalid email address")
    else:
        raise FTPIncorrectSyntax("Unknown command '" + command + "'")

    return command, folder, email

