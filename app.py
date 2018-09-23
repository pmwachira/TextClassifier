from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_restful import Resource, Api
from checklanguage import identity

app=Flask(__name__)
app.config['SECRET_KEY']='SECRET_KEY'

bootstrap=Bootstrap(app)

class LanguageForm(FlaskForm):
    language=StringField('Enter a phrase', validators=[DataRequired()])
    submit=SubmitField('Submit')


@app.route('/',methods=['GET','POST'])
def index():
    phrase=None
    language=None
    form=LanguageForm()
    if form.validate_on_submit():
        phrase=form.language.data
        language=identify(form.language.data)
        form.language.data=''
    return render_template('index.html',form=form,phrase=phrase,language=language)

api=Api(app)

class TodoSimple(Resource):
    def get(self):
        return {'language':identify(request.form['data'])}

api.add_resource(TodoSimple,'/identify')


if __name__ == '__main__':
    app.run()