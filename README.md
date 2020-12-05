# Attendance Script

A python script that logs onto the University of Bristol Blackboard website and logs your attendance. Can be run manually or as a cron job.

## Requirements

Check `requirements.txt` for library requirements

Install requirements:

```sh
pip3 install -r requirements.txt
```

You also need a `.env` file containing your credentials. See `.blankenv` for template or put in your own credentials and rename it as `.env`. 

In addition, you need to choose a browser to use for the script. At this time you will have to modify the source code to choose the browser. To do so, check the init function of the class in the script:

```py
def __init__(self, cls: str, pin=None):
    self.pin = pin
    self.cls = self.check_class(cls)
    self.bb_username, self.bb_password, browser = self.read_env()
    #* Choose: webdriver.Safari(), webdriver.Chrome(), webdriver.Firefox()
    self.driver = webdriver.Safari()
    self.blackboard_url = "https://www.ole.bris.ac.uk"
    logger.debug(f"CLASS: {self.cls}, PIN: {self.pin}")
```

## Available Classes

| Class                               | Code   | Remarks    |
| ----------------------------------- | ------ | ---------- |
| Computer Architecture               | "ca"   | N/A        |
| Imperative & Functional Programming | "ifp"  | pin needed |


## Usage

```sh
python3 take_attendance.py <code> <pin>
```

Examples:

1. Attend Computer Architecture

```sh
python3 take_attendance.py "ca" 
```

2. Attend IFP

```sh
python3 take_attendance.py "ifp" 8149
```