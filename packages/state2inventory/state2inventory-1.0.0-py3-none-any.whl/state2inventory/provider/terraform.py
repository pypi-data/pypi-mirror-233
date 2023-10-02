# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from output.inventory import Inventory, Instance
from typing import ClassVar


@dataclass
class Terraform:
    """Terraform provider, extract data for an Ansible inventory
    from the terraform command:
    terraform show -json
    """

    json_data: str
    json_key: str = ""
    KEY_TYPE: ClassVar[str] = "openstack_compute_instance_v2"
    KEY_IP: ClassVar[str] = "access_ip_v4"
    KEY_GROUPS: ClassVar[str] = "host_groups"
    KEY_VARS: ClassVar[str] = "host_vars"

    def parse(self) -> Inventory:
        """Parse data from terraform show -json command

        Raises:
            JSONDecodeError: If the file has not a valid JSON format
            KeyError: If a required key is not found

        Returns:
            Inventory: An Inventory object
        """
        key_type: str = Terraform.KEY_TYPE
        key_ip: str = Terraform.KEY_IP
        key_groups: str = Terraform.KEY_GROUPS
        key_vars: str = Terraform.KEY_VARS

        if (self.json_key is not None) and (len(self.json_key) > 0):
            try:
                key_dict = json.loads(self.json_key)
            except JSONDecodeError as jde:
                raise ValueError("Wrong JSON file format for key option: " + str(jde))
            key_list = key_dict.keys()
            if "type" in key_list:
                key_type = key_dict["type"]
            if "ip" in key_list:
                key_ip = key_dict["ip"]
            if "groups" in key_list:
                key_groups = key_dict["groups"]
            if "vars" in key_list:
                key_vars = key_dict["vars"]

        try:
            tf_dict = json.loads(self.json_data)
            resources = tf_dict["values"]["root_module"]["resources"]
            inventory = Inventory()

            for resource in resources:
                if ("type" in resource.keys()) and (resource["type"] == key_type):
                    values_keys = resource["values"].keys()
                    if "name" in values_keys:
                        name = resource["values"]["name"]
                    else:
                        name = resource["name"]
                    instance = Instance(name)

                    if key_ip in values_keys:
                        instance.IP = resource["values"][key_ip]

                    if "metadata" in values_keys:
                        metadata = resource["values"]["metadata"]
                        if key_groups in metadata:
                            groups = resource["values"]["metadata"][key_groups]
                            instance.groups = groups.split(";")

                        if key_vars in metadata:
                            vars = resource["values"]["metadata"][key_vars]
                            instance.vars = vars.split(";")

                    inventory.instances.append(instance)
            return inventory
        except JSONDecodeError as jde:
            raise ValueError(f"Wrong JSON file format for state file: {jde}")
        except KeyError as ke:
            raise ValueError(f"Key {ke} not found in state file")
