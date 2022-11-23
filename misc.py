
def check_code(code):
    with open("codes.txt") as file:
        admin_code = file.readline()
        executor_code = file.readline()
        if admin_code == code:
            return "Admin"
        elif executor_code == code:
            return "Executor"
        else:
            return "no"
