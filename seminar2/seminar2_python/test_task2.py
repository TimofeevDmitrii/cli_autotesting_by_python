# def test_something(self):
#     errors = []
#
#     # replace assertions by conditions
#     if not condition_1:
#         errors.append("an error message")
#     if not condition_2:
#         errors.append("an other error message")
#
#     # assert no error message has been registered, else print messages
#     assert not errors, "errors occured:\n{}".format("\n".join(errors))



import subprocess as subp

def checkout(cmd, text):
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

def get_output(cmd):
    result = subp.run(cmd, shell=True, stdout=subp.PIPE, encoding='utf-8')
    return result.returncode, result.stdout



# - скопировать архив в пайтон-директорию семинара 2
# - mkdir test_files_dir
# - echo something >> test_files_dir/f1.txt
# - mkdir test_extract_dir
# - cp <archive> test_archive.7z

user_name = "kojedub-kojedubovich"
seminar2_path = '/home/'+user_name+'/seminars_cli_testing/seminar2/seminar2_python'
archive_name = 'test_archive.7z'
archive_path = seminar2_path + "/" + archive_name
test_files_dir_name = "test_files_dir"
test_files_path = seminar2_path + "/" + test_files_dir_name
test_out_path = seminar2_path + "/" + "test_extract_dir"


def test_step4():
    # in this case there is no file in archive before update cmd execute
    file_name = 'f1.txt'
    check_file_not_exists = checkout_text_is_not_present(f'cd {seminar2_path}; 7z l {archive_name}', file_name)
    update_operation_ok = checkout(f'7z u {archive_name} {test_files_path}/{file_name}', "Everything is Ok")
    check_file_append = checkout(f'7z l {archive_name}', file_name)

    assert check_file_not_exists and update_operation_ok and check_file_append, "test4 FAIL"


def test_step5():
    file_name = 'f1.txt'
    check_file_exists = checkout(f'cd {seminar2_path}; 7z l {archive_name}', file_name)
    delete_operation_ok = checkout(f'7z d {archive_name} {test_files_path}/{file_name}', "Everything is Ok")
    check_file_delete = checkout_text_is_not_present(f'7z l {archive_name}', file_name)

    assert check_file_exists and delete_operation_ok and check_file_delete, "test5 FAIL"



# If file not chosen before executing cmds update and delete -
# only archive_name is presents:
# update - archive will create if not exists?
# delete - archive will delete

