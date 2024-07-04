_url = "https://cmslesotho.limkokwing.net/campus/registry"
login = f"{_url}/login.php"


def bos_page():
    return f"{_url}/newbos.php"


def results_page():
    return f"{_url}/graderesult.php"


def transcript(student_number):
    return f"{_url}/Officialreport.php?showmaster=1&StudentID={student_number}"


def get_full_url(link: str):
    return _url + link
