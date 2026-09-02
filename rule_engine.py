from datetime import datetime, timedelta

SUGGESTIONS = {
    "Low Sleep": "Try to build a more consistent sleep routine.",
    "High screen time": "Consider reducing screen time before bed.",
    "Irregular eating": "Try to keep your meal times more consistent.",
    "Not enough breaks": "Add regular short breaks between long work sessions."
}


def analyze(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine):
    flags = []

    if sleep_hours < 6:
        flags.append("Low Sleep")

    if screen_hours > 5:
        flags.append("High screen time")

    if workload_hours > 8 and break_hours < 1:
        flags.append("Not enough breaks")

    if eating_routine == "irregular":
        flags.append("Irregular eating")

    return flags


def get_suggestions(flags):
    return [SUGGESTIONS[flag] for flag in flags]


def get_summary(flags):
    if not flags:
        return "Your routine looks balanced right now."

    joined = ", ".join(flags[:-1])
    if len(flags) > 1:
        joined += " and " + flags[-1]
    else:
        joined = flags[0]

    return f"Your response suggests that {joined.lower()} may be affecting your overall balance."


def get_explanations(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine, flags):
    explanations = {}

    if "Low Sleep" in flags:
        explanations["Low Sleep"] = f"Sleep was {sleep_hours} hours, below the recommended 6-hour minimum."

    if "High screen time" in flags:
        explanations["High screen time"] = f"Screen time was {screen_hours} hours, above the 5-hour guideline."

    if "Not enough breaks" in flags:
        explanations["Not enough breaks"] = f"Workload was {workload_hours} hours with only {break_hours} hour(s) of breaks."

    if "Irregular eating" in flags:
        explanations["Irregular eating"] = "Eating routine was marked as irregular."

    return explanations

def build_schedule(wake_time, sleep_time, work_hours, activity_minutes):
    schedule = []

    wake = datetime.strptime(wake_time, "%H:%M")
    schedule.append((wake.strftime("%H:%M"), "Wake up"))

    current = wake + timedelta(minutes=30)
    schedule.append((current.strftime("%H:%M"), "Breakfast"))

    current += timedelta(minutes=30)
    work_block_1 = work_hours / 2
    schedule.append((current.strftime("%H:%M"), f"Work/study block ({work_block_1}h)"))

    current += timedelta(hours=work_block_1)
    schedule.append((current.strftime("%H:%M"), "Break"))
    
    current += timedelta(minutes=30)
    schedule.append((current.strftime("%H:%M"), f"Work/study block ({work_block_1}h)"))

    current += timedelta(hours=work_block_1)
    schedule.append((current.strftime("%H:%M"), f"Physical activity ({activity_minutes} min)"))

    current += timedelta(minutes=activity_minutes)
    schedule.append((current.strftime("%H:%M"), "Dinner"))

    current += timedelta(hours=1)
    schedule.append((current.strftime("%H:%M"), "Relax / wind down"))

    schedule.append((sleep_time, "Sleep"))

    return schedule

if __name__ == "__main__":
    sleep_hours = 5
    workload_hours = 6
    break_hours = 2
    screen_hours = 3
    eating_routine = "irregular"

    flags = analyze(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine)
    suggestions = get_suggestions(flags)
    summary = get_summary(flags)
    explanations = get_explanations(sleep_hours, workload_hours, break_hours, screen_hours, eating_routine, flags)

    print("Flags:", flags)
    print("Suggestions:", suggestions)
    print("Summary:", summary)
    print("Explanations:", explanations)



