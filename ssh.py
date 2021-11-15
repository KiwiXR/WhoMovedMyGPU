import logging
import socket
import threading
import paramiko
import configparser
import csv
import io
import time


ref = {
    'timestamp': 0,
    'name': 1,
    'index': 2,
    'utilization.gpu': 3,
    'memory.total': 4,
    'memory.free': 5,
    'power.limit': 6,
    'power.draw': 7
}


pause = False


def visualize(ssh_id, host, csv_str_gpu, str_ncore, str_cpu, host_info):
    info = csv.reader(io.StringIO(csv_str_gpu))
    rec_g = []
    for line in info:
        name = line[ref['name']].strip()
        index = line[ref['index']].strip()
        util = line[ref['utilization.gpu']].strip()
        mem_tot = line[ref['memory.total']].strip()
        mem_fre = line[ref['memory.free']].strip()
        pwr_lim = line[ref['power.limit']].strip()
        pwr_drw = line[ref['power.draw']].strip()
        rec_g.append([name, index, util, mem_tot, mem_fre, pwr_lim, pwr_drw])
    rec_c = str_cpu.strip().split(' ')
    rec_n = str_ncore.strip()
    host_info[ssh_id] = [host, rec_g, rec_n, rec_c]


def query_host(ssh_id, host, ssh_cfg, host_info, timeout):
    # create
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # always try to reconnect if connection failed
        while True:
            try:
                # connect
                ssh.connect(hostname=ssh_cfg["hostname"], port=ssh_cfg["port"], username=ssh_cfg["username"], password=ssh_cfg["password"], timeout=timeout)

                gpu_str = "nvidia-smi --format=csv,noheader --query-gpu=timestamp,name,index,utilization.gpu,memory.total,memory.free,power.limit,power.draw"

                ncore_str = "cat /proc/cpuinfo | grep processor | wc -l"
                cpu_str = "cat /proc/loadavg"

                while True:
                    stdin, stdout, stderr = ssh.exec_command(gpu_str, timeout=timeout)

                    out, err = stdout.read(), stderr.read()
                    if not out:
                        raise paramiko.SSHException
                    res_g = out
                    res_g = res_g.decode()

                    stdin, stdout, stderr = ssh.exec_command(ncore_str, timeout=timeout)

                    out, err = stdout.read(), stderr.read()
                    if not out:
                        raise paramiko.SSHException
                    res_n = out
                    res_n = res_n.decode()

                    stdin, stdout, stderr = ssh.exec_command(cpu_str, timeout=timeout)

                    out, err = stdout.read(), stderr.read()
                    if not out:
                        raise paramiko.SSHException
                    res_c = out
                    res_c = res_c.decode()
                    visualize(ssh_id, host, res_g, res_n, res_c, host_info)
                    time.sleep(3)
            except (paramiko.SSHException, socket.error):
                continue
    except Exception as e:
        logging.exception(e)
    finally:
        ssh.close()


def init():
    cfg = configparser.ConfigParser()
    cfg.read("ssh.config", encoding="utf-8")

    host_names = cfg.sections()
    cfg_name, host_names = host_names[0], host_names[1:]

    if cfg_name != 'config':
        raise Exception('[config] item should come first in configure file!')
    cfg_dict = {}
    cfg_dict['refresh'] = cfg.getint(cfg_name, 'refresh')
    cfg_dict['timeout'] = cfg.getint(cfg_name, 'timeout')
    cfg_dict['warmup'] = cfg.getint(cfg_name, 'warmup')

    ssh_pool = {}
    for host in host_names:
        # read from config file
        hostname = cfg.get(host, "hostname")
        port = cfg.getint(host, "port")
        username = cfg.get(host, "username")
        password = cfg.get(host, "password")
        ssh_cfg = {"hostname": hostname, "port": port, "username": username, "password": password}

        # record
        ssh_pool[host] = ssh_cfg

    return ssh_pool, cfg_dict


if __name__ == '__main__':
    ssh_pool = init()
    host_info = {}
    for (ssh_id, (host, ssh_cfg)) in enumerate(ssh_pool.items()):
        t = threading.Thread(target=query_host, args=(ssh_id, host, ssh_cfg, host_info))
        t.start()
    print(host_info)
    time.sleep(0.55)
    print(host_info)
    time.sleep(1)
    print(host_info)
    time.sleep(1)
    print(host_info)
    time.sleep(1)
    print(host_info)
