# HCS CLI User Guide

- [HCS CLI User Guide](#hcs-cli-user-guide)
  - [Setup Prerequisites](#setup-prerequisites)
    - [Mac](#mac)
    - [Ubuntu](#ubuntu)
    - [Windows](#windows)
    - [Troubleshooting Installation](#troubleshooting-installation)
      - [Error: "Command not found: hcs"](#error-command-not-found-hcs)
        - [Mac](#mac-1)
        - [Ubuntu](#ubuntu-1)
  - [Authentication](#authentication)
    - [Method 1 - Interactive Login Via Browser](#method-1---interactive-login-via-browser)
    - [Method 2 - Using CSP User API Token](#method-2---using-csp-user-api-token)
      - [Get CSP User API Token](#get-csp-user-api-token)
    - [Method 3 - Using CSP OAuth app client id/secret](#method-3---using-csp-oauth-app-client-idsecret)
    - [Get authentication details](#get-authentication-details)
    - [Security Practice](#security-practice)
  - [Profile - Working with multiple environments or different users](#profile---working-with-multiple-environments-or-different-users)
  - [Customize Output](#customize-output)
    - [Customize Output Format](#customize-output-format)
    - [Customize Output Fields](#customize-output-fields)
  - [Convention](#convention)
    - [Parameter \& Input](#parameter--input)
    - [Return Code](#return-code)
    - [Output](#output)
  - [Next](#next)


## Setup Prerequisites
### Mac
```zsh
brew update
brew install python3
python3 --version
# Make sure python version is above 3.10

python3 -m ensurepip
pip3 --version
```

### Ubuntu
```bash
sudo apt update
sudo apt install python3 -y
python3 --version
sudo apt install python3-pip -y
pip3 --version
# By default, on Ubuntu, python setup will not put hcs cli executable to
# the generic /usr/local/bin, but ~/.local/bin, which is not on the path.
# Add it to the path:
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Windows
Install python 3.11 from Windows App Store, then:
```bash
pip install hcs-cli
```
With default installation, it will show a message like:
```
WARNING: The script xxx is installed in 'C:\Users\xxx\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_xxxxx\LocalCache\local-packages\Python311\Scripts' which is not on PATH.
```
Add that path above to system or user path.


### Troubleshooting Installation
#### Error: "Command not found: hcs"
In some environment due to permission issue, the setup can not create the starter script. To fix it:

##### Mac
Create the file
```bash
sudo vi /usr/local/bin/hcs
```
Copy-paste the following as the file content:
```bash
#!/usr/local/opt/python@3.11/bin/python3.11
# -*- coding: utf-8 -*-
import re
import sys
from vhcs.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
Add execution permission:
```bash
sudo chmod +x /usr/local/bin/hcs
```

##### Ubuntu
```bash
sudo vi ~/.local/bin/hcs
```
Copy-paste the following as the file content:
```bash
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from vhcs.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
Add execution permission:
```bash
sudo chmod +x ~/.local/bin/hcs
```

## Authentication

### Method 1 - Interactive Login Via Browser
```
hcs login [--org <org-id>]
```
Org ID is not required if the default CSP org is the target org to login.

### Method 2 - Using CSP User API Token

If interactive browser login is not feasible (e.g. no browser), user API token can be used to authenticate HCS CLI:

```
hcs login --api-token <csp-api-token>
```

#### Get CSP User API Token
1. Goto CSP console
   1. Production: https://console.cloud.vmware.com/ 
   2. Staging: https://console-stg.cloud.vmware.com/
2. Click right top user name to bring the dropdown menu.
3. If needed, change organization to the desired one.
4. Click the right top user name to bring the dropdown menu, click "My Account"
5. Click "API Tokens" tab
6. Click "Generate a New API Token"
7. Provide proper input in the form, generate the token, and copy the token after generated.
8. 
### Method 3 - Using CSP OAuth app client id/secret
The OAuth app represents a service identity. It's normally used for development purposes.
```
hcs login --client-id <client-id> --client-secret <client-secret> [--org \<org-id\>]
```
### Get authentication details
```
hcs login -d
```

### Security Practice
HCS CLI stores authentication information in a conventional way. The profile and authentication state after login are stored in the current user home directory. The best practice is to use it on a single user system with admin privilege.

## Profile - Working with multiple environments or different users

By default, HCS CLI is configured to use production environment. To work with a custom environment, or configure a different authentication identity, profile is the way. 

There are multiple ways to create additional profiles.
1. Create the default profiles for development environments:
```
hcs profile init --dev
```
2. Create a custom profile, either for using a different identity for authentication, or for using a feature stack, copy an existing profile to create a new one:

```
hcs profile copy --from \<src-name\> --to \<target-name>
hcs profile edit
```
Switch between profiles:
```
hcs profile use
```

## Customize Output

### Customize Output Format

  * There are common parameters to control output format:

  * --output <json | yaml | text>
  * -o  <json | yaml | text>

  Example:

  * hcs -o=yaml admin template get <id>

### Customize Output Fields

Instead of output the full json, which is normally large, use the --field argument to selectively keep fields to output.

  * --field <comma separated field names>
  * -f <comma separated field names>

Schema:

  * hcs --field <comma-separated-field-names> <subcommand> [ ... ]

Example:

  * hcs --field id,name lcm template get ras-07110204-2047
  * hcs --field id,name lcm template list

For advanced output manipulation, use the "jq" tool.

Examples:

  * hcs admin template list | jq ".[] | count"
  * hcs admin template list | jq ".[] | map(.id)"


## Convention

This section describes the convention & parameters that apply to all subcommands.

### Parameter & Input
* Unix default double dash.
* Support STDIN for file-based input.

### Return Code
  * 0: successful execution
  * Non-zero: problematic execution
### Output
  * STDOUT for output
  * STDERR for error details
  * JSON format by default. Overridable to human-readable or yaml



## Next
- [HCS CLI - Cheatsheet](hcs-cli-cheatsheet.md)
- [HCS CLI - Dev Guide](hcs-cli-dev-guide.md)
- [HCS Plan](hcs-plan.md)
