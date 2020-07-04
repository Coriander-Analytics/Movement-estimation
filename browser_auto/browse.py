from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import json

# enable browser logging
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'INFO' }

script_dir = os.path.dirname(os.path.abspath(__file__))
page_path = "file:{}".format(os.path.join(script_dir, "..", "my_posenet.html"))
exec_path=os.path.join(script_dir, "drivers", "chromedriver")
print("Page Path: {}".format(page_path))
print("Exec Path: {}".format(exec_path))

browser = Chrome(executable_path=exec_path, desired_capabilities=d)

print("Fetching page...")
browser.get(page_path)

# Pretty janky. Only captures 30 times then closes
with open("poses.json", "w") as f:
    for i in range(30):
        for entry in browser.get_log('browser'):
            if entry['level'] == 'INFO' and "score" in entry['message']:
                json_str = entry['message'].split()[-1]
                #print("MESSAGE ENTRY:", entry['message'])
                #print("JSON STR:")
                #print(json_str)
                parsed = json.loads(json.loads(json_str)) # Parse twice
                f.write(json.dumps(parsed, indent=2))
        time.sleep(1)

browser.close()
