import json

import paramiko


def connect_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("moddwarf.local", username="root", password="mod")
    return client


def get_pedalboard_list():
    client = connect_ssh()
    stdin, stdout, stderr = client.exec_command("ls -l .pedalboards")
    pb_list = list(stdout)[1:]
    pb_list = [pbdir.split(" ")[-1].strip("\n") for pbdir in pb_list]
    return pb_list


def get_pedalboard(pb_path):
    client = connect_ssh()
    pb_name, _ = pb_path.split(".")

    #
    # Pedalboard definition
    pb_data_path = f".pedalboards/{pb_path}/{pb_name}.ttl"
    stdin, stdout, stderr = client.exec_command(f"cat {pb_data_path}")
    pb_ttl = list(stdout)

    #
    # Snapshots
    #
    pb_snapshots_path = f".pedalboards/{pb_path}/snapshots.json"
    stdin, stdout, stderr = client.exec_command(f"cat {pb_snapshots_path}")
    pb_snapshots = list(stdout)
    snapshot_data = json.loads("".join(pb_snapshots))
    snapshot_names = [sn["name"] for sn in snapshot_data["snapshots"]]
    #print(snapshot_names)

    #
    # Addressings
    #
    pb_adressings_path = f".pedalboards/{pb_path}/addressings.json"
    stdin, stdout, stderr = client.exec_command(f"cat {pb_adressings_path}")
    pb_addressings = list(stdout)
    addressing_data = json.loads("".join(pb_addressings))
    addressing_names = addressing_data.keys()
    #print(addressing_names)
    return snapshot_names, list(addressing_names)