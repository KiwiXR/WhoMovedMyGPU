# Who Moved My GPU?

>Get GPU information from various servers via ssh

- [Who Moved My GPU?](#who-moved-my-gpu)
  - [Why should this exist?](#why-should-this-exist)
  - [Structure of the server](#structure-of-the-server)
  - [How to use the ready-made executable?](#how-to-use-the-ready-made-executable)
    - [[Windows]](#windows)
    - [[Unix-like]](#unix-like)
  - [How to directly run the Python script?](#how-to-directly-run-the-python-script)
    - [[OS-invariant]](#os-invariant)
  - [How to compile from scratch?](#how-to-compile-from-scratch)
    - [[Windows-only]](#windows-only)
  - [About configuration file](#about-configuration-file)
  - [Scripts for convenience](#scripts-for-convenience)
    - [[optional]](#optional)
  - [About [WinError 10013]](#about-winerror-10013)
    - [Recommended Solution](#recommended-solution)

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

## About [WinError 10013]

Indeed, it's sort of a headache.

As easily known, it's a problem caused by **Port Occupation**. Therefore, the common way to handle it is either to figure out the unexpected guest(i.e., a process) and wipe it out, or to change the port of this certain program. Either of the solutions sounds troublesome for lazybones.

On top of that, you could even be unable to find the specific process, should you have Hyper-V enabled in your Windows. As far as I know, some ports are dynamically excluded from TCP to favour Hyper-V.

### Recommended Solution

1. Run **CMD** or **PowerShell** as Administrator
2. Use the following code to view the excluded ports

    ```shell
    netsh interface ipv4 show excludedportrange protocol=tcp
    ```

3. Disable Hyper-V

    ```shell
    dism.exe /Online /Disable-Feature:Microsoft-Hyper-V
    ```

4. Reserve the desired port, e.g., the port 1301

    ```shell
    netsh int ipv4 add excludedportrange protocol=tcp startport=1301 numberofports=1
    ```

5. (Maybe after reboot) Enable Hyper-V

    ```shell
    dism.exe /Online /Enable-Feature:Microsoft-Hyper-V /All
    ```

6. (Maybe reboot again) All done and enjoy yourself
