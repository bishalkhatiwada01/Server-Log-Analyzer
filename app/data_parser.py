import re
import csv
from multiprocessing import Pool


def parse_log_line(line):
    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.+?)\] ".+?" \d+ \d+ "(.*?)" "(.*?)"'
    match = re.search(pattern, line)
    if match:
        ip = match.group(1)
        date_time = match.group(2)
        user_agent = match.group(4)

        browser_match = re.search(r'(?:^|/)(\w+)(?:/|\s)', user_agent)
        browser = browser_match.group(1) if browser_match else 'Unknown'

        if 'Linux' in user_agent:
            os = 'Linux'
        elif 'Windows' in user_agent:
            os = 'Windows'
        elif 'Mac OS' in user_agent:
            os = 'Mac OS'
        else:
            os = 'Other'

        return ip, browser, os, date_time
    else:
        return None


def parse_log_file(filename):
    ip_list = []
    with open(filename) as f:
        pool = Pool()
        ip_list = pool.map(parse_log_line, f)
        pool.close()
        pool.join()
    return [item for item in ip_list if item is not None]


def write_to_csv(data):
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'Browser', 'Operating System', 'Date Time'])
        writer.writerows(data)


if __name__ == "__main__":
    ip_data = parse_log_file('/Users/bishalkhatiwada/Desktop/6th sem/Server Log Analyzer/access.csv')
    write_to_csv(ip_data)