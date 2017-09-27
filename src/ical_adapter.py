from io import BytesIO
from flask import send_file
from icalendar import Calendar, Todo
from src.models import Task
from datetime import datetime


def import_ical_to_tasks(ical):
    tasks = []
    for component in ical.walk():
        if component.name == "VTODO":
            task = Task(description=component.get('summary'),
                        date_created=component.get('dtstamp'))
            tasks.append(task)
    return tasks


def export_tasks_to_ical(tasks):
    cal = Calendar()
    cal.add('prodid', '-//Todos from flask app//hs3.pl//')
    cal.add('version', '0.1')

    for task in tasks:
        todo = Todo()
        # TODO: export all fields
        todo.add('summary', task.description)
        todo.add('dtstamp', task.date_created)
        if task.date_due:
            todo.add('due', task.date_due)
        cal.add_component(todo)

    return cal

def send_ical_file(ical):
    """Sends .ical file created from icalendar.Calendar"""
    ical_io = BytesIO()
    ical_io.write(ical.to_ical())
    ical_io.seek(0)

    filename = "%s_%s.ical" % (ical['summary'], datetime.now().isoformat(timespec='seconds'))
    return send_file(ical_io,
                     attachment_filename=filename,
                     as_attachment=True)
