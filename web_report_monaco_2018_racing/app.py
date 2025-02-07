from flask import Flask, render_template, request

from .config import ABBREVIATIONS_FILE, END_LOG, START_LOG
from .report import (
    build_report, format_timedelta, parse_abbreviations,
    sort_race_results
)

app = Flask(__name__)


@app.route("/report")
def report():
    order = request.args.get("order", "asc")
    race_results = build_report(START_LOG, END_LOG, ABBREVIATIONS_FILE)

    sorted_results = sort_race_results(race_results, order)

    return render_template(
        "report.html",
        top_15=sorted_results.positive_times[:15],
        others=sorted_results.positive_times[15:] +
        sorted_results.negative_times,
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
    return render_template(
        "drivers.html",
        drivers=sorted_drivers,
        order=order,
        special_wikipedia_names=special_wikipedia_names
    )


@app.route("/report/drivers/")
def driver_info():
    driver_id = request.args.get("driver_id")
    race_results = build_report(START_LOG, END_LOG, ABBREVIATIONS_FILE)
    driver_data = race_results.get(driver_id)
    if not driver_data:
        return render_template(
            "driver_not_found.html",
            driver_id=driver_id
        ), 404
    return render_template(
        "driver_info.html",
        driver=driver_data,
        format_timedelta=format_timedelta
    )
