# HCS CLI Development Guide

- [HCS CLI Development Guide](#hcs-cli-development-guide)
  - [Introduction](#introduction)
  - [Install hcs-cli from local repo](#install-hcs-cli-from-local-repo)
  - [Create a new HCS CLI command](#create-a-new-hcs-cli-command)
    - [Add a command file](#add-a-command-file)
    - [Run the new command](#run-the-new-command)
    - [Lint Code](#lint-code)
    - [Unit Test](#unit-test)
  - [Debug HCS CLI](#debug-hcs-cli)
  - [References](#references)
    - [Command Return Value](#command-return-value)
      - [Specify Return Value](#specify-return-value)
      - [Return error with non-zero return code](#return-error-with-non-zero-return-code)
    - [Convention](#convention)
      - [Exception](#exception)
    - [Code Structure: Packages Explained](#code-structure-packages-explained)
  - [Publish to PyPI](#publish-to-pypi)
    - [Prepare authentication to pypi](#prepare-authentication-to-pypi)
    - [Publish](#publish)


## Introduction
- This guide describes how to develop HCS CLI commands

- Before getting started, follow [HCS CLI - User Guide](hcs-cli-user-guide.md) to setup basic requirements.

- If you are for how to use/develop HCS Plan, refer to [HCS CLI - Plan](hcs-plan.md).

## Install hcs-cli from local repo
To develop hcs-cli code and use local source code:

Update dependencies

```bash
brew install python3
# Make sure the python version >= 3.10
python3 --version

git@gitlab.eng.vmware.com:horizonv2-labs/lab/hcs-cli.git
cd hcs-cli
pip3 install -r requirements-dev.txt

# Install the CLI from local source repo, so any change takes effect immediately via the "hcs" command:

make devinstall

# Check the availability of HCS command:
hcs --version
```

## Create a new HCS CLI command

### Add a command file
This tutorial introduces how to add a new subgroup, and add a new command in that group.

1. Create a new folder "dev" in "vhcs/cli/cmds"
2. Create a new file "hello.py" in the new folder "vhcs/cli/cmds/dev/hello.py", with the following content:


```python
import click
 
@click.command()
@click.argument("name", type=str, required=True)
def hello(name: str):
    """Say hello"""
    return {
        "hello": name
    }
```

### Run the new command
```bash
hcs dev hello mortal
```

You should get:
```
{
    "hello": "mortal"
}
```
If the command is not found, refer to section [Install hcs-cli from local repo](#install-hcs-cli-from-local-repo)


### Lint Code
hcs-cli uses the black style without customization. We have more important things than style debating to worry about.
```bash
make lint
```


### Unit Test
To run all unit tests
```bash
make test
```

To run a specific unit test
```bash
cd tests
python3 -m unittest vhcs.cli.cmds.plan.test_plan.TestPlan.test10_basic -v
```

To debug a test in IDE

<img src="images/hcs-dev-run-test.png" width="600px"/>


## Debug HCS CLI

1. Install [VS Code and prepare for Python](https://code.visualstudio.com/docs/python/python-tutorial).

2. Configure

   <img src="images/hcs-debug-1.png" width="600px"/>

3. Choose proper Python Intepreter
   
   <img src="images/hcs-debug-2.png" width="200px"/>

   <img src="images/hcs-debug-3.png" width="600px"/>

   <img src="images/hcs-debug-4.png" width="600px"/>
   
4. Add breakpoint and start debugging
   
   <img src="images/hcs-debug-5.png" width="600px"/>



## References

### Command Return Value

#### Specify Return Value
The default function return will be handled as data object and formated as CLI output. The output is formated according to common output parameters "–output" (e.g. json, yaml, etc).

Example of a command, which get an LCM template by ID:

```python
import click
from vhcs.service import lcm
 
@click.command()
@click.argument("id", type=str, required=True)
def get(id: str):
    """Get template by ID"""
    return lcm.template.get(id)
```

#### Return error with non-zero return code
If a failure case is encountered, the CLI should return a non-zero return code per convention. The second return value, if exists and is integer, will be used as return value.
In such error scenario, the output will be printed to STDERR, instead of STDOUT.
```python
@click.command()
def demoerror():
    """Demo error return"""
    my_shell_return_code = 123
    return "something wrong", my_shell_return_code
```

Or alternatively:
```python
import vhcs.common.ctxp as ctxp
@click.command()
def demoerror():
    """Demo error return"""
  return ctxp.error("Only set or get should be specified.")
```

By default, if an exception is thrown from a command function, it is considered as error and the CLI will have a non-zero return code.

### Convention
Refer to [IO Convention](hcs-cli-suer-guide.md#io-convention)

#### Exception
* For known cases, exception & stack trace should be avoided. E.g. anticipated IO failures
* For unknown cases, exception & stack track must NOT be omitted and should be printed to STDERR.

### Code Structure: Packages Explained

| Directory | Purpose |
| --------- | ------- |
| .vscode | VS Code configurations |
| build | Generated folder during build |
| dist | Generated folder during build |
| doc | Documentations |
| hcs_cli.egg-info | Generated folder during build |
| payload | HCS API related payload templates. |
| tests | Unit tests |
| vhcs/cli | CLI command implementations |
| vhcs/config | Configuration files |
| vhcs/ctxp | Common library for Context Programming |
| vhcs/ext | Domain specific extensions |
| vhcs/plan | The plan engine |
| vhcs/service | HCS service wrappers |
| vhcs/sglib | Common library for HCS |
| vhcs/util | Utilities |


## Publish to PyPI
Note: this step is NOT needed for daily development. This step is only needed for the public to get the updated HCS CLI using "pip3 install hcs-cli".

### Prepare authentication to pypi
Create the pypi config file

vi ~/.pypirc
Put the following content, and save the file.
```ini
[distutils]
  index-servers =
    pypi
    hcs-cli
 
[pypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
 
[hcs-cli]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = <an-auth-token-ask-dev-to-join-the-project-and-generate-your-own>
```

### Publish
```
make release
```
