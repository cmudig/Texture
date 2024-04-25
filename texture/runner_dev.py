from texture.runner import run


def dev_run():
    """For launching server from poetry"""
    run({"port": 3000})
