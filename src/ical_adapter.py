from icalendar import Calendar, Todo
from datetime import datetime
from src.models import Task


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
        todo.add('summary', task.description)
        todo.add('dtstamp', task.date_created)
        todo.add('due', task.date_due)
        cal.add_component(todo)

    return cal
