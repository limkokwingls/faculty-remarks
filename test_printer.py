import pdfkit


pdfkit.from_string("""
    <html>
        <h1>Hello World</h1>
        <p>This is a hello world page</p>
    </html>

""", 'file_to_print.pdf')
