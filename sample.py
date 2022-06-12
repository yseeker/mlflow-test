# MLflow racking API よりコード部分引用
# https://www.mlflow.org/docs/latest/quickstart.html
import os
from random import random, randint
import mlflow
from mlflow import log_metric, log_param, log_artifacts
import git


def git_commits(rand):
    def func_decorator(my_func):
        repo = git.Repo("/work")
        repo.config_writer().set_value("user", "name", "yseeker").release()
        repo.config_writer().set_value(
            "user", "email", "maxwell8313@gmail.com"
        ).release()
        repo.git.add(".")
        repo.index.commit(f"{rand}_running")
        repo.git.push("origin", "HEAD:experiment")
        logger.info(f"git pushed to the remote origin")

        def decorator_wrapper(*args, **kwargs):
            my_func(*args, **kwargs)
            repo.git.add(".")
            repo.index.commit(f"{rand}_done")
            repo.git.push("origin", "HEAD:experiment")
            logger.info(f"git pushed to the remote origin")

        return decorator_wrapper

    return func_decorator

@git_commits("test")
def main():
    log_param("param1", randint(0, 100))

    # 指標を記録し、実行中に指標を更新することが可能（ MLflowに記録）
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    # アーティファクト（出力ファイル）のログ
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")
    log_artifacts("outputs") # フォルダごと記録

main()



