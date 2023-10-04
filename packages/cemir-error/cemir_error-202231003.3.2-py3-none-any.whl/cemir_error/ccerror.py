import os
import sys
import traceback
from datetime import datetime


class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = '\033[92m'
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = '\033[95m'
    CYAN = "\033[96m"
    DARK_CYAN = '\033[36m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colored_print(color, text):
    return f"{color}{text}{Colors.RESET}"


def translate_error_message(error_type, language="tr"):
    # Dil dosyasını yükle
    if language == "tr":
        from .errors_tr import error_messages

    elif language == "en":
        from .errors_en import error_messages

    elif language == "fr":
        from .errors_fr import error_messages

    elif language == "de":
        from .errors_de import error_messages

    else:
        raise ValueError(f"Unknown language: {language}")

    # Hata türüne göre açıklamayı al veya varsayılanı kullan
    return error_messages.get(error_type, "Unknown error occurred.")


def error_tracking(error_type, traceback_obj, language="tr"):
    project_path = "/".join(os.getcwd().split("/")[-4:])
    error_description = translate_error_message(error_type, language=language)['detail']
    error_fix = translate_error_message(error_type, language=language)['fix']


    print("#" * 100)
    print(colored_print(Colors.UNDERLINE, colored_print(Colors.BOLD, colored_print(Colors.MAGENTA, datetime.now()))))
    print(colored_print(Colors.RED, f"{colored_print(Colors.YELLOW, error_type)} ({error_description}) "), f"{Colors.BOLD}{error_fix}")

    for frame in reversed(traceback.extract_tb(traceback_obj)):
        file_path, line_number, function_name, code_line = frame

        if project_path in file_path:
            print("*" * 50)
            file_path = colored_print(Colors.BLUE, file_path)
            code_line = colored_print(Colors.BLUE, code_line)
            line_number = colored_print(Colors.YELLOW, line_number)
            last_folder = colored_print(Colors.CYAN, " / ".join(file_path.split("/")[-4:]))
            print(colored_print(Colors.RED, f"{last_folder} : {line_number}"))
            print(colored_print(Colors.RED, f"{code_line}"))

            # function_name = colored_print(Colors.BLUE, function_name)
            # print(colored_print(Colors.RED, f"File Path: {file_path}"))
            # print(colored_print(Colors.RED, f"Function Name: {function_name}"))
            print("*" * 50)

    print("#" * 100)


sys.excepthook = error_tracking
