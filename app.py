from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task

    id = ma.auto_field()
    title = ma.auto_field()
    completed = ma.auto_field()

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    return jsonify(tasks_schema.dump(all_tasks))

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
