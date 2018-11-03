import os
import json
import subprocess

def env_to_config(envs_src):
    envs = dict([(e, os.getenv(e, "")) for e in envs_src])
    envs_available = any(envs.values())
    if envs_available:
        print('#Start Update config.txt')
        with open('config.txt', 'w') as file:
            file.write(json.dumps(envs))
        print('#Done Update config.txt')

if __name__ == "__main__":
    # Docker環境変数からコンフィグを生成
    envs_src = ["api_key", "cookie", "session_token", "user_lang"]
    env_to_config(envs_src)
    # submoduleで追加されたsplatnet2statinkを更新
    if not(os.getenv("skip_update", "")):
        print("#Start Update git submodules")
        subprocess.call(["git", "submodule", "foreach", "git", "reset", "--hard", ])
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "origin", "master", ])
        print("#Done Update git submodules")
    # 実行
    args = ["python", "./splatnet2statink/splatnet2statink.py"]
    flags = os.getenv("run_flags", "-r").split(" ")
    args.extend(flags)
    print('#Start Run {}'.format(args))
    subprocess.call(args)
    print('#Done Run {}'.format(args))
    # Salmon runを更新する
    if not(os.getenv("skip_salmon", "")):
        salmon_args = ["python", "./splatnet2statink/splatnet2statink.py", "--salmon"]
        print('#Start Run {}'.format(salmon_args))
        p = subprocess.Popen(salmon_args, stdin=subprocess.PIPE, encoding="utf8")
        p.stdin.write("50")
        p.stdin.close()
        print('#Done Run {}'.format(salmon_args))