from app_config import CODES_PATH


def check_code(code):
    with open(CODES_PATH) as file:
        admin_code = file.readline()
        executor_code = file.readline()
        if admin_code == code:
            return "Admin"
        elif executor_code == code:
            return "Executor"
        else:
            return "no"
