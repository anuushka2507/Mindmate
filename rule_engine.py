def analyze(sleep_hours,workload_hours,break_hours,screen_hours,eating_routine,):
    flags = []

    if sleep_hours<6:
        flags.append("Low Sleep")

    if screen_hours>5:
            flags.append("High screen time")

    if workload_hours>8 and break_hours<1:
            flags.append("Not enough breaks")

    if eating_routine == "irregular":
        flags.append("Irregular eating")
    return flags

if __name__ == "__main__":
      result = analyze(
        sleep_hours=5,
        workload_hours=9,
        break_hours=0.5,
        screen_hours=6,
        eating_routine="irregular"
    )
      print(result)
    