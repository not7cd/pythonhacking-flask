import datetime


USERS = [
    dict(
        name='Patryk',
        password='admin',
        email='pat@mail.pl'
    ),
    dict(
        name='Nikodem',
        password='admin',
        email='nik@mail.pl'
    ),
    dict(
        name='Andrzej',
        password='admin',
        email='and@mail.pl'
    )
]


TASKS = [
    dict(
        user_id=1,
        description='Zakupy w biedronce.',
        date_due=(datetime.datetime.utcnow() +
                  datetime.timedelta(days=10)),
        status='OPEN'
    ),
    dict(
        user_id=2,
        description='Mycie samochodu.',
        date_due=(datetime.datetime.utcnow() +
                  datetime.timedelta(days=5)),
        status='IN PROGRESS'
    ),
    dict(
        user_id=3,
        description='Projekt na uczelni.',
        date_due=(datetime.datetime.utcnow() +
                  datetime.timedelta(days=15)),
        status='DONE'
    )
]
