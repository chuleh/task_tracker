# Jira Task Manager

## Overview

- So, do you suck at tracking, updating or moving your tasks in Jira because you live in the CLI? ✅
- Do you usually forget to open Jira? ✅
- Do you hate when you need to click all over Jira just to write a comment? ✅

## Prerequisites

Before you get started, ensure you have the following prerequisites:

1. **Python 3.x**: Make sure you have Python 3.x installed on your system.
2. **Pip**: You'll need the Pip package manager to install required Python packages.

## Installation

1. **Clone or Download**: Begin by cloning this repository to your local machine or downloading it as a ZIP archive.

2. **Install Dependencies**: Open your terminal and navigate to the project directory. Run the following command to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configure Jira Credentials

Create a .env file in the same directory as the script. Add your Jira credentials in the following format:

   ```bash
    JIRA_URL=YOUR_JIRA_URL
    USERNAME=YOUR_USERNAME
    API_TOKEN=YOUR_API_TOKEN
   ```

## Make the Script Executable

   ```bash
    chmod +x jira_task_manager.py
   ```

## Optional: Create Symbolic Link (macOS/Linux)
  ```bash
  ln -s /path/to/jira_task_manager.py /usr/local/bin/jira-task-manager
  ```
## Usage

Execute the script using various flags to perform different actions:

- `-m TASK_KEY COMMENT`: Add a comment to a task.
- `-n SUMMARY DESCRIPTION ISSUE_TYPE`: Create a new task on a board.
- `-l BOARD_ID`: List tasks on a board.
- `-b`: List all available boards.
- `-s BOARD_ID`: Display a simplified board view.
- `-u BOARD_ID`: Use a specific board when creating a new task.
- `-ip TASK_KEY`: Transition a task to 'In Progress' status.
- `-bk TASK_KEY`: Transition a task to 'Blocked' status.
- `-cl TASK_KEY`: Transition a task to 'Closed' status.

