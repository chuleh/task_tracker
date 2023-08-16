from jira import JIRA
from dotenv import load_dotenv
import os
import argparse

# Load environment variables from .env file
load_dotenv()

# Read Jira credentials from environment variables
JIRA_URL = os.getenv("JIRA_URL")
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

# Initialize Jira connection using API token
jira = JIRA(server=JIRA_URL, basic_auth=(USERNAME, API_TOKEN))

# Get all boards
def get_all_boards():
    boards = jira.boards()
    return boards

# Get tasks on a board
def get_tasks_on_board(board_id):
    issues = jira.search_issues(f"project={board_id}")
    return issues

# Write a comment on a task
def write_comment_on_task(task_key, comment):
    issue = jira.issue(task_key)
    issue.update(comment={"body": comment})

# Create a new task on a board
def create_task_on_board(board_id, summary, description, issue_type):
    issue_dict = {
        "project": {"id": board_id},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue.key

# Transition a task to a new status
def transition_task(task_key, transition_name):
    transitions = jira.transitions(task_key)
    for transition in transitions:
        if transition_name.lower() in transition["name"].lower():
            jira.transition_issue(task_key, transition["id"])
            return True
    return False

# Display a simplified board representation
def display_board(board_id):
    tasks = get_tasks_on_board(board_id)
    print("Board Tasks:")
    for task in tasks:
        assignee = task.fields.assignee.displayName if task.fields.assignee else "Unassigned"
        print(f"Task: {task.key}, Assignee: {assignee}, Summary: {task.fields.summary}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jira Task Manager")
    parser.add_argument("-m", "--comment", nargs=2, metavar=("TASK_KEY", "COMMENT"), help="Write a comment on a task")
    parser.add_argument("-n", "--newtask", nargs=3, metavar=("SUMMARY", "DESCRIPTION", "ISSUE_TYPE"), help="Create a new task on a board")
    parser.add_argument("-l", "--listtasks", metavar="BOARD_ID", help="List tasks on a board")
    parser.add_argument("-b", "--listboards", action="store_true", help="List all boards")
    parser.add_argument("-s", "--showboard", metavar="BOARD_ID", help="Display a simplified board")
    parser.add_argument("-u", "--useboard", metavar="BOARD_ID", help="Use a specific board when creating a new task")
    parser.add_argument("-ip", "--inprogress", metavar=("TASK_KEY"), help="Move a task to 'In Progress' status")
    parser.add_argument("-bk", "--blocked", metavar=("TASK_KEY"), help="Move a task to 'Blocked' status")
    parser.add_argument("-cl", "--closed", metavar=("TASK_KEY"), help="Move a task to 'Closed' status")
    args = parser.parse_args()

    try:
        if args.comment:
            task_key, comment = args.comment
            write_comment_on_task(task_key, comment)
            print("Comment added to task:", task_key)

        elif args.newtask:
            if args.useboard:
                board_id = args.useboard
            else:
                boards = get_all_boards()
                print("Available boards:")
                for board in boards:
                    print(f"Board ID: {board.id}, Board Name: {board.name}")
                board_id = input("Enter the ID of the board to use for the new task: ")

            summary, description, issue_type = args.newtask
            new_task_key = create_task_on_board(board_id, summary, description, issue_type)
            print("New task created:", new_task_key)

        elif args.listtasks:
            board_id = args.listtasks
            tasks = get_tasks_on_board(board_id)
            for task in tasks:
                print(f"Task Key: {task.key}, Summary: {task.fields.summary}")

        elif args.listboards:
            boards = get_all_boards()
            for board in boards:
                print(f"Board ID: {board.id}, Board Name: {board.name}")

        elif args.showboard:
            board_id = args.showboard
            display_board(board_id)

        elif args.inprogress:
            task_key = args.inprogress
            if transition_task(task_key, "In Progress"):
                print("Task moved to 'In Progress' status:", task_key)
            else:
                print("Transition to 'In Progress' status failed for task:", task_key)

        elif args.blocked:
            task_key = args.blocked
            if transition_task(task_key, "Blocked"):
                print("Task moved to 'Blocked' status:", task_key)
            else:
                print("Transition to 'Blocked' status failed for task:", task_key)

        elif args.closed:
            task_key = args.closed
            if transition_task(task_key, "Closed"):
                print("Task moved to 'Closed' status:", task_key)
            else:
                print("Transition to 'Closed' status failed for task:", task_key)

        else:
            print("No action specified. Use -h for help.")

    except Exception as e:
        print("An error occurred:", str(e))

