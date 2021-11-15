# Who Moved My GPU?

Get GPU information from various servers via ssh

## Why should this exist?

'cause I'm lazy

## Structure of the server

```text
webroot
├─ gpu (main page)
└─ fix (fix display)
```

## How to use the ready-made executable?

### [Windows]

Just download from *Release*, unzip, **write config** and execute!

The desired page should be at `127.0.0.1:1301/gpu` by default.

### [Unix-like]

Why bother?

## How to directly run the Python script?

### [OS-invariant]

* Set up the environment

```shell
pip install -r requirements.txt
```

* Run app.py with flask

```shell
flask run -h 0.0.0.0 -p 1301
```

**Note that** the ip address along with port could be changed here.

## How to compile from scratch?

### [Windows-only]

* Set up the environment

```shell
pip install -r requirements.txt
```

* Build exectuable with pyinstaller

```shell
pyinstaller --clean -F app.py -p ssh.py --add-data ".\templates\*;.\templates" --add-data ".\static\*;.\static" -i GPU.ico -n WhoMovedMyGPU --noconsole
```

## About configuration file

The ssh.config file should look like this:

```text
[config]
refresh = 30
timeout = 10
# 20s for warmup
warmup = 4

[example 1]
hostname = 0.0.0.0
port = 22
username = guest
password = 123456

[example 2]
hostname = 1.2.3.4
port = 33
username = guest
password = 123456
```

**Note that** the **[config]** block should never be renamed, and should always be the first item.

## Scripts for convenience

There are some scripts(.bat) provided in the *util* folder, which could be of some help.

### [optional]

The file **auto.bat** should be put beside the executable or Python script for the webserver to reboot itself.
