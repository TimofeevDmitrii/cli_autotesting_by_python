import yaml
import checkout_functions as check_f


with open("config.yaml") as yaml_f:
    data_yaml = yaml.safe_load(yaml_f)

test_archive_name = data_yaml["test_archive_name"]
test_work_dir = data_yaml['test_work_dir_name']
test_files_dir = data_yaml["test_files_dir_name"]
test_extract_dir = data_yaml["test_extract_dir_name"]
test_out_dir = data_yaml["test_out_dir_name"]
arch_type = data_yaml["archive_type_key"]


class TestPositive7z:
    def test_step1(self, make_folders, clear_folders, make_files):
        # create archive in out_dir
        res_1 = check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}',
            "Everything is Ok")
        # check archive was created
        res_2 = check_f.checkout_text_is_present(f'cd {test_work_dir}; ls {test_out_dir}',
            f"{test_archive_name}")
        assert res_1 and res_2, "test1 FAIL"


    def test_step2(self, clear_folders, make_files):
        results = []

        # create archive in out_dir
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}',
            "Everything is Ok"))
        # execute extract operation
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_out_dir}; 7z e{arch_type} {test_archive_name} -o../{test_extract_dir} -y',
                                                 "Everything is Ok"))

        # get list of extracted files by 'ls' cmd
        get_extr_files_cmd = check_f.get_output(f'ls {test_work_dir}/{test_extract_dir}')
        results.append(get_extr_files_cmd[0] == 0)

        created_files_set = set(make_files)
        extracted_files_set = set(filter(lambda x: x != '', get_extr_files_cmd[1].split("\n")))

        # compare lists of created files and extracted files
        results.append(created_files_set == extracted_files_set)

        assert all(results), "test2 FAIL"


    def test_step3(self):
        arch_type_expected = arch_type.replace(" -t", "") if arch_type != "" else "7z"

        output_cmd = check_f.get_output(f'cd {test_work_dir}/{test_out_dir}; 7z t{arch_type} {test_archive_name}')
        find_archive_type = list(filter(lambda x: "Type = " in x, output_cmd[1].split('\n')))
        arch_type_actual = find_archive_type[0].replace("Type = ", '')

        assert output_cmd[0] == 0 and arch_type_actual == arch_type_expected, "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        results = []
        # in this case there is no file in archive before update cmd execute

        # create empty archive in out_dir
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_extract_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}',
            "Everything is Ok"))

        #check created files not in archive before update operation
        for file_name in make_files:
            results.append(check_f.checkout_text_is_not_present(
                f'cd {test_work_dir}; 7z l{arch_type} {test_out_dir}/{test_archive_name}', file_name))

        # execute update operation
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_files_dir}; 7z u{arch_type} ../{test_out_dir}/{test_archive_name} *',
            "Everything is Ok"))

        # get list of appended files in archive by cmd
        updated_archive_list_cmd = check_f.get_output(
            f"cd {test_work_dir}; 7z l{arch_type} -slt {test_out_dir}/{test_archive_name}")
        results.append(updated_archive_list_cmd[0] == 0)

        archive_file_list = updated_archive_list_cmd[1].split("\n")
        archive_filter_list = filter(lambda x: 'Path =' in x and f'{test_archive_name}' not in x, archive_file_list)
        archive_file_set = set([x.replace('Path = ', '') for x in archive_filter_list])
        created_files_set = set(make_files)
       # compare lists of created files and appended into archive files by update cmd
        results.append(archive_file_set == created_files_set)

        assert all(results), "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        results = []

        # create archive in out_dir
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}',
            "Everything is Ok"))

        # get list of appended files in archive by cmd
        archive_list_cmd = check_f.get_output(f"cd {test_work_dir}; 7z l{arch_type} -slt {test_out_dir}/{test_archive_name}")
        results.append(archive_list_cmd[0] == 0)

        # check created files in archive before delete operation
        archive_file_list = archive_list_cmd[1].split("\n")
        archive_filter_list = filter(lambda x: 'Path =' in x and f'{test_archive_name}' not in x, archive_file_list)
        archive_file_set = set([x.replace('Path = ', '') for x in archive_filter_list])
        created_files_set = set(make_files)
        results.append(archive_file_set == created_files_set)

        created_files = ' '.join(make_files)
        delete_cmd = f'cd {test_work_dir}; 7z d{arch_type} {test_out_dir}/{test_archive_name} {created_files}'
        # execute delete operation
        results.append(check_f.checkout_text_is_present(delete_cmd, "Everything is Ok"))

        # check files were deleted
        for file_name in make_files:
            results.append(check_f.checkout_text_is_not_present(
                f'cd {test_work_dir}; 7z l{arch_type} {test_out_dir}/{test_archive_name}', file_name))

        assert all(results), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        results = []

        # create archive with files and subdirectory
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}',
            "Everything is Ok"))
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}/{test_out_dir}; 7z x{arch_type} {test_archive_name} -o../{test_extract_dir} -y',
            "Everything is Ok"
        ))

        for file_name in make_files:
            results.append(check_f.checkout_text_is_present(f'cd {test_work_dir}; ls {test_extract_dir}',
                                                            file_name))

        results.append(check_f.checkout_text_is_present(f'cd {test_work_dir}; ls {test_extract_dir}',
                                                        f'{make_subfolder[0]}'))
        results.append(check_f.checkout_text_is_present(
            f'cd {test_work_dir}; ls {test_extract_dir}/{make_subfolder[0]}',
            f'{make_subfolder[1]}'))

        assert all(results), "test6 FAIL"


    def test_step7(self, clear_folders, make_files):
        results = []

        for file_name in make_files:
            crc32_cmd_out = check_f.get_output(f"cd {test_work_dir}; crc32 {test_files_dir}/{file_name}")
            results.append(crc32_cmd_out[0] == 0)
            crc32_cmd_result = crc32_cmd_out[1].replace('\n', '')

            hash_7z_h_out = check_f.get_output(f"cd {test_work_dir}; 7z h{arch_type} {test_files_dir}/{file_name}")
            results.append(hash_7z_h_out[0] == 0)
            hash_7z_h_crc32_string = list(filter(lambda x: "CRC32  for data:" in x, hash_7z_h_out[1].split('\n')))
            hash_7z_h_result = hash_7z_h_crc32_string[0].replace("CRC32  for data:", "").replace(" ", "")
            results.append(crc32_cmd_result.upper() == hash_7z_h_result)

        assert all(results), "test7 FAIL"


class TestNegative7z:
    def test_step8(self, clear_folders, make_files, create_broken_archive):
        err_message = "ERROR:"
        # try to execute extract operation
        cmd = f"cd {test_work_dir}/{test_out_dir}; 7z e{arch_type} {create_broken_archive}"
        extract_operation = check_f.checkout_error(cmd, err_message, True, error_code=2)

        assert extract_operation, "test8 FAIL"


    def test_step9(self, clear_folders, make_files, create_broken_archive):
        err_message = "ERROR:"
        assert check_f.checkout_error(
            f"cd {test_work_dir}/{test_out_dir}; 7z t{arch_type} {create_broken_archive}", err_message), "test9 FAIL"