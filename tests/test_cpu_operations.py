import unittest
from uvsim.constants import WORD_SIZE
from uvsim.cpu import CPU


class TestCPUOperations(unittest.TestCase):

    def setUp(self):
        # This method is called before each test to set up a CPU instance with a fresh memory state.
        self.cpu = CPU([0] * WORD_SIZE)

    def test_store_value_in_memory(self):
        # Test storing the accumulator's value in a specified memory location.
        self.cpu.accumulator = 123
        target_memory_location = 10
        self.cpu.store(target_memory_location)
        self.assertEqual(self.cpu.memory[target_memory_location], 123, "Memory location should contain the value of the accumulator.")

    def test_add_positive_numbers(self):
        # Test adding a positive number to the accumulator.
        self.cpu.accumulator = 5
        self.cpu.memory[10] = 15  # Simulate memory location 10 containing the value 15.
        self.cpu.add(10)  # Perform the add operation.
        self.assertEqual(self.cpu.accumulator, 20, "Accumulator should have the result of 5 + 15.")

    def test_subtract_positive_numbers(self):
        # Test subtracting a positive number from the accumulator.
        self.cpu.accumulator = 20
        self.cpu.memory[5] = 10  # Simulate memory location 5 containing the value 10.
        self.cpu.subtract(5)  # Perform the subtract operation.
        self.assertEqual(self.cpu.accumulator, 10, "Accumulator should have the result of 20 - 10.")

    def test_add_with_negative_result(self):
        # Test adding a number that results in a negative accumulator value.
        self.cpu.accumulator = -10
        self.cpu.memory[3] = 20  # Simulate memory location 3 containing the value 20.
        self.cpu.add(3)
        self.assertEqual(self.cpu.accumulator, 10, "Accumulator should have the result of -10 + 20.")

    def test_subtract_resulting_in_negative(self):
        # Test subtracting a number that results in a negative accumulator value.
        self.cpu.accumulator = 10
        self.cpu.memory[2] = 20  # Simulate memory location 2 containing the value 20.
        self.cpu.subtract(2)
        self.assertEqual(self.cpu.accumulator, -10, "Accumulator should have the result of 10 - 20.")

if __name__ == '__main__':
    unittest.main()
