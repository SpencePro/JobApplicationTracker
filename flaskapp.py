from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appstracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.String(50), nullable=False)
    interview_date = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return "<Job %r>" % self.id

# functions for adding elements to db 
@app.route("/", methods=['POST', 'GET'])
def add_company():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        date_added = str(date.today())
        interview_date = request.form['interview_date']
        
        try:
            my_entry = Jobs(company=company, position=position, date_added=date_added, interview_date=interview_date)
            db.session.add(my_entry)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding the entry"

    else:
        jobs = Jobs.query.order_by(Jobs.date_added).all()
        return render_template("index.html", jobs=jobs)


# function for deleting from db
@app.route("/delete/<int:id>")
def delete(id):
    job_to_delete = Jobs.query.get_or_404(id)

    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting the entry"


# function for updating interview date
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    job = Jobs.query.get_or_404(id)

    if request.method == 'POST':
        job.interview_date = request.form['interview_date']

        try:
            db.session.add(job)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the page"

    else:
        return render_template("update.html", job=job)


if __name__ == "__main__":
    app.run(debug=True)
