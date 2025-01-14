import subprocess
import string


def checkout(cmd, text, strong=False):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if strong:
        for c in string.punctuation:
            s = result.stdout.replace(c, "")
        listout = s.split()
        if text in listout and result.returncode == 0:
            return True
        else:
            return False
    else:
        if text in result.stdout and result.returncode == 0:
            return True
        else:
            return False

