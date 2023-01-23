_url = "https://cmslesotho.limkokwing.net/campus/faculty"
login = f"{_url}/login.php"


def bos_page():
    return f"{_url}/newbos.php"


def get_full_url(link: str):
    return _url + link
