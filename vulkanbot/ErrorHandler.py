import sys
import datetime
import traceback

MAXIMUM_TRIES = 10


class ErrorHandler():
    """Receive errors to write into a log file

        Arg:
        folder_path = Relative path from root to where the logs should be create
    """

    def __init__(self, folder_path='') -> None:
        self.__folder_path = folder_path

    def write(self, error) -> bool:
        """Write the error to a log file"""
        if not isinstance(error, Exception):
            return False

        full_path = self.__open_file()
        if isinstance(full_path, bool):
            return False

        error_str = self.__prepare_error(error)

        try:
            with open(file=full_path, mode='w+') as log_file:
                log_file.write(error_str)
            return True
        except Exception as e:
            print(e)
            return False

    def __prepare_error(self, error: Exception) -> str:
        """Receive the error and return a good str"""
        time_now = datetime.datetime.now()
        tipo = sys.exc_info()[0]
        msg = sys.exc_info()[1]
        tb = traceback.format_tb(sys.exc_info()[2])
        error_str = f'Error Time: {time_now}\nTipo: {tipo}\nMsg: {msg}\nTraceback: {tb}'
        return error_str

    def __open_file(self) -> str:
        """Open a file to write the error"""
        successfull = False
        tries = 0

        while True:
            now = datetime.datetime.now()
            date_now = now.strftime(r'%d.%b.%Y-%Hh%Mm%Ss')

            full_path = f'{self.__folder_path}/{date_now}({tries}).txt'

            try:
                log_file = open(file=full_path, mode='w+')
                log_file.close()
            except Exception as e:
                print(e)
                tries += 1
                if tries > MAXIMUM_TRIES:
                    successfull = False
                    break
            else:
                successfull = True
                break

        if successfull:
            return full_path
        else:
            return False
