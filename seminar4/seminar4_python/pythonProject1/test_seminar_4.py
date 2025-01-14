import yaml
from ssh_checkout_functions import *

# with open("config_7z.yaml") as yaml_f:
#     data_yaml = yaml.safe_load(yaml_f)

with open("config_zip.yaml") as yaml_f:
    data_yaml = yaml.safe_load(yaml_f)

host = data_yaml["host_name"]
user = data_yaml["user_name"]
passwd = data_yaml["user_passwd"]
port = data_yaml["port_ssh"]

local_file_folder = data_yaml["deb_package_local_folder"]
destination_folder = data_yaml["deb_package_destination_folder"]
package_name = data_yaml["deb_package_name"]

test_archive_name = data_yaml["test_archive_name"]
test_work_dir = data_yaml['test_work_dir_name']
test_files_dir = data_yaml["test_files_dir_name"]
test_extract_dir = data_yaml["test_extract_dir_name"]
test_out_dir = data_yaml["test_out_dir_name"]
arch_type = data_yaml["archive_type_key"]


class TestPositive7z:

    def test_step0(self, get_test_start_time):
        results = []

        ssh_upload_files(
            host, user, passwd, local_file_folder+package_name, destination_folder+package_name)

        results.append(ssh_checkout(
            host, user, passwd,
        f"echo '{passwd}' | sudo -S dpkg -i {destination_folder+package_name}",
        "Setting up"))

        results.append(ssh_checkout(
            host, user, passwd,
            "echo '{0}' | sudo -S dpkg -s {1}".format(passwd, package_name.replace(".deb","")),
        "Status: install ok installed"))

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step0.txt")

        return all(results)


    def test_step1(self, make_folders, clear_folders, make_files, get_test_start_time):
        # create archive in out_dir
        cmd_1 = f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}'
        res_1 = ssh_checkout(host, user, passwd, cmd_1,"Everything is Ok")
        # check archive was created
        cmd_2 = f'cd {test_work_dir}; ls {test_out_dir}'
        res_2 = ssh_checkout(host, user, passwd, cmd_2,f"{test_archive_name}")

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step1.txt")

        assert res_1 and res_2, "test1 FAIL"


    def test_step2(self, clear_folders, make_files, get_test_start_time):
        results = []

        # create archive in out_dir
        cmd_1 = f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}'
        results.append(ssh_checkout(host, user, passwd, cmd_1,"Everything is Ok"))
        # execute extract operation
        cmd_2 = f'cd {test_work_dir}/{test_out_dir}; 7z e{arch_type} {test_archive_name} -o../{test_extract_dir} -y'
        results.append(ssh_checkout(host, user, passwd, cmd_2,"Everything is Ok"))

        # get list of extracted files by 'ls' cmd
        get_extr_files_cmd = ssh_get_output(host, user, passwd, f'ls {test_work_dir}/{test_extract_dir}')
        results.append(get_extr_files_cmd[0] == 0)

        created_files_set = set(make_files)
        extracted_files_set = set(filter(lambda x: x != '', get_extr_files_cmd[1].split("\n")))

        # compare lists of created files and extracted files
        results.append(created_files_set == extracted_files_set)

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step2.txt")

        assert all(results), "test2 FAIL"


    def test_step3(self, get_test_start_time):
        arch_type_expected = arch_type.replace(" -t", "") if arch_type != "" else "7z"

        cmd = f'cd {test_work_dir}/{test_out_dir}; 7z t{arch_type} {test_archive_name}'
        output_cmd = ssh_get_output(host, user, passwd, cmd)
        find_archive_type = list(filter(lambda x: "Type = " in x, output_cmd[1].split('\n')))
        arch_type_actual = find_archive_type[0].replace("Type = ", '')

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step3.txt")

        assert output_cmd[0] == 0 and arch_type_actual == arch_type_expected, "test3 FAIL"

    def test_step4(self, clear_folders, make_files, get_test_start_time):
        results = []
        # in this case there is no file in archive before update cmd execute

        # create empty archive in out_dir
        cmd_1 = f'cd {test_work_dir}/{test_extract_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}'
        results.append(ssh_checkout(host, user, passwd, cmd_1,"Everything is Ok"))

        #check created files not in archive before update operation
        cmd_2 = f'cd {test_work_dir}; 7z l{arch_type} {test_out_dir}/{test_archive_name}'
        for file_name in make_files:
            results.append(ssh_checkout_no_text(host, user, passwd, cmd_2, file_name))

        # execute update operation
        update_cmd = f'cd {test_work_dir}/{test_files_dir}; 7z u{arch_type} ../{test_out_dir}/{test_archive_name} *'
        results.append(ssh_checkout(host, user, passwd, update_cmd,"Everything is Ok"))

        # get list of appended files in archive by cmd
        cmd_3 = f"cd {test_work_dir}; 7z l{arch_type} -slt {test_out_dir}/{test_archive_name}"
        updated_archive_list_cmd = ssh_get_output(host, user, passwd, cmd_3)
        results.append(updated_archive_list_cmd[0] == 0)

        archive_file_list = updated_archive_list_cmd[1].split("\n")
        archive_filter_list = filter(lambda x: 'Path =' in x and f'{test_archive_name}' not in x, archive_file_list)
        archive_file_set = set([x.replace('Path = ', '') for x in archive_filter_list])
        created_files_set = set(make_files)
       # compare lists of created files and appended into archive files by update cmd
        results.append(archive_file_set == created_files_set)

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step4.txt")

        assert all(results), "test4 FAIL"


    def test_step5(self, clear_folders, make_files, get_test_start_time):
        results = []

        # create archive in out_dir
        cmd_1 = f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}'
        results.append(ssh_checkout(host, user, passwd, cmd_1,"Everything is Ok"))

        # get list of appended files in archive by cmd
        cmd_2 = f"cd {test_work_dir}; 7z l{arch_type} -slt {test_out_dir}/{test_archive_name}"
        archive_list_cmd = ssh_get_output(host, user, passwd, cmd_2)
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
        results.append(ssh_checkout(host, user, passwd, delete_cmd, "Everything is Ok"))

        # check files were deleted
        cmd_3 = f'cd {test_work_dir}; 7z l{arch_type} {test_out_dir}/{test_archive_name}'
        for file_name in make_files:
            results.append(ssh_checkout_no_text(host, user, passwd, cmd_3, file_name))

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step5.txt")

        assert all(results), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder, get_test_start_time):
        results = []

        # create archive with files and subdirectory
        cmd_1 = f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{test_archive_name}'
        results.append(ssh_checkout(host, user, passwd, cmd_1,"Everything is Ok"))

        cmd_2 = f'cd {test_work_dir}/{test_out_dir}; 7z x{arch_type} {test_archive_name} -o../{test_extract_dir} -y'
        results.append(ssh_checkout(host, user, passwd, cmd_2,"Everything is Ok"))

        cmd_3 = f'cd {test_work_dir}; ls {test_extract_dir}'
        for file_name in make_files:
            results.append(ssh_checkout(host, user, passwd, cmd_3, file_name))

        cmd_4 = f'cd {test_work_dir}; ls {test_extract_dir}'
        results.append(ssh_checkout(host, user, passwd, cmd_4,f'{make_subfolder[0]}'))

        cmd_5 = f'cd {test_work_dir}; ls {test_extract_dir}/{make_subfolder[0]}'
        results.append(ssh_checkout(host, user, passwd, cmd_5,f'{make_subfolder[1]}'))

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step6.txt")

        assert all(results), "test6 FAIL"


    def test_step7(self, clear_folders, make_files, get_test_start_time):
        results = []

        for file_name in make_files:
            crc32_cmd = f"cd {test_work_dir}; crc32 {test_files_dir}/{file_name}"
            crc32_cmd_out = ssh_get_output(host, user, passwd, crc32_cmd)
            results.append(crc32_cmd_out[0] == 0)
            crc32_cmd_result = crc32_cmd_out[1].replace('\n', '')

            hash_7z_h_cmd = f"cd {test_work_dir}; 7z h{arch_type} {test_files_dir}/{file_name}"
            hash_7z_h_out = ssh_get_output(host, user, passwd, hash_7z_h_cmd)
            results.append(hash_7z_h_out[0] == 0)
            hash_7z_h_crc32_string = list(filter(lambda x: "CRC32  for data:" in x, hash_7z_h_out[1].split('\n')))
            hash_7z_h_result = hash_7z_h_crc32_string[0].replace("CRC32  for data:", "").replace(" ", "")
            results.append(crc32_cmd_result.upper() == hash_7z_h_result.upper())

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step7.txt")

        assert all(results), "test7 FAIL"


    def test_step10(self, get_test_start_time):
        results = []

        results.append(ssh_checkout(
            host, user, passwd,
        "echo '{0}' | sudo -S dpkg -r {1}".format(passwd, package_name.replace(".deb","")),
        "Removing"))

        results.append(ssh_checkout(
            host, user, passwd,
            "echo '{0}' | sudo -S dpkg -s {1}".format(passwd, package_name.replace(".deb","")),
        "Status: deinstall ok config-files"))

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step10.txt")

        return all(results)


class TestNegative7z:
    def test_step8(self, clear_folders, make_files, create_broken_archive, get_test_start_time):
        err_message = "ERROR:"
        error_num = 2
        # try to execute extract operation
        cmd = f"cd {test_work_dir}/{test_out_dir}; 7z e{arch_type} {create_broken_archive}"
        extract_operation = ssh_checkout_negative(host, user, passwd, cmd, err_message, error_num)

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step8.txt")

        assert extract_operation, "test8 FAIL"


    def test_step9(self, clear_folders, make_files, create_broken_archive, get_test_start_time):
        err_message = "ERROR:"
        error_num = 2
        cmd = f"cd {test_work_dir}/{test_out_dir}; 7z t{arch_type} {create_broken_archive}"
        result = ssh_checkout_negative(host, user, passwd, cmd, err_message, error_num)

        ssh_save_journalctl_info(host, user, passwd, get_test_start_time, "log_tests/test_step9.txt")

        assert result, "test9 FAIL"