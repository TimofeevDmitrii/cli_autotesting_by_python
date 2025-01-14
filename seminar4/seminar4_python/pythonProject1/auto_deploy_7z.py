from ssh_checkout_functions import ssh_checkout, ssh_upload_files

def deploy():
    results = []

    local_file_path = "p7zip_folder/p7zip-full.deb"
    destination_path = "/home/user_test/p7zip-full.deb"
    ssh_upload_files(
        "0.0.0.0", "user_test", "2323", local_file_path, destination_path)

    results.append(ssh_checkout("0.0.0.0", "user_test", "2323",
                 "echo '2323' | sudo -S dpkg -i /home/user_test/p7zip-full.deb",
                 "Setting up"))

    results.append(ssh_checkout("0.0.0.0", "user_test", "2323",
                 "echo '2323' | sudo -S dpkg -s p7zip-full",
                 "Status: install ok installed"))

    return all(results)


if deploy():
    print("Deploy is successful !!!")
else:
    print("Deploy is failed")