# Formula 1 Monaco 2018 Racing Web Report

## Project Description
This project is a web application for analyzing and displaying the qualification results of the 2018 Monaco Grand Prix.
It processes log files with start and finish times of drivers, calculates their lap times, sorts results, and generates a web-based report.

## Features
- Parses log files for start (`start.log`) and end (`end.log`) times.
- Parses a file with driver abbreviations (`abbreviations.txt`).
- Calculates lap times for each driver.
- Sorts results in ascending or descending order.
- Displays results on a web page.
- API to view detailed information about a specific driver.

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files.
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```sh
cd existing_repo
git remote add origin https://github.com/Aleksandr-ln/web-report-of-monaco-2018-f1.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.foxminded.ua/foxstudent107874/task-7-web-report-of-monaco-2018-racing/-/settings/integrations)

## Installation & Usage

### 1. Clone the repository:
```sh
git clone https://github.com/Aleksandr-ln/web-report-of-monaco-2018-f1.git
cd web-report-of-monaco-2018
```

### 2. Install dependencies:
It is recommended to use a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows
```

After activation:

```sh
pip install -r requirements.txt
```

### 3. Run the Flask server:
```sh
flask --app app run
```

By default, the app will be available at:
[http://127.0.0.1:5000/report](http://127.0.0.1:5000/report)

### 4. Run tests:
```sh
pytest web_report_monaco_2018_racing/tests/
```

Or with test coverage:

```sh
coverage run -m pytest && coverage report -m
```

## 🔗 API Endpoints

| Route | Description |
|--------|-------------|
| `/report` | Main report page |
| `/report/drivers` | List of drivers |
| `/report/drivers/?driver_id=XXX` | Detailed driver information |

## Technologies Used
- **Python 3.11+**
- **Flask** – Web framework
- **Jinja2** – HTML templating engine
- **unittest / pytest / mock** – For testing
- **coverage** – Test coverage analysis

## Author
**Author:** Oleksandr Onupko  
**License:** MIT
