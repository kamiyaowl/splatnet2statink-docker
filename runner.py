import os
import json
import subprocess
from subprocess import Popen, PIPE
import time
from flask import Flask, stream_with_context, Response

app = Flask(__name__)
VERSION = "1.3.3-beta2"

def write_config():
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
    with Popen(["git", "submodule", "foreach", "git", "reset", "--hard", ], stdout=PIPE, encoding="utf8") as proc:
        yield proc.stdout.read()
    with Popen(["git", "submodule", "foreach", "git", "pull", "origin", "master", ], stdout=PIPE, encoding="utf8") as proc:
        yield proc.stdout.read()
    yield ("#Done Update git submodules")


def sync_battle():
    args = ["python", "./splatnet2statink/splatnet2statink.py"]
    flags = os.getenv("run_flags", "-r").split(" ")
    args.extend(flags)
    yield ('#Start Run {}'.format(args))
    with Popen(args, stdout=PIPE, encoding="utf8") as proc:
        yield proc.stdout.read()
    yield ('#Done Run {}'.format(args))

def sync_salmon():
    salmon_args = ["python", "./splatnet2statink/splatnet2statink.py", "--salmon", "-r"]
    yield ('#Start Run {}'.format(salmon_args))
    with Popen(salmon_args, stdin=PIPE, stdout=PIPE, encoding="utf8") as proc:
        proc.stdin.write("50")
        proc.stdin.close()
        yield proc.stdout.read()
    yield ('#Done Run {}'.format(salmon_args))


def sync_all():
    # 時間計測
    start = time.time()
    # Docker環境変数からコンフィグを生成
    for log in write_config():
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

# ジェネレータの値をプリントしてから返す
def yield_insert_debug(func, sep="\n"):
    for log in func():
        print(log)
        yield log + sep

########## Flask Response ##########
@app.route('/')
def index():
    return 'OK'

@app.route('/sync')
def sync():
    return Response(stream_with_context(yield_insert_debug(func=sync_all)))
########## Flask Response ##########


if __name__ == "__main__":
    print("splatnet2statink-docker v{}".format(VERSION))
    run_flask = os.getenv("flask_run", "")
    run_port = os.getenv("flask_port", "8080")
    debug = os.getenv("flask_debug", "")
    if (run_flask):
        print("REST API mode. port {} listen ...".format(run_port))
        app.run(debug=debug, host="0.0.0.0", port=run_port, use_reloader=False)
    else:
        for log in sync_all():
            print(log)


