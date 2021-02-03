from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Vacancy %s>' % self.title


class VacancySchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description")
        model = Vacancy

class VacancyListResource(Resource):
    def get(self):
        vacancies = Vacancy.query.all()
        return vacancies_schema.dump(vacancies)

    def post(self):
        new_vacancy = Vacancy(
            title=request.json['title'],
            description=request.json['description']
        )
        db.session.add(new_vacancy)
        db.session.commit()
        return vacancy_schema.dump(new_vacancy)

class VacancyResource(Resource):
    def get(self, vacancy_id):
        vacancy = Vacancy.query.get_or_404(vacancy_id)
        return vacancy_schema.dump(vacancy)
    def patch(self, vacancy_id):
        vacancy = Vacancy.query.get_or_404(vacancy_id)

        if 'title' in request.json:
            vacancy.title = request.json['title']
        if 'description' in request.json:
            vacancy.description = request.json['description']

        db.session.commit()
        return vacancy_schema.dump(vacancy)

    def delete(self, vacancy_id):
        vacancy = Vacancy.query.get_or_404(vacancy_id)
        db.session.delete(vacancy)
        db.session.commit()
        return '', 204

api.add_resource(VacancyListResource, '/vacancies')
api.add_resource(VacancyResource, '/vacancies/<int:vacancy_id>')

vacancy_schema = VacancySchema()
vacancies_schema = VacancySchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)