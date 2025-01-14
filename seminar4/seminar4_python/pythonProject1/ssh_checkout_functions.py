import paramiko

def ssh_checkout(host, user_name, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user_name, password=passwd, port=port)
    client_stdin, client_stdout, client_stderr = client.exec_command(cmd)
    return_code = client_stdout.channel.recv_exit_status()
    output = (client_stdout.read() + client_stderr.read()).decode("utf-8")
    client.close()

    if text in output and return_code == 0:
        return True
    else:
        return False


def ssh_checkout_no_text(host, user_name, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user_name, password=passwd, port=port)
    client_stdin, client_stdout, client_stderr = client.exec_command(cmd)
    return_code = client_stdout.channel.recv_exit_status()
    output = (client_stdout.read() + client_stderr.read()).decode("utf-8")
    client.close()

    if text not in output and return_code == 0:
        return True
    else:
        return False


def ssh_checkout_negative(host, user_name, passwd, cmd, text, err_code, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user_name, password=passwd, port=port)
    client_stdin, client_stdout, client_stderr = client.exec_command(cmd)
    return_code = client_stdout.channel.recv_exit_status()
    output = (client_stdout.read() + client_stderr.read()).decode("utf-8")
    client.close()

    if text in output and return_code == err_code:
        return True
    else:
        return False


def ssh_get_output(host, user_name, passwd, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user_name, password=passwd, port=port)
    client_stdin, client_stdout, client_stderr = client.exec_command(cmd)
    return_code = client_stdout.channel.recv_exit_status()
    output = (client_stdout.read() + client_stderr.read()).decode("utf-8")
    client.close()

    return return_code, output



def ssh_upload_files(host, user_name, passwd, local_path, remote_path, port=22):
    print(f"Loading file from {local_path} to {remote_path} ...")
    transport = paramiko.Transport((host, port)) # host and port in a parenthesis because it should be one element
    transport.connect(None, username = user_name, password=passwd)
    sftp_client = paramiko.SFTPClient.from_transport(transport)
    sftp_client.put(local_path, remote_path)
    if sftp_client:
        sftp_client.close()
    if transport:
        transport.close()


def ssh_download_files(host, user_name, passwd, remote_path, local_path, port=22):
    print(f"Downloading file from {remote_path} to {local_path} ...")
    transport = paramiko.Transport((host, port)) # host and port in a parenthesis because it should be one element
    transport.connect(None, username = user_name, password=passwd)
    sftp_client = paramiko.SFTPClient.from_transport(transport)
    sftp_client.get(local_path, remote_path)
    if sftp_client:
        sftp_client.close()
    if transport:
        transport.close()


def ssh_save_journalctl_info(host, user, passwd, since_time, file_name, port=22):
    cmd = f"journalctl --since '{since_time}'"
    journalctl_output = ssh_get_output(host, user, passwd, cmd, port)
    with open(file_name, "w", encoding='utf-8') as info_file:
        info_file.write(journalctl_output[1] + "\n")