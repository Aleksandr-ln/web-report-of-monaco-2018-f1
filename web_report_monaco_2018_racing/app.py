from flask import Flask, render_template, request
from .report import build_report, format_timedelta, parse_abbreviations
from .config import START_LOG, END_LOG, ABBREVIATIONS_FILE

app = Flask(__name__)

@app.route("/report")
def report():
    order = request.args.get("order", "asc")
    race_results = build_report(START_LOG, END_LOG, ABBREVIATIONS_FILE)

    positive_times = [item for item in race_results.items() if item[1].lap_time.total_seconds() > 0]
    negative_times = [item for item in race_results.items() if item[1].lap_time.total_seconds() <= 0]

    sorted_positives = sorted(
        positive_times,
        key=lambda item: item[1].lap_time.total_seconds(),
        reverse=(order == "desc")
    )

    sorted_negatives = sorted(
        negative_times,
        key=lambda item: item[1].lap_time.total_seconds(),
        reverse=(order == "desc")
    )

    top_15 = sorted_positives[:15]

    others = sorted_positives[15:] + sorted_negatives

    return render_template(
        "report.html",
        top_15=top_15,
        others=others,
        order=order,
        format_timedelta=format_timedelta
    )

@app.route("/report/drivers")
def report_drivers():
    order = request.args.get("order", "asc")
    special_wikipedia_names = {
        "Carlos Sainz": "Carlos_Sainz_Jr."
    }
    drivers = parse_abbreviations(ABBREVIATIONS_FILE)
    sorted_drivers = sorted(
        drivers.items(),
        key=lambda item: item[1].name,
        reverse=(order == "desc")
    )
    return render_template("drivers.html", drivers=sorted_drivers, order=order, special_wikipedia_names=special_wikipedia_names)

@app.route("/report/drivers/")
def driver_info():
    driver_id = request.args.get("driver_id")
    race_results = build_report(START_LOG, END_LOG, ABBREVIATIONS_FILE)
    driver_data = race_results.get(driver_id)
    if not driver_data:
        return render_template("driver_not_found.html", driver_id=driver_id), 404
    return render_template(
        "driver_info.html",
        driver=driver_data,
        format_timedelta=format_timedelta
    )
