import subprocess as subp


def checkout_text_is_present(cmd, text):
    result = subp.run(cmd, shell=True, stdout=subp.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_text_is_not_present(cmd, text):
    result = subp.run(cmd, shell=True, stdout=subp.PIPE, encoding='utf-8')
    if text not in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_error(cmd, error_message, check_error_code = False, error_code=1):
    result = subp.run(cmd, shell=True, stderr=subp.PIPE, encoding='utf-8')
    if check_error_code:
        if error_message in result.stderr and error_code == result.returncode:
            return True
        else:
            return False
    else:
        if error_message in result.stderr and result.returncode != 0:
            return True
        else:
            return False


def get_output(cmd):
    result = subp.run(cmd, shell=True, stdout=subp.PIPE, encoding='utf-8')
    return result.returncode, result.stdout
