"""
College Network Connector - core graph logic.

The college is modelled as an undirected graph stored as an adjacency list:
    friends: dict[str, set[str]]   student -> set of friends
    groups:  dict[str, set[str]]   student -> set of clubs/classes/hostels
"""

from collections import deque
import json


class StudentNotFoundError(KeyError):
    """Raised when an operation refers to a student who is not in the network."""


class CollegeNetwork:
    def __init__(self):
        self.friends = {}   # adjacency list
        self.groups = {}    # student -> set of group names

    # ------------------------------------------------------------------
    # Building the network
    # ------------------------------------------------------------------
    def add_student(self, name):
        """Add a student node (no-op if already present). O(1)"""
        name = name.strip()
        if not name:
            raise ValueError("Student name cannot be empty.")
        self.friends.setdefault(name, set())
        self.groups.setdefault(name, set())
        return name

    def add_friendship(self, a, b):
        """Add an undirected edge between two students. O(1) average."""
        a, b = self.add_student(a), self.add_student(b)
        if a == b:
            raise ValueError("A student cannot be friends with themselves.")
        self.friends[a].add(b)
        self.friends[b].add(a)

    def add_to_group(self, student, group):
        """Attach a student to a club/class/hostel. O(1) average."""
        student = self.add_student(student)
        group = group.strip()
        if not group:
            raise ValueError("Group name cannot be empty.")
        self.groups[student].add(group)

    def has_student(self, name):
        return name in self.friends

    def _require(self, *names):
        for name in names:
            if name not in self.friends:
                raise StudentNotFoundError(f"Student not found: {name}")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def list_friends(self, student):
        self._require(student)
        return sorted(self.friends[student])

    def mutual_friends(self, a, b):
        """Friends common to a and b, via set intersection. O(min(d1, d2))"""
        self._require(a, b)
        return sorted(self.friends[a] & self.friends[b])

    def common_groups(self, a, b):
        """Groups both students belong to. O(min(g1, g2))"""
        self._require(a, b)
        return sorted(self.groups[a] & self.groups[b])

    def shortest_connection(self, src, dst):
        """
        Shortest chain of people from src to dst using BFS.

        Returns a list of names [src, ..., dst] or None if not connected.
        Degrees of separation = len(path) - 1.
        O(V + E) time, O(V) space.
        """
        self._require(src, dst)
        if src == dst:
            return [src]

        queue = deque([src])
        parent = {src: None}          # doubles as the visited set

        while queue:
            current = queue.popleft()
            # sorted() keeps results deterministic across runs
            for friend in sorted(self.friends[current]):
                if friend in parent:
                    continue
                parent[friend] = current
                if friend == dst:
                    return self._rebuild_path(parent, dst)
                queue.append(friend)

        return None

    @staticmethod
    def _rebuild_path(parent, dst):
        path = []
        node = dst
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path

    def suggest_connections(self, student):
        """
        People at distance 2 (friends-of-friends who are not already friends),
        ranked by number of mutual friends (highest first).

        Returns a list of (name, mutual_count) tuples.
        """
        self._require(student)
        direct = self.friends[student]
        counts = {}

        for friend in direct:
            for candidate in self.friends[friend]:
                if candidate == student or candidate in direct:
                    continue
                counts[candidate] = counts.get(candidate, 0) + 1

        return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    def degrees_of_separation(self, a, b):
        """Number of introduction steps between a and b, or None if unconnected."""
        path = self.shortest_connection(a, b)
        return None if path is None else len(path) - 1

    # ------------------------------------------------------------------
    # Display and persistence
    # ------------------------------------------------------------------
    def display(self):
        """Lines describing every student with friends and groups. O(V + E)"""
        lines = []
        for student in sorted(self.friends):
            friends = ", ".join(sorted(self.friends[student])) or "-"
            groups = ", ".join(sorted(self.groups[student])) or "-"
            lines.append(f"{student}\n  Friends: {friends}\n  Groups:  {groups}")
        return "\n".join(lines) if lines else "The network is empty."

    def save(self, filepath):
        data = {
            "friends": {s: sorted(f) for s, f in self.friends.items()},
            "groups": {s: sorted(g) for s, g in self.groups.items()},
        }
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        network = cls()
        for student in data.get("friends", {}):
            network.add_student(student)
        for student, friend_list in data.get("friends", {}).items():
            for friend in friend_list:
                network.add_friendship(student, friend)
        for student, group_list in data.get("groups", {}).items():
            for group in group_list:
                network.add_to_group(student, group)
        return network


def sample_network():
    """The sample network from the project synopsis (Section 12)."""
    net = CollegeNetwork()
    net.add_friendship("Aman", "Riya")
    net.add_friendship("Aman", "Karan")
    net.add_friendship("Neha", "Riya")
    net.add_friendship("Neha", "Karan")
    net.add_friendship("Neha", "Dev")
    net.add_friendship("Simran", "Karan")
    net.add_student("Meera")          # present in the college, not connected
    net.add_to_group("Aman", "Coding Club")
    net.add_to_group("Aman", "Robotics Club")
    net.add_to_group("Neha", "Coding Club")
    net.add_to_group("Neha", "Robotics Club")
    return net
