"""
Menu-driven console interface for the College Network Connector.

Run from the project root:
    python -m src.main
"""

import os
import sys

from src.network import CollegeNetwork, StudentNotFoundError, sample_network

DATA_FILE = "network_data.json"

MENU = """
========== College Network Connector ==========
 1. Add student
 2. Add friendship
 3. Add student to group
 4. Mutual friends
 5. Shortest connection (BFS)
 6. Common groups
 7. Suggest connections
 8. Display network
 9. Save network
10. Load network
11. Load sample network
 0. Exit
==============================================
"""


def ask(prompt):
    return input(prompt).strip()


def ask_student(network, prompt):
    """Ask for a student name until it exists in the network."""
    while True:
        name = ask(prompt)
        if network.has_student(name):
            return name
        print(f"  '{name}' is not in the network. Add them first (option 1).")


def handle_add_student(net):
    name = ask("Student name: ")
    try:
        net.add_student(name)
        print(f"  Added {name.strip()}.")
    except ValueError as exc:
        print(f"  Error: {exc}")


def handle_add_friendship(net):
    a = ask("First student: ")
    b = ask("Second student: ")
    try:
        net.add_friendship(a, b)
        print(f"  {a} and {b} are now friends.")
    except ValueError as exc:
        print(f"  Error: {exc}")


def handle_add_group(net):
    name = ask("Student name: ")
    group = ask("Group name: ")
    try:
        net.add_to_group(name, group)
        print(f"  {name} added to {group}.")
    except ValueError as exc:
        print(f"  Error: {exc}")


def handle_mutual(net):
    a = ask_student(net, "First student: ")
    b = ask_student(net, "Second student: ")
    result = net.mutual_friends(a, b)
    print("  Mutual friends: " + (", ".join(result) if result else "None"))


def handle_shortest(net):
    a = ask_student(net, "From: ")
    b = ask_student(net, "To: ")
    path = net.shortest_connection(a, b)
    if path is None:
        print("  No connection found.")
    else:
        steps = len(path) - 1
        print("  " + " > ".join(path))
        print(f"  ({steps} step{'s' if steps != 1 else ''})")


def handle_common_groups(net):
    a = ask_student(net, "First student: ")
    b = ask_student(net, "Second student: ")
    result = net.common_groups(a, b)
    print("  Common groups: " + (", ".join(result) if result else "None"))


def handle_suggest(net):
    student = ask_student(net, "Student: ")
    suggestions = net.suggest_connections(student)
    if not suggestions:
        print("  No suggestions available.")
        return
    for rank, (name, count) in enumerate(suggestions, start=1):
        word = "mutual friend" if count == 1 else "mutual friends"
        print(f"  {rank}. {name} ({count} {word})")


def handle_save(net):
    net.save(DATA_FILE)
    print(f"  Network saved to {DATA_FILE}.")


def handle_load(net):
    if not os.path.exists(DATA_FILE):
        print(f"  No saved file found ({DATA_FILE}).")
        return net
    print(f"  Network loaded from {DATA_FILE}.")
    return CollegeNetwork.load(DATA_FILE)


def main():
    net = CollegeNetwork()
    actions = {
        "1": handle_add_student,
        "2": handle_add_friendship,
        "3": handle_add_group,
        "4": handle_mutual,
        "5": handle_shortest,
        "6": handle_common_groups,
        "7": handle_suggest,
        "8": lambda n: print(n.display()),
        "9": handle_save,
    }

    while True:
        print(MENU)
        choice = ask("Choose an option: ")

        if choice == "0":
            print("Goodbye!")
            break
        if choice == "10":
            net = handle_load(net)
        elif choice == "11":
            net = sample_network()
            print("  Sample network loaded (from the project synopsis).")
        elif choice in actions:
            try:
                actions[choice](net)
            except StudentNotFoundError as exc:
                print(f"  Error: {exc}")
        else:
            print("  Invalid option, please try again.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        sys.exit(0)
