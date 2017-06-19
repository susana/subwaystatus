# -*- coding: utf-8 -*-

import curses
from apscheduler.schedulers.background import BackgroundScheduler

from subwaystatus.utils import get_upcoming_hour
from subwaystatus.utils import get_local_time
from subwaystatus.client import Client


def run(stdscr):
    client = Client("http://www.mta.info/service_status_json/")
    scheduler = BackgroundScheduler()
    stdscr.bkgd(' ', curses.color_pair(0))

    scheduler.add_job(
        display,
        args=[stdscr, client],
        trigger='interval',
        next_run_time=get_upcoming_hour(),
        hours=1)
    scheduler.start()
    display(stdscr, client)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            stdscr.clear()
            scheduler.shutdown()
            break
        elif c == ord('r'):
            display(stdscr, client)
        elif c == curses.KEY_RESIZE:
            stdscr.refresh()


def format_status_msg(status):
    if status == "GOOD SERVICE":
        code = "💚\tOK"
    elif status == "DELAYS":
        code = "💛\tDelays"
    elif status == "PLANNED WORK":
        code = "💖\tPlanned Work"
    elif status == "SERVICE CHANGE":
        code = "💞\tService change"
    else:
        code = "❓"
    return code


def display(stdscr, client):
    stdscr.addstr(0, 1, "{}".format("🚇  Subway Health"))
    stdscr.addstr(2, 1, "{}:".format("Last update"))
    stdscr.addstr(
        3, 1,
        get_local_time().format('YYYY-MMM-D hh:mm:ss A'))
    line_statuses = client.get_status()
    line_statuses = sorted(line_statuses, key=lambda l: l['name'])
    y = 5
    for line_status in line_statuses:
        status_msg = format_status_msg(line_status['status'])
        stdscr.addstr(y, 1, "{}\t{}".format(line_status['name'], status_msg))
        y += 1
    stdscr.refresh()


def main():
    curses.wrapper(run)
