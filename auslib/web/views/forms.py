from flaskext.wtf import Form, TextField, Required

class PermissionForm(Form):
    permission = TextField('permission', validators=[Required()])
