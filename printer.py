import pdfkit
import subprocess


def print_text(text: str):
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")
    pdfkit.from_string(text, 'file_to_print.pdf', configuration=config)

    command = "{} {}".format('PDFtoPrinter.exe', 'file_to_print.pdf')

    subprocess.call(command, shell=True)


def test_printer():
    print_text("Hello World")


if __name__ == "__main__":
    test_printer()
