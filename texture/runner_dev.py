from texture.runner import run
import pandas as pd


def dev_run():
    """For launching server from poetry"""
    # N.B frontend dev server hard coded for localhost:8080
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "text": [
                "Hello world how are you?",
                "I'm fine how about you?",
                "The weather is great today.",
            ],
            "label": [0, 1, 0],
            "umap_x": [0.1, 0.2, 0.3],
            "umap_y": [0.4, 0.5, 0.6],
        }
    )
    run(df, load_example_data=True)


if __name__ == "__main__":
    dev_run()
