import os


def test_pages(file_name: str):
    script_dir = os.path.dirname(__file__)
    path = f"{file_name}"
    return os.path.join(script_dir, path)
