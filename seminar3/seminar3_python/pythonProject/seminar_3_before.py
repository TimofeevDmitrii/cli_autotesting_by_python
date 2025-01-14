import checkout_functions as check_f

test_archive_name = 'test_archive.7z'
test_files_dir_name = "test_files_dir"
test_extract_dir_name = "test_extract_dir"
test_out_dir_name = "test_out_dir"

test_work_dir = f'/home/kojedub-kojedubovich/seminars_cli_testing/seminar3'


def test_step1():
    cmd = f'cd {test_work_dir}; 7z a {test_work_dir}/{test_out_dir_name}/{test_archive_name}'
    assert check_f.checkout_text_is_present(cmd,"Everything is Ok"), "test1 FAIL"


def test_step2():
    assert check_f.checkout_text_is_present(f'cd {test_work_dir}/{test_out_dir_name}; 7z e {test_archive_name} -o../{test_extract_dir_name} -y',
                                             "Everything is Ok"), "test2 FAIL"


def test_step3():
    assert check_f.checkout_text_is_present(f'cd {test_work_dir}/{test_out_dir_name}; 7z t {test_archive_name}',
                                            "Everything is Ok"), "test3 FAIL"

def test_step4():
    # in this case there is no file in archive before update cmd execute
    file_name = 'f1.txt'
    check_file_not_exists = check_f.checkout_text_is_not_present(f'cd {test_work_dir}; 7z l {test_archive_name}', file_name)
    update_operation_ok = check_f.checkout_text_is_present(f'7z u {test_archive_name} {test_files_dir_name}/{file_name}', "Everything is Ok")
    check_file_append = check_f.checkout_text_is_present(f'7z l {test_archive_name}', file_name)

    assert check_file_not_exists and update_operation_ok and check_file_append, "test4 FAIL"


def test_step5():
    file_name = 'f1.txt'
    check_file_exists = check_f.checkout_text_is_present(f'cd {test_work_dir}; 7z l {test_archive_name}', file_name)
    delete_operation_ok = check_f.checkout_text_is_present(f'7z d {test_archive_name} {test_files_dir_name}/{file_name}', "Everything is Ok")
    check_file_delete = check_f.checkout_text_is_not_present(f'7z l {test_archive_name}', file_name)

    assert check_file_exists and delete_operation_ok and check_file_delete, "test5 FAIL"


def test_step6():
    err_message = "ERROR:"
    extract_operation = check_f.checkout_error(f"cd {test_work_dir}; 7z e {test_archive_name} {test_out_dir_name}", \
                                               err_message, True, error_code=2)

    assert extract_operation, "test6 FAIL"


def test_step7():
    err_message = "ERROR:"
    assert check_f.checkout_error(f"cd {test_work_dir}; 7z t {test_archive_name}", err_message), "test7 FAIL"


def test_step8():
    create_archive_operation = check_f.checkout_text_is_present(f"7z a {test_archive_name} 7z_*", "Everything is Ok")
    archive_created = check_f.checkout_text_is_present("ls", test_archive_name)
    assert create_archive_operation and archive_created, "test8 FAIL"


def test_step9():
    archive_file_list = check_f.get_output(f"cd {test_work_dir}; 7z l -slt {test_archive_name}")[1].split("\n")
    archive_filter_list = filter(lambda x: 'Path =' in x and f'{test_archive_name}' not in x, archive_file_list)
    archive_file_set = set([x.replace('Path = ', '') for x in archive_filter_list])

    extract_operation = check_f.checkout_text_is_present(f"7z e {test_archive_name} -o{test_out_dir_name}", "Everything is Ok")

    extracted_file_set = set(filter(lambda x: x != '', check_f.get_output(f'ls {test_out_dir_name}')[1].split("\n")))

    assert extract_operation and archive_file_set == extracted_file_set, "test9 FAIL"
    # it is necessary to delete all files in dir {test_out_path} at the end of this test


def test_step10():

    crc32_cmd_out = check_f.get_output(f"crc32 {test_archive_name}")
    crc32_cmd_result = crc32_cmd_out[1].replace('\n', '')

    hash_7z_h_out = check_f.get_output(f"7z h {test_archive_name}")
    hash_7z_h_crc32_string = list(filter(lambda x: "CRC32 for data:" in x, hash_7z_h_out[1].split('\n')))
    hash_7z_h_result = hash_7z_h_crc32_string[0].replace("CRC32 for data:", "").replace(" ", "")

    assert crc32_cmd_out[0] == hash_7z_h_out[0] == 0 and crc32_cmd_result.upper() == hash_7z_h_result, "test10 FAIL"

