import subprocess as subpr

if __name__ == '__main__':
    result = subpr.run("cat /etc/os-release", shell=True, stdout=subpr.PIPE, encoding="utf-8")
    result_stdout_list = result.stdout.split('\n')
    find_1 = 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'
    find_2 = 'VERSION_CODENAME=jammy'
    process_exit_code = result.returncode
    # print(result_stdout_list)
    if process_exit_code == 0:
        if find_1 in result_stdout_list and find_2 in result_stdout_list:
            print("Test is successful!")
        else:
            print("Test is failed")
    else:
        print("Process was ended with error:", process_exit_code)