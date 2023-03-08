# Transpose Sandbox

This repository contains mini-projects and demos built upon the Transpose suite of APIs. All implementations are built with Python 3.11 and various Python packages.

## Getting Started

Make sure you have Python 3.11 installed. Then, install the dependencies with the following command:

```python
virtualenv --python=python3.11 env
source env/bin/activate
pip install -r requirements.txt
```

Next, add a `.env` file in the project root directory with the following config:

```ini
TRANSPOSE_API_KEY=YOUR_API_KEY_HERE
```

Finally, uncomment the demos you want to run in `run.py` and run the following command:

```python
python run.py
```
