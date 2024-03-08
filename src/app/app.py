from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

def convert_outlook_to_titan(input_file):
    output_rows = []
    with open(input_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titan_row = {
                'Email': row.get('E-mail Address', ''),
                'Full Name': row.get('Nombre', ''),
                'First Name': row.get('Nombre', '').split(' ')[0],
                'Last Name': row.get('Apellidos', ''),
                'Phone Number 1': row.get('Teléfono principal', ''),
                'Phone Number 2': row.get('Teléfono del trabajo', ''),
                'Url': '',
                'Address': row.get('Calle del trabajo', ''),
                'Notes': row.get('Notes', ''),
                'Birthday': row.get('Birthday', ''),
                'Designation': row.get('Puesto', ''),
                'Department': row.get('Department', ''),
                'Company': row.get('Organización', '')
            }
            output_rows.append(titan_row)
    return output_rows

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            input_file = file.filename
            output_rows = convert_outlook_to_titan(input_file)
            output_file = 'titan_mail.csv'
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Email', 'Full Name', 'First Name', 'Last Name', 'Phone Number 1', 'Phone Number 2',
                              'Url', 'Address', 'Notes', 'Birthday', 'Designation', 'Department', 'Company']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)
            return redirect(url_for('upload_file'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
