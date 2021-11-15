import threading

from flask import Flask, render_template
import ssh

from gevent import pywsgi

app = Flask(__name__)

host_info = {}
cfg_dict = {}

@app.before_first_request
def start_ssh():
    global cfg_dict, host_info
    ssh_pool, cfg_dict = ssh.init()
    for (ssh_id, (host, ssh_cfg)) in enumerate(ssh_pool.items()):
        t = threading.Thread(target=ssh.query_host, args=(ssh_id, host, ssh_cfg, host_info, cfg_dict['timeout']))
        t.start()


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/gpu', methods=['GET', 'POST'])
def gpu():
    global host_info, cfg_dict
    host_i = dict(sorted(host_info.items(), key=lambda item: item[0]))
    if cfg_dict['warmup'] > 0:
        refresh = 5
        cfg_dict['warmup'] -= 1
    else:
        refresh = cfg_dict['refresh']
    return render_template('gpu.html', title='Who Moved My GPU?', host_info=host_i, refresh_time=refresh)


@app.route('/fix', methods=['GET', 'POST'])
def fix():
    return render_template('fix.html')


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 1301), app)
    server.serve_forever()
