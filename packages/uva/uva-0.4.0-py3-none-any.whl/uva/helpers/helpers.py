import datetime
from pathlib import Path
from enum import Enum

import timeago


class SubmitLanguage(str, Enum):
    c = 'c',
    java = 'java',
    cplusplus = 'c++'
    pascal = 'pascal'
    cplusplus11 = 'c++11'
    python = 'python'

    def __int__(self):
        if self.value == 'c':
            return 1
        elif self.value == 'java':
            return 2
        elif self.value == 'c++':
            return 3
        elif self.value == 'pascal':
            return 4
        elif self.value == 'c++11':
            return 5
        else:
            return 6


verdict_dict = {
        0: "Processing",
        10: "[bold #000000]Submission error",
        15: "Can't be judged",
        20: "[bold #000000]In queue",
        30: "[bold #AAAA00]Compile error",
        35: "Restricted function",
        40: "[bold #00AAAA]Runtime error",
        45: "Output limit",
        50: "[bold #0000FF]Time limit",
        60: "Memory limit",
        70: "[bold #FF0000]Wrong answer",
        80: "[bold #666600]PresentationE",
        90: "[bold #00AA00]Accepted"
    }

language_dict = {
        1: "ANSI C",
        2: "Java",
        3: "C++",
        4: "Pascal",
        5: "C++11",
        6: "Python"
}

extensions_language_map_dict = {
    '.c': SubmitLanguage.c,
    '.java': SubmitLanguage.java,
    '.cpp': SubmitLanguage.cplusplus,
    '.pas': SubmitLanguage.pascal,
    '.py': SubmitLanguage.python
}


def detect_language(filepath):
    extension = Path(filepath).suffix
    return extensions_language_map_dict.get(extension)


language_extensions_map_dict = {
    SubmitLanguage.c: '.c',
    SubmitLanguage.java: '.java',
    SubmitLanguage.cplusplus: '.cpp',
    SubmitLanguage.pascal: '.pas',
    SubmitLanguage.python: '.py',
}


def get_file_extension(language):
    return language_extensions_map_dict.get(language)


def generate_submission_table_row(s):
    submission_time = timeago.format(datetime.datetime.fromtimestamp(s[4]) - datetime.timedelta())
    return [
        str(s[0]),
        str(s[1]),
        verdict_dict[s[2]],
        str(s[3]),
        submission_time,
        language_dict[s[5]],
        str(s[6])
    ]
