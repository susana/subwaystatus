# -*- coding: utf-8 -*-

import logging

import curses
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_MISSED

from subwaystatus.utils import get_upcoming_hour
from subwaystatus.utils import get_local_time
from subwaystatus.client import Client


def handle_missed_job(event):
    pass

def run(stdscr):
    logging.getLogger('apscheduler.executors').setLevel(logging.ERROR)
    client = Client("http://www.mta.info/service_status_json/")
    scheduler = BackgroundScheduler()
    stdscr.bkgd(' ', curses.color_pair(0))
    scheduler.add_listener(handle_missed_job, EVENT_JOB_MISSED)
    scheduler.add_job(
        display,
        args=[stdscr, client],
        trigger='interval',
        next_run_time=get_upcoming_hour(),
        hours=1,
        coalesce=True)
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


def get_message(status):
    msg = []
    if status == "GOOD SERVICE":
        msg.extend(["💚", "OK"])
    elif status == "DELAYS":
        msg.extend(["💛", "Delays"])
    elif status == "PLANNED WORK":
        msg.extend(["💖", "Planned Work"])
    elif status == "SERVICE CHANGE":
        msg.extend(["💞", "Service change"])
    else:
        msg.extend(["❓", "Unknown status"])
    return msg


def display(stdscr, client):
    stdscr.addstr(0, 1, "{}".format("🚇  Subway Health"))
    stdscr.addstr(2, 1, "{}:".format("Last update"))
    stdscr.addstr(
        3, 1,
        get_local_time().format('YYYY-MMM-D hh:mm:ss A'))
    line_statuses = client.get_status()
    line_statuses = sorted(line_statuses, key=lambda l: l['line'])
    y = 5
    for line_status in line_statuses:
        symbol, msg = get_message(line_status['status'])
        line = stdscr.addstr(y, 1, line_status['line'], curses.A_BOLD)
        stdscr.addstr(y, 8, symbol)
        stdscr.addstr(y, 11, msg)
        y += 1
    stdscr.refresh()


def main():
    curses.wrapper(run)
