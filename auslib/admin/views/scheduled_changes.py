from flask import jsonify, request

from auslib.admin.views.base import requirelogin, AdminView


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table, forms):
        self.namespace = namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        self.new_form, self.edit_form = forms
        super(ScheduledChangesView, self).__init__()

    def get(self):
        rows = self.sc_table.select()
        return jsonify({
            "count": len(rows),
            "scheduled_changes": rows,
        })

    @requirelogin
    def _post(self, transaction, changed_by):
        # TODO: add permission checks
        if request.form.get("data_version"):
            form = self.edit_form()
        else:
            form = self.new_form()

        sc_id = self.sc_table.insert(changed_by, transaction, **form.data)

        return jsonify({"sc_id": sc_id})
