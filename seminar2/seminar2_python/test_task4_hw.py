import checkout_functions as check_f

user_name = "kojedub-kojedubovich"
seminar2_path = '/home/'+user_name+'/seminars_cli_testing/seminar2/seminar2_python'
archive_name = 'test_archive.7z'
archive_path = seminar2_path + "/" + archive_name
test_files_dir_name = "test_files_dir"
test_files_path = seminar2_path + "/" + test_files_dir_name
test_out_path = seminar2_path + "/" + "test_extract_dir"

def test_step8():
    create_archive_operation = check_f.checkout_text_is_present(f"7z a {archive_name} 7z_*", "Everything is Ok")
    archive_created = check_f.checkout_text_is_present("ls", archive_name)
    assert create_archive_operation and archive_created, "test8 FAIL"


def test_step9():
    archive_file_list = check_f.get_output(f"7z l -slt {archive_name}")[1].split("\n")
    archive_filter_list = filter(lambda x: 'Path =' in x and f'{archive_name}' not in x, archive_file_list)
    archive_file_set = set([x.replace('Path = ', '') for x in archive_filter_list])

    extract_operation = check_f.checkout_text_is_present(f"7z e {archive_name} -o{test_out_path}", "Everything is Ok")

    extracted_file_set = set(filter(lambda x: x != '', check_f.get_output(f'ls {test_out_path}')[1].split("\n")))

    assert extract_operation and archive_file_set == extracted_file_set, "test9 FAIL"
    # it is necessary to delete all files in dir {test_out_path} at the end of this test

def test_step10():
    file_name = "test_task3_negative.py"
    crc32_cmd_out = check_f.get_output(f"crc32 {archive_name}")
    crc32_cmd_result = crc32_cmd_out[1].replace('\n', '')

    hash_7z_h_out = check_f.get_output(f"7z h {archive_name}")
    hash_7z_h_crc32_string = list(filter(lambda x: "CRC32  for data:" in x, hash_7z_h_out[1].split('\n')))
    hash_7z_h_result = hash_7z_h_crc32_string[0].replace("CRC32  for data:", "").replace(" ", "")

    assert crc32_cmd_out[0] == hash_7z_h_out[0] == 0 and crc32_cmd_result.upper() == hash_7z_h_result, "test10 FAIL"


