import os
import json
import subprocess
import time
from flask import Flask, stream_with_context, Response

app = Flask(__name__)
VERSION = "1.3.3-beta2"

@app.route('/')
def index():
    return 'OK'

# api_key, cookie, session_token, user_langのいずれかが書かれていたらconfig.txtを更新
def env_to_config():
    envs_src = ["api_key", "cookie", "session_token", "user_lang"]
    envs = dict([(e, os.getenv(e, "")) for e in envs_src])
    envs_available = any(envs.values())
    if envs_available:
        yield ('#Start Update config.txt')
        with open('config.txt', 'w') as file:
            file.write(json.dumps(envs))
        yield ('#Done Update config.txt')

def update_submodules():
    yield ("#Start Update git submodules")
    subprocess.call(["git", "submodule", "foreach", "git", "reset", "--hard", ])
    subprocess.call(["git", "submodule", "foreach", "git", "pull", "origin", "master", ])
    yield ("#Done Update git submodules")

def sync_salmon():
    salmon_args = ["python", "./splatnet2statink/splatnet2statink.py", "--salmon", "-r"]
    yield ('#Start Run {}'.format(salmon_args))
    p = subprocess.Popen(salmon_args, stdin=subprocess.PIPE, encoding="utf8")
    p.stdin.write("50")
    p.stdin.close()
    p.wait()
    yield ('#Done Run {}'.format(salmon_args))

def sync_battle():
    args = ["python", "./splatnet2statink/splatnet2statink.py"]
    flags = os.getenv("run_flags", "-r").split(" ")
    args.extend(flags)
    yield ('#Start Run {}'.format(args))
    subprocess.call(args)
    yield ('#Done Run {}'.format(args))

@app.route('/sync')
def sync_all():
    # 時間計測
    start = time.time()
    # Docker環境変数からコンフィグを生成
    for log in env_to_config():
        yield log
    # submoduleで追加されたsplatnet2statinkを更新
    if not(os.getenv("skip_update", "")):
        for log in update_submodules():
            yield log
    # 実行
    for log in sync_battle():
        yield log
    # Salmon runを更新する
    if not(os.getenv("skip_salmon", "")):
        for log in sync_salmon():
            yield log
    elapsed = time.time() - start
    yield ("elapsed_time: {}".format(elapsed))

if __name__ == "__main__":
    print("splatnet2statink-docker v{}".format(VERSION))
    run_flask = os.getenv("flask_run", "")
    run_port = os.getenv("flask_port", "8080")
    debug = os.getenv("flask_debug", "True")
    if (run_flask):
        print("REST API mode. port {} listen ...".format(run_port))
        app.run(debug=debug, host="0.0.0.0", port=run_port)
    else:
        for log in sync_all():
            print(log)


