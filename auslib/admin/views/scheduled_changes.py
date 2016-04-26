from flask import jsonify

from auslib.admin.views.base import AdminView


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        super(AdminView, self).__init__()

    def get(self):
        rows = self.sc_table.select()
        return jsonify({
            "count": len(rows),
            "scheduled_changes": rows,
        })
