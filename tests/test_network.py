import os
import tempfile
import unittest

from src.network import CollegeNetwork, StudentNotFoundError, sample_network


class TestBuilding(unittest.TestCase):
    def test_add_friendship_is_undirected(self):
        net = CollegeNetwork()
        net.add_friendship("A", "B")
        self.assertIn("B", net.friends["A"])
        self.assertIn("A", net.friends["B"])

    def test_cannot_befriend_self(self):
        net = CollegeNetwork()
        with self.assertRaises(ValueError):
            net.add_friendship("A", "A")

    def test_empty_name_rejected(self):
        net = CollegeNetwork()
        with self.assertRaises(ValueError):
            net.add_student("   ")

    def test_duplicate_friendship_is_harmless(self):
        net = CollegeNetwork()
        net.add_friendship("A", "B")
        net.add_friendship("B", "A")
        self.assertEqual(net.list_friends("A"), ["B"])


class TestMutualAndGroups(unittest.TestCase):
    def setUp(self):
        self.net = sample_network()

    def test_mutual_friends(self):
        self.assertEqual(self.net.mutual_friends("Aman", "Neha"), ["Karan", "Riya"])

    def test_no_mutual_friends(self):
        self.assertEqual(self.net.mutual_friends("Aman", "Meera"), [])

    def test_common_groups(self):
        self.assertEqual(
            self.net.common_groups("Aman", "Neha"),
            ["Coding Club", "Robotics Club"],
        )

    def test_unknown_student_raises(self):
        with self.assertRaises(StudentNotFoundError):
            self.net.mutual_friends("Aman", "Ghost")


class TestShortestConnection(unittest.TestCase):
    def setUp(self):
        self.net = sample_network()

    def test_three_steps_from_aman_to_dev(self):
        path = self.net.shortest_connection("Aman", "Dev")
        self.assertEqual(len(path) - 1, 3)
        self.assertEqual(path[0], "Aman")
        self.assertEqual(path[-1], "Dev")

    def test_path_uses_only_real_friendships(self):
        path = self.net.shortest_connection("Aman", "Dev")
        for a, b in zip(path, path[1:]):
            self.assertIn(b, self.net.friends[a])

    def test_not_connected_returns_none(self):
        self.assertIsNone(self.net.shortest_connection("Aman", "Meera"))
        self.assertIsNone(self.net.degrees_of_separation("Aman", "Meera"))

    def test_same_student_is_zero_steps(self):
        self.assertEqual(self.net.shortest_connection("Aman", "Aman"), ["Aman"])

    def test_bfs_finds_shortest_not_longest(self):
        # Direct link A-D plus a longer chain A-B-C-D: BFS must pick A-D.
        net = CollegeNetwork()
        net.add_friendship("A", "B")
        net.add_friendship("B", "C")
        net.add_friendship("C", "D")
        net.add_friendship("A", "D")
        self.assertEqual(net.shortest_connection("A", "D"), ["A", "D"])


class TestSuggestions(unittest.TestCase):
    def test_sample_suggestions_match_synopsis(self):
        net = sample_network()
        self.assertEqual(
            net.suggest_connections("Aman"),
            [("Neha", 2), ("Simran", 1)],
        )

    def test_direct_friends_are_not_suggested(self):
        net = sample_network()
        names = [name for name, _ in net.suggest_connections("Aman")]
        self.assertNotIn("Riya", names)
        self.assertNotIn("Karan", names)
        self.assertNotIn("Aman", names)


class TestPersistence(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        net = sample_network()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "net.json")
            net.save(path)
            loaded = CollegeNetwork.load(path)
        self.assertEqual(loaded.friends, net.friends)
        self.assertEqual(loaded.groups, net.groups)


if __name__ == "__main__":
    unittest.main()
