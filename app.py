from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission here
        # You can save the form data to a database, send an email, etc.
        return redirect('/')
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
