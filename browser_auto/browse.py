from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import json
import signal

# Helper functions (will move to separate file)
def is_pose(entry):
    """
        Input: entry from the browser's console.log
        Output: True if it's an entry describing a pose, False otw
    """
    return entry['level'] == 'INFO' and "score" in entry['message']

def poses_json_to_csv_list(poses):
    """
        Input: JSON dictionary of poses, as retrieved from json.loads()
        Output: Corresponding CSV list

        Each pose entry in the JSON is converted to a corresponding CSV
        entry
    """
    pass

browser_is_running = True # Not familiar enough with Selenium to know how
                          # to check if a browser instance is running or not
def quit_browser(browser):
    global browser_is_running
    if browser_is_running:
        browser.quit() # Destroy all windows
        browser_is_running = False

# Paths to resources
script_dir = os.path.dirname(os.path.abspath(__file__))
page_path = "file:{}".format(os.path.join(script_dir, "..", "my_posenet.html"))
exec_path = os.path.join(script_dir, "drivers", "chromedriver")
output_path = "poses.json"

print("Chrome Browser Exececutable: {}".format(exec_path))
print("Page URL: {}".format(page_path))
print("Output File Path: {}".format(output_path))

# Setup options to enable browser logging
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'INFO' }

try:
    # Create the browser (window should pop up)
    browser = Chrome(executable_path=exec_path, desired_capabilities=d)

    # Grab the page at the specified URL
    print("Fetching page...")
    browser.get(page_path)
    print("Fetched!")

    # Main loop. Idea is to keep outputting the poses to log until
    # either Ctrl+C is pressed on the terminal or the browser window is
    # closed (though terminal program will still need to be terminated
    # in that case)
    with open(output_path, "w") as outfile:
        while (True):
            # Go through available console logs
            for entry in browser.get_log('browser'):
                if is_pose(entry):
                    #  Grab the JSON str of the pose from the last entry
                    json_str = entry['message'].split()[-1]
                    # Decode JSON str into a dictionary
                    poses = json.loads(json.loads(json_str)) # Parse twice
                    # Write to file
                    outfile.write(json.dumps(poses, indent=2))

            # Sleep to allow for more logs to accumulate
            time.sleep(1)
except KeyboardInterrupt:
    print("Signal received! Closing...")
finally:
    quit_browser(browser)
