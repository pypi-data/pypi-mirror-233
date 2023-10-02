# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class Instance:
    """Data necessary for the Ansible inventory of an instance"""

    name: str = ""
    IP: str = ""
    groups: list[str] = field(default_factory=list)
    vars: list[str] = field(default_factory=list)


@dataclass
class Inventory:
    """Inventory definition class that generate the Ansible inventory file"""

    instances: list[Instance] = field(default_factory=list)
    instances_by_group: dict[str, list[str]] = field(default_factory=dict)
    max_len_name: int = 0

    def prepare(self) -> None:
        """Analyse data and pre-format the Ansible inventory"""

        for instance in self.instances:
            if len(instance.name) > self.max_len_name:
                self.max_len_name = len(instance.name)

            for group in instance.groups:
                if group in self.instances_by_group.keys():
                    self.instances_by_group[group].append(instance.name)
                else:
                    self.instances_by_group[group] = [instance.name]

    def generate(self) -> str:
        """Generate the Ansible inventory file

        Returns:
            str: The inventory file content
        """
        output: str = ""

        self.prepare()

        for instance in self.instances:
            spaces_count = self.max_len_name - len(instance.name)
            spaces = " " * spaces_count
            output += instance.name + spaces

            if len(instance.IP) > 0:
                output += f" ansible_host={instance.IP}"

            for var in instance.vars:
                output += f" {var}"
            output += "\n"

        for group in self.instances_by_group:
            output += "\n"
            output += f"[{group}]\n"

            for instance_name in self.instances_by_group[group]:
                output += f"{instance_name}\n"

        return output
