import os
import json
import subprocess

def env_to_config(envs_src):
    envs = dict([(e, os.getenv(e, "")) for e in envs_src])
    envs_available = all(envs.values())
    if envs_available:
        with open('config.txt', 'w') as file:
            file.write(json.dumps(envs))
        print('#update config.txt')

if __name__ == "__main__":
    # Docker環境変数からコンフィグを生成
    envs_src = ["api_key", "cookie", "session_token", "user_lang"]
    env_to_config(envs_src)
    # submoduleで追加された
    skip_update = os.getenv("skip_update", "") # monitor per 3hour
    if not(skip_update):
        print("#update git submodules")
        subprocess.call(["git", "submodule", "foreach", "git", "reset", "--hard", ])
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "origin", "master", ])
    # 実行
    args = ["python", "./splatnet2statink/splatnet2statink.py"]
    flags = os.getenv("run_flags", "-M 14400 -r").split(" ") # monitor per 4hour
    args.extend(flags)
    print('#run {}'.format(args))
    subprocess.call(args)