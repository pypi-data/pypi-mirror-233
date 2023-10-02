#!/usr/bin/env python3

from datetime import datetime
import json
import os
import subprocess
import yaml

def parse_yaml_file(filepath : str):
    print("Parsing YAML file: " + filepath)
    if filepath and os.path.isfile(filepath) and os.path.exists(filepath):
        with open(filepath, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        print("YAML file provided does not exist. Exiting...")
        exit

def sanitize_stdout_for_json(std_out : list[str]):
    json_started = False
    json_lines = []
    for line in std_out:
        if line.startswith('[', 0, 1) or line.startswith('{', 0, 1):
            json_started = True
            json_lines.append(line)
        elif (line.startswith(']') or line.startswith('}')) and not line.startswith((' ', '\t')):
            json_lines.append(line)
            json_started = False
        elif json_started:
            json_lines.append(line)
    return "".join(json_lines)

def send_os_command(command : str, cwd : str=os.getcwd(), env : dict={}, shell : bool=False, is_secret : bool=False) -> str:
    all_stdout = []
    if not is_secret:
        print(command)
    if shell:
        process_command = command
    else:
        process_command = command.split()
    popen = subprocess.Popen(process_command, stdout=subprocess.PIPE, env=env, cwd=cwd, shell=shell, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        if not is_secret:
            print(stdout_line, end="")
        all_stdout.append(stdout_line)
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)
    return all_stdout 

def get_resource_group_from_subscription(subscription : str):
    print("Getting the resource group information from the subscription")
    az_cli_command = "az group list --subscription " + subscription 
    output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
    for rg in output:
        if "name" in rg.keys():
            return rg["name"]
    return None
    
def get_location_from_resource_group(resource_group : str):
    print("Getting the resource group information from the resource group: " + resource_group)
    az_cli_command = "az group show --resource-group " + resource_group 
    output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
    if "location" in output.keys():
        return output["location"]
    else:
        return None
    
def get_secret_from_key_vault(key_vault_name: str, secret_name : str):
    secret_value = None
    print("Getting secret " + secret_name + " from Azure Key Vault " + key_vault_name + ".")
    try:
        az_cli_command = "az keyvault secret show --name " + secret_name + " --vault-name " + key_vault_name
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        if "value" in output:
            if "attributes" in output and "enabled" in output["attributes"]:
                expiration_date = datetime.strptime(output["attributes"]["expires"], '%Y-%m-%dT%H:%M:%S+00:00').date()
                if output["attributes"]["enabled"] == True and expiration_date > datetime.now().date():
                    secret_value = str(output["value"]).strip().replace('"', '')
    except subprocess.CalledProcessError:
        print("Unable to retrieve secret " + secret_name + " from Azure Key Vault " + key_vault_name)
    return secret_value