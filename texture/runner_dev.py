from texture.runner import run


def dev_run():
    """For launching server from poetry"""
    # N.B frontend dev server hard coded for localhost:8080
    run({})


if __name__ == "__main__":
    dev_run()
