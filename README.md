# Attendance Script

A python script that logs onto the University of Bristol Blackboard website and logs your attendance. Can be run manually or as a cron job.

## Requirements

Check `requirements.txt` for dependencies

Install dependencies:

```sh
pip3 install -r requirements.txt
```

You also need a `.env` file containing your credentials. See `.env.sample` for template.

## Available Units

| Class                               | Code          | Remarks    |
| ----------------------------------- | ------------- | ---------- |
| Computer Architecture               | "coms10015"   | N/A        |
| Imperative & Functional Programming | "coms10016"   | pin needed |


## Usage

```sh
python3 take_attendance.py --unit <code> --pin <pin>
```

Examples:

1. Attend Computer Architecture (coms10015)

```sh
python3 take_attendance.py --unit coms10015
```

2. Attend IFP

```sh
python3 take_attendance.py --unit coms10015 --pin 8768
```