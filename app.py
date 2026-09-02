from flask import Flask, render_template, request, redirect, url_for
from rule_engine import analyze, get_suggestions, get_summary, get_explanations, build_schedule
from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mindmate.db"
db = SQLAlchemy(app)

class RoutineEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sleep_hours = db.Column(db.Float)
    workload_hours = db.Column(db.Float)
    break_hours = db.Column(db.Float)
    screen_hours = db.Column(db.Float)
    eating_routine = db.Column(db.String(20))

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/age-group", methods=["GET", "POST"])
def age_group():
    if request.method == "POST":
        selected_age = request.form.get("age_group")
        return redirect(url_for("checkin"))
    return render_template("age_group.html")

@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        selected_concerns = request.form.getlist("concerns")
        details = request.form.get("details")
        other_detail = request.form.get("other_detail")
        return redirect(url_for("routine"))
    return render_template("check_in.html")

@app.route("/need-to-talk")
def need_to_talk():
    return render_template("need_to_talk.html")

@app.route("/not-safe")
def not_safe():
    return render_template("not_safe.html")

class TrustedPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))

from datetime import date, timedelta

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"))
    log_date = db.Column(db.Date)

def calculate_streak(habit_id):
    streak = 0
    check_date = date.today()

    while True:
        log = HabitLog.query.filter_by(habit_id=habit_id, log_date=check_date).first()
        if log:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return streak

def get_badge(streak):
    if streak >= 7:
        return "🏆 7-Day Consistency"
    elif streak >= 3:
        return "🔥 3-Day Streak"
    return None

@app.route("/habits", methods=["GET", "POST"])
def habits():
    if request.method == "POST":
        if "new_habit" in request.form:
            habit_name = request.form.get("new_habit")
            if habit_name:
                new_habit = Habit(name=habit_name)
                db.session.add(new_habit)
                db.session.commit()

        if "complete_habit" in request.form:
            habit_id = int(request.form.get("complete_habit"))
            existing_log = HabitLog.query.filter_by(habit_id=habit_id, log_date=date.today()).first()
            if not existing_log:
                new_log = HabitLog(habit_id=habit_id, log_date=date.today())
                db.session.add(new_log)
                db.session.commit()

    all_habits = Habit.query.all()
    habit_data = []
    for h in all_habits:
        streak = calculate_streak(h.id)
        badge = get_badge(streak)
        done_today = HabitLog.query.filter_by(habit_id=h.id, log_date=date.today()).first() is not None
        habit_data.append({"habit": h, "streak": streak, "badge": badge, "done_today": done_today})

    return render_template("habits.html", habit_data=habit_data)

@app.route("/trusted-person", methods=["GET", "POST"])
def trusted_person():
    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")

        new_person = TrustedPerson(name=name, contact=contact)
        db.session.add(new_person)
        db.session.commit()

        return render_template("trusted_person.html", person=new_person)

    person = TrustedPerson.query.first()
    return render_template("trusted_person.html", person=person)

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/dashboard")
def dashboard():
    entries = RoutineEntry.query.all()

    if entries:
        avg_sleep = round(sum(e.sleep_hours for e in entries) / len(entries), 1)
        avg_workload = round(sum(e.workload_hours for e in entries) / len(entries), 1)
        avg_screen = round(sum(e.screen_hours for e in entries) / len(entries), 1)
        total_entries = len(entries)
    else:
        avg_sleep = avg_workload = avg_screen = 0
        total_entries = 0

    return render_template("dashboard.html", avg_sleep=avg_sleep, avg_workload=avg_workload, avg_screen=avg_screen, total_entries=total_entries)

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        wake_time = request.form.get("wake_time")
        sleep_time = request.form.get("sleep_time")
        work_hours = float(request.form.get("work_hours"))
        activity_minutes = int(request.form.get("activity_minutes"))

        schedule_items = build_schedule(wake_time, sleep_time, work_hours, activity_minutes)
        return render_template("schedule_result.html", schedule_items=schedule_items)
    return render_template("schedule.html")

@app.route("/routine", methods=["GET", "POST"])
def routine():
    if request.method == "POST":
        sleep_hours = float(request.form.get("sleep_hours"))
        workload_hours = float(request.form.get("workload_hours")) 
        break_hours = float(request.form.get("break_hours"))
        screen_hours = float(request.form.get("screen_hours"))
        eating_routine = request.form.get("eating_routine")



        new_entry = RoutineEntry(
            sleep_hours=sleep_hours,
            workload_hours=workload_hours,
            break_hours=break_hours,
            screen_hours=screen_hours,
            eating_routine=eating_routine
        )
        db.session.add(new_entry)
        db.session.commit()

        flags = analyze(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine)
        suggestions = get_suggestions(flags)
        summary = get_summary(flags)
        explanations = get_explanations(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine, flags)

        return render_template("results.html", summary=summary, suggestions=suggestions, explanations=explanations)
    return render_template("routine.html")
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)