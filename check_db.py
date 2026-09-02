from app import app, db, RoutineEntry

with app.app_context():
    entries = RoutineEntry.query.all()
    for entry in entries:
        print(entry.id, entry.sleep_hours, entry.workload_hours, entry.break_hours, entry.screen_hours, entry.eating_routine)