Project description

SSH Client Package


#Simple, Fast and Secure method to:

- Create automated tools to back-up Routers, Switches and Access-Points
- Create automated tools for dynamic network configuration generation
- Create automated tools for configurations roll-out
- Create automated tools for network devices audit
- Create automated tools for network devices inventory generation
- Create automated tools for network devices troubleshooting

##How to use the Package.

###How to send a single command to a remote host 'in global config mode'

#####Download the package in your computer

pip install sshFRIEND

#####Inside your script, do the following:

- from sshFRIEND.ssh_connector import *

- hostname = "your hostname here"

- username = "your username here"

- password = "your password here"

- cmd = "show running-config"

- channel = ssh_connector(hostname, username, password)

- output = send_cmd(cmd, channel)

- print(output)


###How to send a single command to a remote host 'in config mode'

#####Inside your script, do the following:

- from sshFRIEND.ssh_connector import *

- hostname = "your hostname here"

- username = "your username here"

- password = "your password here"

- cmd = "show running-config"

- channel = ssh_connector(hostname, username, password)

- output = send_config_cmd(cmd, channel)

- print(output)


###How to send multiple commands to a remote host 'in global config mode'

#####Inside your script, do the following:

- from sshFRIEND.ssh_connector import *

- hostname = "your hostname here"

- username = "your username here"

- password = "your password here"

- list_of_commands = ["show running-config", "show running-config"]

- channel = ssh_connector(hostname, username, password)

- output = send_cmds(list_of_commands, channel)

- print(output)


###How to send multiple commands to a remote host 'in config mode'

##### Inside your script, do the following:

- from sshFRIEND.ssh_connector import *

- hostname = "your hostname here"

- username = "your username here"

- password = "your password here"

- list_of_commands = ["show running-config", "show running-config"]

- channel = ssh_connector(hostname, username, password)

- output = send_config_cmds(list_of_commands, channel)

- print(output)