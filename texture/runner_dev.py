from texture.runner import run
import pandas as pd


def dev_run():
    """For launching server from poetry"""
    # N.B frontend dev server hard coded for localhost:8080
    df = pd.DataFrame(
        {
            "id": [
                100,
                200,
                300,
            ],
            "text": [
                "hello world good",
                "hello hello world",
                "maybe good",
            ],
            "topic": [
                "A",
                "B",
                "C",
            ],
            "umap_x": [0.1, 0.2, 0.3],
            "umap_y": [0.4, 0.5, 0.6],
            "vector": [
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
                [0.7, 0.8, 0.9],
            ],
            "word": [
                ["hello", "world", "good"],
                ["hello", "hello", "world"],
                ["maybe", "good"],
            ],
            "POS": [
                ["NOUN", "NOUN", "ADJ"],
                ["NOUN", "NOUN", "NOUN"],
                ["ADV", "ADJ"],
            ],
        }
    )

    run(df)


if __name__ == "__main__":
    dev_run()
