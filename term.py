from datetime import datetime


def get_term():
    now = datetime.now()

    if now.month < 7:
        term = f"{now.year - 1}-08"
    else:
        term = f"{now.year}-02"
    return term


if __name__ == '__main__':
    print(get_term())
