# Attendance Script

A python script that logs onto the University of Bristol Blackboard website and logs your attendance. Can be run manually or as a cron job.

## Requirements

Check `requirements.txt` for library requirements

Install requirements:

```sh
pip3 install -r requirements.txt
```

You also need a `.env` file containing your credentials. See `.env.sample` for template.

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

```shs
python3 take_attendance.py "ifp" 8149
```