import checkout_functions as check_f

user_name = "kojedub-kojedubovich"
seminar2_path = '/home/'+user_name+'/seminars_cli_testing/seminar2/seminar2_python'
archive_name = 'test_archive.7z'
archive_path = seminar2_path + "/" + archive_name
test_files_dir_name = "test_files_dir"
test_files_path = seminar2_path + "/" + test_files_dir_name
test_out_path = seminar2_path + "/" + "test_extract_dir"


def test_step6():
    err_message = "ERROR:"
    extract_operation = check_f.checkout_error(f"7z e {archive_name} {test_out_path}", \
                                               err_message, True, error_code=2)

    assert extract_operation, "test6 FAIL"


def test_step7():
    err_message = "ERROR:"
    assert check_f.checkout_error(f"cd {seminar2_path}; 7z t {archive_name}", err_message), "test7 FAIL"


#
# result = subp.run(f"cd {seminar2_path}; 7z t {archive_name}", shell=True, stderr=subp.PIPE, encoding='utf-8')
#
# print(f'result.returncode = {result.returncode}')
# print(f'result.stderr = {result.stderr}')
