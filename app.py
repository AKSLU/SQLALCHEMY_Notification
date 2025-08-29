from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import Flask, request, render_template, redirect, url_for
import datetime


Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    author = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///notifications.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        text = request.form['text']
        author = request.form['author']
        new_note = Notification(text=text, author=author)
        session.add(new_note)
        session.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html')

@app.route('/user')
def user():
    notifications = session.query(Notification).order_by(Notification.timestamp.desc()).all()
    return render_template('user.html', notifications=notifications)

if __name__ == '__main__':
    app.run(debug=True,port = 5001)


