from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def save_registration(data):
    file_path = 'lunch_data.csv'
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Email', 'Lunch Choice', 'Days', 'Allergies'])

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_registrations():
    registrations_list = []
    if os.path.exists('lunch_data.csv'):
        with open('lunch_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                registrations_list.append(row)
    return registrations_list

def write_registrations(data):
    with open('lunch_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email', 'Lunch Choice', 'Days', 'Allergies'])
        writer.writerows(data)

@app.route('/')
def register():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        lunch_choice = request.form.get('lunch_choice')
        allergies = request.form.get('allergies', '')

        days = request.form.getlist('days[]')
        days_selected = ', '.join(days)

        error_messages = []

        if not name:
            error_messages.append('Name is required.')
        if not email:
            error_messages.append('Email is required.')
        if not lunch_choice:
            error_messages.append('Lunch choice is required.')
        if not days:
            error_messages.append('At least one day must be selected.')

        if error_messages:
            return render_template('index.html', errors=error_messages, name=name, email=email, lunch_choice=lunch_choice, allergies=allergies, days=request.form.getlist('days[]'))

        save_registration([name, email, lunch_choice, days_selected, allergies])

        return render_template('success.html')

@app.route('/registrations')
def registrations():
    registrations_list = read_registrations()
    return render_template('registrations.html', registrations=enumerate(registrations_list))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_registration(index):
    registrations_list = read_registrations()

    if 0 <= index < len(registrations_list):
        registrations_list.pop(index)
        write_registrations(registrations_list)
        flash('Registration deleted successfully.')
    else:
        flash('Invalid registration index.')

    return redirect(url_for('registrations'))

if __name__ == '__main__':
    app.run(debug=True)
