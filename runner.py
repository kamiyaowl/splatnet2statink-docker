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
    update_submodule = os.getenv("update_submodule", "1") # monitor per 3hour
    if update_submodule == "1":
        print("#update git submodules")
        subprocess.call("git submodule foreach git pull origin master")
    # 実行
    flags = os.getenv("run_flags", "-M 14400 -r") # monitor per 4hour
    arg = "python .\\splatnet2statink\\splatnet2statink.py {}".format(flags)
    print('#run {}'.format(arg))
    subprocess.call(arg)