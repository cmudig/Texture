from texture.runner import run


def dev_run():
    """For launching server from poetry"""
    run({"port": 8080})  # N.B frontend dev server hard coded for localhost:8080


if __name__ == "__main__":
    dev_run()
