from __future__ import annotations
import constants as const
from os import system
from sys import exit as sys_exit

class BuildCommands:
    @staticmethod
    def dead_code():
        exit_code = system(f"vulture {const.SOURCE_DIR} --exclude {const.EXCLUDED_GLOBS} --min-confidence 70")
        if exit_code > 0:
            sys_exit(1)

    @staticmethod
    def format_check():
        exit_code = system(f"autopep8 --diff --exclude {const.EXCLUDED_GLOBS} --exit-code --recursive {const.SOURCE_DIR}")
        if exit_code > 0:
            sys_exit(1)
    
    @staticmethod
    def format_fix():
        exit_code = system(f"autopep8 --exclude {const.EXCLUDED_GLOBS} --exit-code --in-place --recursive {const.SOURCE_DIR}")
        if exit_code > 0:
            sys_exit(1)
    
    @staticmethod
    def imports_check():
        skip_glob_flag = "--skip-glob"
        globs = const.EXCLUDED_GLOBS.split(",")

        def to_cli_arg(excluded_glob):
            return f"{skip_glob_flag} {excluded_glob}"
        skip_globs = " ".join(list(map(to_cli_arg, globs)))
        command = f"isort {const.SOURCE_DIR} {const.TEST_DIR} --check-only {skip_globs}"
        exit_code = system(command)
        if exit_code > 0:
            sys_exit(1)

    @staticmethod
    def imports_fix():
        skip_glob_flag = "--skip-glob"
        globs = const.EXCLUDED_GLOBS.split(",")

        def to_cli_arg(excluded_glob):
            return f"{skip_glob_flag} {excluded_glob}"
        skip_globs = " ".join(list(map(to_cli_arg, globs)))
        command = f"isort {const.SOURCE_DIR} {const.TEST_DIR} {skip_globs}"
        exit_code = system(command)
        if exit_code > 0:
            sys_exit(1)

    @staticmethod
    def lint():
        pycodestyle_exit_code = system(f'pycodestyle {const.SOURCE_DIR} {const.TEST_DIR}')
        pylint_exit_code = system(f'pylint {const.SOURCE_DIR} {const.TEST_DIR} --enable=useless-suppression')
        if pycodestyle_exit_code or pylint_exit_code > 0:
            print('Linting finished with errors - please fix the errors above.')
            sys_exit(1)

    @staticmethod
    def unit_test():
        exit_code = system('pytest')
        if exit_code > 0:
            sys_exit(1)