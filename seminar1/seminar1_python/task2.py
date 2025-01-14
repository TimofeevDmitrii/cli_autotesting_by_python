import subprocess as subpr

if __name__ == '__main__':
    result = subpr.run("cat /etc/os-release", shell=True, stdout=subpr.PIPE, encoding="utf-8")
    find_1 = "jammy"
    find_2 = "22.04.4"
    output = result.stdout
    if find_1 in output and find_2 in output and result.returncode == 0:
        print("Test is successful")
    else:
        print("Test is failed")

