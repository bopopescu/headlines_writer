from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required


class WordForm(Form):
    
    input_word = TextField('word', validators = [Required()])
