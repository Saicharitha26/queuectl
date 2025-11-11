 QueueCTL – Job Queue Management CLI

QueueCTL is a simple command-line tool to manage background jobs with retry handling and a dead-letter queue.

 Features
- Add, list, and remove jobs
- Persistent job storage (`jobs.json`)
- Dead Letter Queue support (`dlq.json`)
- Configurable retries and delays
- CLI built using `click` and output using `rich`
  
Installation

```bash
# Clone the repository
git clone https://github.com/<saicharitha26>/queuectl.git
cd queuectl

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Usage

Run the CLI:

python -m queuectl.cli add "Backup Database"
python -m queuectl.cli list
python -m queuectl.cli run

 Project Structure
queuectl/
├── queuectl/
│   ├── cli.py
│   ├── job_manager.py
│   ├── worker.py
│   ├── config.py
│   ├── storage.py
│   ├── dlq_manager.py
│   └── utils.py
├── jobs.json
├── dlq.json
├── config.json
├── requirements.txt
└── README.md

MIT License © 2025 kumavath saicharitha
