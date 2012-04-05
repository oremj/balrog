from simplejson import JSONDecodeError
import simplejson as json
import sys

from flaskext.wtf import Form, TextField, Required, TextInput, NumberRange, IntegerField, HiddenInput

import logging
log = logging.getLogger(__name__)

class DisableableTextInput(TextInput):
    """A TextInput widget that supports being disabled."""
    def __init__(self, disabled, *args, **kwargs):
        self.disabled = disabled
        TextInput.__init__(self, *args, **kwargs)
    def __call__(self, *args, **kwargs):
        if self.disabled:
            kwargs['disabled'] = 'disabled'
        return TextInput.__call__(self, *args, **kwargs)

class JSONTextField(TextField):
    """TextField that parses incoming data as JSON."""
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            log.debug("JSONTextField.process_formdata: valuelist[0] is: %s", valuelist[0])
            try:
                self.data = json.loads(valuelist[0])
            except JSONDecodeError, e:
                # WTForms catches ValueError, which JSONDecodeError is a child
                # of. Because of this, we need to wrap this error in something
                # else in order for it to be properly raised.
                log.debug('JSONTextField.process_formdata: Caught JSONDecodeError')
                self.process_errors.append(e.message)
        else:
            log.debug('JSONTextField: No value list, setting self.data to %s' % self.default)
            try:
                self.data = self.default()
            except TypeError:
                self.data = self.default

class DbEditableForm(Form):
    data_version = IntegerField('data_version', widget=HiddenInput())

class PermissionForm(DbEditableForm):
    options = JSONTextField('Options')

class NewPermissionForm(PermissionForm):
    permission = TextField('Permission', validators=[Required()])

class ExistingPermissionForm(PermissionForm):
    permission = TextField('Permission', validators=[Required()], widget=DisableableTextInput(disabled=True))

class ReleaseForm(DbEditableForm):
    product = TextField('Product', validators=[Required()])
    version = TextField('Version', validators=[Required()])
    data = JSONTextField('Data', validators=[Required()])
    copyTo = JSONTextField('Copy To', default=list)
