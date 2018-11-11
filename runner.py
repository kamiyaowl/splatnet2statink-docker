import os
import json
import subprocess
import time
from flask import Flask

app = Flask(__name__)
VERSION = "1.3.3-beta"

@app.route('/')
def index():
    return 'OK'

# api_key, cookie, session_token, user_langのいずれかが書かれていたらconfig.txtを更新
def env_to_config():
    envs_src = ["api_key", "cookie", "session_token", "user_lang"]
    envs = dict([(e, os.getenv(e, "")) for e in envs_src])
    envs_available = any(envs.values())
    if envs_available:
        print('#Start Update config.txt')
        with open('config.txt', 'w') as file:
            file.write(json.dumps(envs))
        print('#Done Update config.txt')

def update_submodules():
    print("#Start Update git submodules")
    subprocess.call(["git", "submodule", "foreach", "git", "reset", "--hard", ])
    subprocess.call(["git", "submodule", "foreach", "git", "pull", "origin", "master", ])
    print("#Done Update git submodules")

def sync_salmon():
    salmon_args = ["python", "./splatnet2statink/splatnet2statink.py", "--salmon", "-r"]
    print('#Start Run {}'.format(salmon_args))
    p = subprocess.Popen(salmon_args, stdin=subprocess.PIPE, encoding="utf8")
    p.stdin.write("50")
    p.stdin.close()
    p.wait()
    print('#Done Run {}'.format(salmon_args))

def sync_battle():
    args = ["python", "./splatnet2statink/splatnet2statink.py"]
    flags = os.getenv("run_flags", "-r").split(" ")
    args.extend(flags)
    print('#Start Run {}'.format(args))
    subprocess.call(args)
    print('#Done Run {}'.format(args))

@app.route('/sync')
def sync_all():
    # 時間計測
    start = time.time()
    # Docker環境変数からコンフィグを生成
    env_to_config()
    # submoduleで追加されたsplatnet2statinkを更新
    if not(os.getenv("skip_update", "")):
        update_submodules()
    # 実行
    sync_battle()
    # Salmon runを更新する
    if not(os.getenv("skip_salmon", "")):
        sync_salmon()
    elapsed = time.time() - start
    result = "elapsed_time: {}".format(elapsed)
    print(result)
    return result

if __name__ == "__main__":
    print("splatnet2statink-docker v{}".format(VERSION))
    run_flask = os.getenv("flask_run", "")
    run_port = os.getenv("flask_port", "8080")
    debug = os.getenv("flask_debug", "True")
    if (run_flask):
        print("REST API mode. port {} listen ...".format(run_port))
        app.run(debug=debug, host="0.0.0.0", port=run_port)
    else:
        sync_all()


