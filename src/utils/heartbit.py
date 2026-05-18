import os
import asyncio
import threading

from time import sleep


from utils.common import is_enabled
from utils.notify import notify
from utils.otel import get_otel_tracer
from utils.gauge import create_gauge, set_gauge
from utils.metrics import all_metrics, check_and_log_usage
from utils.logger import log_msg

WAIT_TIME = int(os.environ['WAIT_TIME'])
NODE_NAME = os.environ['IMALIVE_NODE_NAME']
WARNING_THRESHOLD = int(os.getenv('WARNING_THRESHOLD', 80))
ERROR_THRESHOLD = int(os.getenv('ERROR_THRESHOLD', 90))

cpu_gauge = create_gauge("cpu_all", "cpu usage in percent")
ram_total_gauge = create_gauge("ram_total", "total of ram")
ram_available_gauge = create_gauge("ram_available", "available ram")
ram_used_gauge = create_gauge("ram_used", "used ram")
ram_percent_gauge = create_gauge("ram_percent", "percent ram")
disk_free_gauge = create_gauge("disk_free", "free storage's space")
disk_used_gauge = create_gauge("disk_used", "used storage's space")
disk_percent_gauge = create_gauge("disk_percent", "percent storage's space")
disk_total_gauge = create_gauge("disk_total", "total storage's space")
swap_free_gauge = create_gauge("swap_free", "free swap")
swap_used_gauge = create_gauge("swap_used", "used swap")
swap_total_gauge = create_gauge("swap_total", "total swap")
swap_percent_gauge = create_gauge("swap_percent", "percent swap")

def cpu(payload):
    cpu_usage_percent = payload['cpu']['percent']['all']
    set_gauge(cpu_gauge, cpu_usage_percent)
    check_and_log_usage('CPU', cpu_usage_percent, WARNING_THRESHOLD, ERROR_THRESHOLD)

def ram(payload):
    memory_usage_percent = payload['virtual_memory']['percent']
    set_gauge(ram_total_gauge, payload['virtual_memory']['numeric']['total'])
    set_gauge(ram_available_gauge, payload['virtual_memory']['numeric']['available'])
    set_gauge(ram_used_gauge, payload['virtual_memory']['numeric']['used'])
    set_gauge(ram_percent_gauge, memory_usage_percent)
    check_and_log_usage('Memory', memory_usage_percent, WARNING_THRESHOLD, ERROR_THRESHOLD)

def swap(payload):
    swap_usage_percent = payload['swap_memory']['percent']
    set_gauge(swap_free_gauge, payload['swap_memory']['numeric']['free'])
    set_gauge(swap_used_gauge, payload['swap_memory']['numeric']['used'])
    set_gauge(swap_total_gauge, payload['swap_memory']['numeric']['total'])
    set_gauge(swap_percent_gauge, swap_usage_percent)
    check_and_log_usage('Swap', swap_usage_percent, WARNING_THRESHOLD, ERROR_THRESHOLD)

def disc(payload):
    disc_usage_percent = payload['disk_usage']['percent']
    set_gauge(disk_free_gauge, payload['disk_usage']['free'])
    set_gauge(disk_used_gauge, payload['disk_usage']['used'])
    set_gauge(disk_total_gauge, payload['disk_usage']['total'])
    set_gauge(disk_percent_gauge, disc_usage_percent)
    check_and_log_usage('Disk', disc_usage_percent, WARNING_THRESHOLD, ERROR_THRESHOLD)

def heartbit():
    def loop_heartbit():
        while True:
            with get_otel_tracer().start_as_current_span("imalive-heartbit"):
                payload = all_metrics()
                payload['type'] = "heartbit"
                payload['message'] = "I'm alive"

                cpu(payload)
                ram(payload)
                swap(payload)
                disc(payload)

                notify("INFO", payload)

                sleep(WAIT_TIME)

    def start_heartbit():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(loop_heartbit())

    async_thread = threading.Thread(target=start_heartbit, daemon=True)
    async_thread.start()
