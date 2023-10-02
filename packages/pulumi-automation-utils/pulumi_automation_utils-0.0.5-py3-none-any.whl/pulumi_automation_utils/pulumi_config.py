#!/usr/bin/env python3

from datetime import timedelta
import os
import subprocess
import sys

from pulumi_automation_utils.common import *
from pulumi_automation_utils.environment import Environment
from pulumi_automation_utils.login_config import LoginConfig

class PulumiConfig:
    def __init__(self,
                 login_config : LoginConfig,
                 yaml_vars : dict
                 ):
        self.environment_vars = os.environ.copy()

        self.stack_name = None
        if "stack_name" in yaml_vars:
            self.stack_name = yaml_vars["stack_name"]
        else:
            print("Stack name was not found in YAML. Exiting...")
            exit

        # Set the random value, useful in name randomization when setting up and tearing down numerous times quickly
        self.random_value = None
        if "random_value" in yaml_vars:
            self.random_value = yaml_vars["random_value"]

        self.login_config = login_config
        self.yaml_vars = yaml_vars
        self.__set_pulumi_vars()
        self.__set_environment()
        self.__set_storage_account_information()
        self.__set_key_vault_information()
        self.__set_location_information()

    def configure_pulumi(self):
        if not self.login_config.is_logged_in():
            self.login_config.login_to_azure()

        self.__setup_storage_account()
        self.__setup_storage_container()
        self.__setup_encryption_key()
        self.__setup_sas_token()

        self.environment_vars["AZURE_STORAGE_ACCOUNT"] = self.storage_account_name
        self.environment_vars["AZURE_STORAGE_SAS_TOKEN"] = self.sas_token
        if self.environment == Environment.SANDBOX:
            self.environment_vars["ARM_ENVIRONMENT"] = "public"
        else:
            self.environment_vars["ARM_ENVIRONMENT"] = "usgovernment"
        self.environment_vars["PULUMI_CONFIG_PASSPHRASE"] = ""

        # storage account URL will change in usgovernment
        self.__run_pulumi_command("/pulumi/bin/pulumi login azblob://" + self.storage_container_name + "?storage_account=" + self.storage_account_name + " --non-interactive")
        # Key Vault URL will change in usgovernment
        command_succeeded = False
        while not command_succeeded:
            try: 
                self.__run_pulumi_command("/pulumi/bin/pulumi stack select --stack " + self.stack_name + " --create --secrets-provider azurekeyvault://" + self.key_vault_name + ".vault.azure.net/keys/" + self.encryption_key_name + " --non-interactive")
                command_succeeded = True
            except subprocess.CalledProcessError:
                pass

        self.__pulumi_set_config("azure", "skipProviderRegistration", "true")
        self.__pulumi_set_config("azure-native", "location", self.location)
        self.__pulumi_set_config(self.stack_name, "location", self.location)
        self.__pulumi_set_config(self.stack_name, "subscription", self.login_config.get_subscription())
        if "key_vault_id" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(self.stack_name, "key_vault_id", get_key_vault_id(login_config=self.login_config, key_vault_name=self.key_vault_name))
        if "resource_group_name" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(self.stack_name, "resource_group_name", get_resource_group_from_subscription(login_config=self.login_config))
        if "storage_account_name" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(self.stack_name, "storage_account_name", self.storage_account_name)
        for var in self.pulumi_vars.keys():
            self.__pulumi_set_config(self.stack_name, var, self.pulumi_vars[var])

    def deploy_pulumi(self):
        command = "/pulumi/bin/pulumi up"
        print(command)
        popen = subprocess.Popen(
                    command, 
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr, 
                    env=self.environment_vars, 
                    cwd=self.pulumi_directory, 
                    shell=True, 
                    universal_newlines=True)
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, command)

    def get_build_container_image(self):
        return self.build_container_image
    
    def get_container_instance_name(self):
        return self.container_instance_name
    
    def get_container_instance_public_ip(self):
        return self.container_instance_public_ip
    
    def get_container_host(self):
        fqdn = self.__run_pulumi_command("pulumi stack output --stack " + self.stack_name + " container_fqdn", is_secret=True)
        if fqdn is not None and fqdn != "":
            return fqdn[0].strip()
        else:
            ip_addr = self.__run_pulumi_command("pulumi stack output --stack " + self.stack_name + " container_ip", is_secret=True)
            return ip_addr[0].strip()
    
    def get_container_ssh_user(self):
        return self.container_ssh_user
    
    def get_container_ssh_group(self):
        return self.container_ssh_group
    
    def get_container_ssh_password(self):
        return self.container_ssh_password

    def get_container_registry_acr(self):
        return self.container_registry_acr
    
    def get_container_registry_name(self):
        return self.container_registry_name
    
    def get_container_registry_username(self):
        return self.container_registry_username

    def get_container_registry_password(self):
        return self.container_registry_password
    
    def get_container_image_name(self):
        return self.container_image_name
    
    def get_container_image_tag(self):
        return self.container_image_tag
    
    def get_dockerfile_context(self):
        return self.dockerfile_context
    
    def get_dockerfile_location(self):
        return self.dockerfile_location
    
    def get_encryption_key_name(self):
        return self.encryption_key_name
    
    def get_file_share_name(self):
        return self.file_share_name
    
    def get_key_vault_name(self):
        return self.key_vault_name
    
    def get_location(self):
        return self.location
    
    def get_sas_token(self):
        return self.sas_token
    
    def get_sas_token_name(self):
        return self.sas_token_name
    
    def get_storage_account_name(self):
        return self.storage_account_name
    
    def get_storage_account_sku(self):
        return self.storage_account_sku
    
    def get_storage_container_name(self):
        return self.storage_container_name
    
    def set_sas(self, sas_token : str):
        self.sas_token = sas_token

    def __set_pulumi_vars(self):
        self.pulumi_vars = {}
        if type(self.yaml_vars) is dict:
            if "pulumi" in self.yaml_vars:
                if "project_location" in self.yaml_vars:
                    self.pulumi_directory = os.path.abspath(self.yaml_vars["project_location"])
                else:
                    self.pulumi_directory = os.path.abspath(os.path.join(os.curdir, "pulumi"))
                for var_name in self.yaml_vars["pulumi"]:
                    self.pulumi_vars[var_name] = self.yaml_vars["pulumi"][var_name]

    
    def __set_environment(self):
        self.environment = Environment.SANDBOX
        if type(self.yaml_vars) is dict:
            if "environment" in self.yaml_vars:
                if self.yaml_vars["environment"].lower() == "zonec":
                    self.environment = Environment.ZONEC
                if self.yaml_vars["environment"].lower() == "zoneb":
                    self.environment = Environment.ZONEB
                if self.yaml_vars["environment"].lower() == "zonea":
                    self.environment = Environment.ZONEA
                if self.yaml_vars["environment"].lower() == "prod":
                    self.environment = Environment.PROD

    def __set_location_information(self):
        self.location = None
        if type(self.yaml_vars) is dict:
            if "location" in self.yaml_vars.keys():
                self.location = self.yaml_vars["location"]
        if (self.location is None or self.location == ""):
            if "resource_group_name" in self.pulumi_vars:
                self.location = get_location_from_resource_group(self.pulumi_vars["resource_group_name"])
            else:
                self.location = get_location_from_resource_group(get_resource_group_from_subscription(login_config=self.login_config))

    def __set_storage_account_information(self):
        self.storage_account_resource_group_name = None
        self.file_share_name = None
        self.storage_account_name = None
        self.storage_account_sku = "Standard_ZRS"
        self.storage_container_name = None
        self.sas_token_name = "pulumisas"
        if self.random_value is not None:
            self.sas_token_name = self.sas_token_name + self.random_value
        if type(self.yaml_vars) is dict:
            if "storage_account" in self.yaml_vars:
                if "name" in self.yaml_vars["storage_account"]:
                    self.storage_account_name = self.yaml_vars["storage_account"]["name"]
                    if self.storage_account_name is not None and self.random_value is not None:
                        self.storage_account_name = self.storage_account_name + self.random_value
                else:
                    print("Storage account name not defined in YAML. Exiting...")
                    exit
                if "resource_group" in self.yaml_vars["storage_account"]:
                    self.storage_account_resource_group_name = self.yaml_vars["storage_account"]["resource_group"]
                else:
                    self.storage_account_resource_group_name = get_resource_group_from_subscription(login_config=self.login_config)
                if "sku" in self.yaml_vars["storage_account"]:
                    self.storage_account_sku = self.yaml_vars["storage_account"]["sku"]
                if "storage_container" in self.yaml_vars["storage_account"]:
                    self.storage_container_name = self.yaml_vars["storage_account"]["storage_container"]["name"]
                    if self.storage_container_name is not None and self.random_value is not None:
                        self.storage_container_name = self.storage_container_name + self.random_value
                else:
                    print("Storage account name not defined in YAML. Exiting...")
                    exit
                if "sas_token" in self.yaml_vars["storage_account"]:
                    if "name" in self.yaml_vars["storage_account"]["sas_token"]:
                        self.sas_token_name = self.yaml_vars["storage_account"]["sas_token"]["name"]
                        if self.sas_token_name is not None and self.random_value is not None:
                            self.sas_token_name = self.sas_token_name + self.random_value
                    else:
                        print("SAS token name not defined in YAML. Using \"" + self.sas_token_name + "\" as the name of the secret when storing in the AKV.")
                else:
                    print("SAS token name not defined in YAML. Using \"" + self.sas_token_name + "\" as the name of the secret when storing in the AKV.")
            else:
                print("No storage account defined in the YAML config. Exiting...")
                exit

    def __set_key_vault_information(self):
        self.key_vault_resource_group_name = None
        self.key_vault_name = None
        self.encryption_key_name = None
        if type(self.yaml_vars) is dict:
            if "key_vault" in self.yaml_vars:
                if "name" in self.yaml_vars["key_vault"]:
                    self.key_vault_name = self.yaml_vars["key_vault"]["name"]
                    if self.key_vault_name is not None and self.random_value is not None:
                        self.key_vault_name = self.key_vault_name + self.random_value
                else:
                    print("Name for Azure Key Vault not found in YAML. Exiting...")
                    exit
                if "resource_group" in self.yaml_vars["key_vault"]:
                    self.key_vault_resource_group_name = self.yaml_vars["key_vault"]["resource_group"]
                else:
                    self.key_vault_resource_group_name = get_resource_group_from_subscription(login_config=self.login_config)
                if "encryption_key" in self.yaml_vars["key_vault"]:
                    self.encryption_key_name = self.yaml_vars["key_vault"]["encryption_key"]
                else:
                    print("Name for pulumi encryption key not found in YAML. Exiting...")
                    exit
            else:
                print("No key vault was defined in the YAML config. Exiting...")
                exit

    def __run_pulumi_command(self, command: str, is_secret : bool=False):
        output = None
        try:
            output = send_os_command(command=command, cwd=self.pulumi_directory, env=self.environment_vars, is_secret=is_secret)
        except subprocess.CalledProcessError as e:
            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.stderr))
            raise subprocess.CalledProcessError(
                returncode=e.returncode, 
                cmd=e.cmd, 
                output=e.output, 
                stderr=e.stderr)
        return output

    def __pulumi_set_config(self, namespace : str, config_variable_name : str, value : str, is_secret : bool=False):
        if namespace is not None and namespace != "":
            pass
        else:
            print("namespace was not provided to 'pulumi config " + namespace + ":" + config_variable_name + "' command. Skipping...")
            return
        if config_variable_name is not None and config_variable_name != "":
            pass
        else:
            print("config_variable_name was not provided to 'pulumi config" + namespace + ":" + config_variable_name + "' command. Skipping...")
            return
        if value is not None and value != "":
            pass
        else:
            print("value was not provided to 'pulumi config " + namespace + ":" + config_variable_name + "' command. Skipping...")
            return

        if is_secret:
            self.__run_pulumi_command("/pulumi/bin/pulumi config set --secret " + namespace + ":" + config_variable_name + " " + value, True)
        else:
            self.__run_pulumi_command("/pulumi/bin/pulumi config set " + namespace + ":" + config_variable_name + " " + value + " --plaintext")

    def __setup_storage_account(self):
        print("Setting up storage account for file share connected to Azure Container Instance.")
        if self.storage_account_resource_group_name and self.storage_account_name:
            az_cli_command = "az storage account list -G " + self.storage_account_resource_group_name
            output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
            storage_account_exists = False
            for account in output:
                if account["name"] == self.storage_account_name:
                    print("Storage account " + self.storage_account_name + " in resource group " + self.storage_account_resource_group_name + " already exists. Nothing to do.")
                    storage_account_exists = True
                    break
            if not storage_account_exists:
                print("Creating storage account " + self.storage_account_name + " in resource group " + self.storage_account_resource_group_name)
                az_cli_command = "az storage account create --name " + self.storage_account_name + " --resource-group " + self.storage_account_resource_group_name + " --location " + self.location + " --sku " + self.storage_account_sku + " --encryption-services blob --allow-blob-public-access false"
                output = send_os_command(az_cli_command)
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.storage_account_resource_group_name: " + str(self.storage_account_resource_group_name))
            print("self.storage_account_name: " + str(self.storage_account_name))
            exit()

    def __setup_storage_container(self):
        if self.storage_account_resource_group_name and self.storage_account_name and self.storage_container_name:
            az_cli_command = "az storage container exists --account-name " + self.storage_account_name + " --auth-mode login --name " + self.storage_container_name
            output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
            container_exists = False
            if "exists" in output and output["exists"] == True:
                print("Storage container " + self.storage_container_name + " in storage account " + self.storage_account_name + " already exists. Nothing to do.")
                container_exists = True
            if not container_exists:
                print("Creating storage container " + self.storage_container_name + " in storage account " + self.storage_account_name + ".")
                az_cli_command = "az storage container create --account-name " + self.storage_account_name + " --name " + self.storage_container_name + " --auth-mode login"
                output = send_os_command(az_cli_command)
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.storage_account_resource_group_name: " + str(self.storage_account_resource_group_name))
            print("self.storage_account_name: " + str(self.storage_account_name))
            print("self.storage_container_name: " + str(self.storage_container_name))
            exit()

    def __setup_key_vault(self):
        if self.key_vault_name and self.key_vault_resource_group_name:
            key_vault_exists = False
            try:
                az_cli_command = "az keyvault list"
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
                for kv in output:
                    if kv["name"] == self.key_vault_name:
                        print("Key vault " + self.key_vault_name + " exists. Nothing to do.")
                        key_vault_exists = True
                        break
            except subprocess.CalledProcessError as e:
                print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                print("Cannot determine if a key vault with the name " + self.key_vault_name + " exists in the subscription. Exiting...")
                exit()
            if not key_vault_exists:
                az_cli_command = "az keyvault check-name --name " + self.key_vault_name
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
                if "nameAvailable" in output:
                    if output["nameAvailable"] == True:
                        try:
                            az_cli_command = "az keyvault create --name " + self.key_vault_name + " --resource-group " + self.key_vault_resource_group_name + " --location " + self.location
                            output = send_os_command(az_cli_command)
                        except subprocess.CalledProcessError as e:
                            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                            print("Could not create Azure Key Vault with name: " + self.key_vault_name)
                            print("Please choose a new name for the Azure Key Vault.")
                            exit
                    else:
                        print("Cannot create a key vault with the name: " + self.key_vault_name)
                        exit()
                else:
                    print("nameAvailable was not found in JSON output returned from az cli command.")
                    exit()
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.key_vault_resource_group_name: " + str(self.key_vault_resource_group_name))
            exit()

    def __setup_encryption_key(self):
        if self.key_vault_name and self.encryption_key_name:
            self.__setup_key_vault()
            key_exists = False
            try:
                az_cli_command = "az keyvault key show --name " + self.encryption_key_name + " --vault-name " + self.key_vault_name
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
                if "key" in output and "kid" in output["key"]:
                    key_exists = True
                    print("Key " + self.encryption_key_name + " exists in key vault " + self.key_vault_name + ". Nothing to do.")
            except subprocess.CalledProcessError:
                pass
            if not key_exists:
                az_cli_command = "az keyvault key create --name " + self.encryption_key_name + " --vault-name " + self.key_vault_name
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.encryption_key_name: " + str(self.encryption_key_name))
            exit()

    def __setup_sas_token(self):
        if self.key_vault_name and self.sas_token_name:
            self.sas_token = get_secret_from_key_vault(self.key_vault_name, self.sas_token_name)
            if sas_token is not None:
                print("Using the current SAS from Azure Key Vault. Nothing to do.")
            else:
                start_date = datetime.utcnow().date().strftime("%Y-%m-%dT%H:%M:%SZ")
                expiration_date = (datetime.utcnow() + timedelta(days=7)).date().strftime("%Y-%m-%dT%H:%M:%SZ")
                az_cli_command = "az storage container generate-sas --account-name " + self.storage_account_name + " --name " + self.storage_container_name + " --permissions acdlrw --start " + start_date + " --expiry " + expiration_date + " --https-only --auth-mode login --as-user"
                sas_token = send_os_command(az_cli_command, is_secret=True)
                self.sas_token = ("".join(sas_token)).strip().replace('"', '')
                az_cli_command = "az keyvault secret set --name " + self.sas_token_name + " --vault-name " + self.key_vault_name + " --value " + self.sas_token + " --expires " + expiration_date
                output = sanitize_stdout_for_json(send_os_command(az_cli_command))
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.sas_token_name: " + str(self.sas_token_name))
            exit()