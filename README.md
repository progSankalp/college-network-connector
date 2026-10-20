# College Network Connector

A menu-driven Python application that models a college as a graph and helps students find the right person to connect with. It uses an **adjacency list**, **Breadth-First Search (BFS)**, a **queue**, and **hash-based sets/maps**.

> DSA Project (B.Tech CSE, 5th Semester, Rayat Bahra University, 2026-27)
> Submitted by: Sankalp Chaudhary (Roll No: 24011010209)

## Features

| Feature | Description | DSA used |
|---|---|---|
| Mutual friends | Friends common to two students | Set intersection |
| Shortest connection | Chain of introductions and degrees of separation | BFS + queue + parent map |
| Common groups | Clubs/classes/hostels two students share | Set intersection |
| Suggest connections | Friends-of-friends ranked by mutual friend count | Hash map counting + sorting |
| Display network | Every student with friends and groups | Adjacency list traversal |
| Save / load | Store the network as JSON | `json` module |

## How it works

- Each **student** is a node.
- Each **friendship** is an undirected edge.
- Each **group** (club, class, hostel) is a label attached to a student.

The network is stored as a dictionary that maps each student to a set of friends:

```python
friends = {
    "Aman":   {"Riya", "Karan"},
    "Neha":   {"Riya", "Karan", "Dev"},
    ...
}
```

## Requirements

- Python 3.8 or newer
- No third-party packages (uses only the standard library)

## Getting started

```bash
git clone https://github.com/<your-username>/college-network-connector.git
cd college-network-connector
python -m src.main
```

Choose option **11** to load the sample network from the synopsis, then try:

- Option **4** with `Aman` and `Neha` gives mutual friends `Karan, Riya`.
- Option **5** with `Aman` and `Dev` gives `Aman > Riya > Neha > Dev` (3 steps). The exact middle student can vary, since more than one shortest path may exist.
- Option **7** with `Aman` gives `Neha (2 mutual friends)` and `Simran (1 mutual friend)`.

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
college-network-connector/
├── src/
│   ├── __init__.py
│   ├── network.py      # Graph (adjacency list), BFS, queries, save/load
│   └── main.py         # Menu-driven console interface
├── tests/
│   ├── __init__.py
│   └── test_network.py # Unit tests (unittest)
├── .gitignore
└── README.md
```

## Complexity

Let **V** be the number of students, **E** the number of friendships, and **d** the number of friends of a student.

| Operation | Time | Space |
|---|---|---|
| Add student / friendship / group | O(1) average | O(1) |
| Shortest connection (BFS) | O(V + E) | O(V) |
| Mutual friends / common groups | O(min(d₁, d₂)) | O(d) |
| Suggest connections | O(V + E) worst case, plus sorting | O(V) |
| Display network | O(V + E) | O(1) extra |

Overall space for the network is **O(V + E)**. An adjacency matrix would need O(V²), which is far larger for a sparse college network.

## Future scope

- Graphical visualisation of the network and the highlighted path (Tkinter, matplotlib, or networkx)
- Weighted relationships (close friend, classmate, acquaintance) using Dijkstra's algorithm
- A web or mobile interface with student login
- Skill or interest tags so the system can suggest people by subject
- Persistent storage with SQLite or MySQL
- Community detection using DFS / connected components

## References

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, MIT Press
- Mark Allen Weiss, *Data Structures and Algorithm Analysis*, Pearson
- Python documentation: [collections](https://docs.python.org/3/library/collections.html)

## License

This project is for academic purposes.
