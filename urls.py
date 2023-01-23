_url = "https://cmslesotho.limkokwing.net/campus/registry/"
login = f"{_url}/login.php"
faculty_programs = f"{_url}/f_programlist.php?showmaster=1&SchoolID=8"


def get_full_url(link: str):
    return _url + link


def program_students(school_id, program_id, semester, term, pageNumber):

    return f"{_url}/r_studentviewlist.php?x_InstitutionID=1&z_InstitutionID=%3D%2C%2C&x_SchoolID={school_id}&z_SchoolID=%3D%2C%2C&x_ProgramID={program_id}&z_ProgramID=%3D%2C%2C&x_CurrentSemester={semester}&z_CurrentSemester=LIKE%2C%27%25%2C%25%27&x_LatestTerm={term}&z_LatestTerm=LIKE%2C%27%25%2C%25%27&start={pageNumber}"


def faculties():
    return f"{_url}/f_schoollist.php?cmd=resetall"


def transcript(student_number):
    return f"{_url}/Officialreport.php?showmaster=1&StudentID={student_number}"
