import pytest
import random, string
import yaml
from datetime import datetime
from ssh_checkout_functions import *


# with open("config_7z.yaml") as yaml_f:
#     data_yaml = yaml.safe_load(yaml_f)
#
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
bad_archive_name = data_yaml["bad_archive_name"]
test_work_dir = data_yaml['test_work_dir_name']
test_files_dir = data_yaml["test_files_dir_name"]
test_extract_dir = data_yaml["test_extract_dir_name"]
test_out_dir = data_yaml["test_out_dir_name"]
files_count = data_yaml["created_files_count"]
file_name_length = data_yaml["file_name_length"]
subfolder_name_length = data_yaml["subfolder_name_length"]
file_size = data_yaml["file_bs"]
arch_type = data_yaml["archive_type_key"]




@pytest.fixture
def make_folders():
    folders = [test_files_dir, test_extract_dir, test_out_dir]
    cmd = "cd {0}; mkdir {1}".format(test_work_dir, " ".join(folders))
    return ssh_checkout(host, user, passwd, cmd, "")


@pytest.fixture
def clear_folders():
    folders = [test_files_dir, test_extract_dir, test_out_dir]
    for ind in range(len(folders)):
        folders[ind] += '/*'
    cmd = "cd {0}; rm -rf {1}".format(test_work_dir, " ".join(folders))
    return ssh_checkout(host, user, passwd, cmd, "")


@pytest.fixture
def make_files():
    created_files = []
    for i in range(files_count):
        file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=file_name_length))
        cmd = "cd {0}; dd if=/dev/urandom of={1} bs={2} count=1 iflag=fullblock".format(
                f"{test_work_dir}/{test_files_dir}", file_name, file_size)
        if ssh_checkout(host, user, passwd, cmd, ''):
            created_files.append(file_name)
    return created_files


@pytest.fixture
def make_subfolder():
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=file_name_length))
    subfolder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=subfolder_name_length))

    cmd_1 = "cd {0}; mkdir {1}".format(f"{test_work_dir}/{test_files_dir}", subfolder_name)
    if not ssh_checkout(host, user, passwd, cmd_1, ""):
        return None, None

    cmd_2 = "cd {0}/{1}; dd if=/dev/urandom of={2} bs={3} count=1 iflag=fullblock".format(
        f"{test_work_dir}/{test_files_dir}", subfolder_name, file_name, file_size
    )
    if not ssh_checkout(host, user, passwd, cmd_2, ""):
        return subfolder_name, None
    return subfolder_name, file_name


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture
def create_broken_archive():
    cmd_create = f'cd {test_work_dir}/{test_files_dir}; 7z a{arch_type} ../{test_out_dir}/{bad_archive_name}'
    ssh_checkout(host, user, passwd, cmd_create,"Everything is Ok")

    cmd_to_brake = "cd {0}; truncate -s 1 {1}".format(f"{test_work_dir}/{test_out_dir}", bad_archive_name)
    ssh_checkout(host, user, passwd, cmd_to_brake, "")
    yield bad_archive_name
    cmd_delete = "cd {0}; rm -f {1}".format(f"{test_work_dir}/{test_out_dir}", bad_archive_name)
    ssh_checkout(host, user, passwd, cmd_delete, "")



@pytest.fixture(autouse=True)
def save_statistics():
        start_time = datetime.now()
        yield
        with open("stat.txt", "a", encoding='utf-8') as stat_file:
            step_info_list = []
            stop_time = datetime.now()
            step_info_list.append(f"step_time: {stop_time - start_time}")
            arch_type_out = arch_type.replace(" -t", "") if arch_type != "" else "7z"
            step_info_list.append(f"archive_type: {arch_type_out}")
            step_info_list.append(f"files_created: {files_count}")
            step_info_list.append(f"file_size: {file_size}")
            step_info_list.append(f"proc_load: {ssh_get_output(host, user, passwd, 'cat /proc/loadavg')[1]}")
            stat_file.write(" | ".join(step_info_list)+"\n")


@pytest.fixture
def get_test_start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
