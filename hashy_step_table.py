""" Hash Table ADT

Defines a Hash Table using a modified Linear Probe implementation for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Jackson Goerner'
__since__ = '07/02/2023'

from data_structures.referential_array import ArrayR
from constants import PlayerPosition, TeamStats
from typing import Generic, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')


class FullError(Exception):
    pass


class HashyStepTable(Generic[K, V]):
    """
    Hashy Step Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.

        Complexity:
        Best Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        Worst Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array: ArrayR[Union[tuple[K, V], None]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        self.sentinel = object()

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
        Best Case Complexity: O(len(key))
        Worst Case Complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
        Best Case Complexity: O(len(key)) - Complexity of calculating the hash value
        Worst Case Complexity: O(len(key)) - Complexity of calculating the hash value
        """
        return 1 + (self.hash(key) * 13 + len(key)) % (self.table_size-1)

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _hashy_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using double hashing probing.

        Args:
            key: The key for which we are searching.
            is_insert: Whether we are inserting the key (True) or searching for it (False).

        Raises:
            KeyError: When the key is not in the table, but is_insert is False.
            FullError: When a table is full and cannot be inserted.

        Complexity:
            Best Case Complexity: O(hash + hash2) - where both hash and hash2 are O(len(key)) in complexity.
                                  This occurs when the key is found on the first probe or the slot is empty.

            Worst Case Complexity: O(hash + hash2 + P * Comp(key))
                                   - P is the number of probes, which can be at most equal to the table size (N) in the worst case.
                                   - Comp(key) is the time taken to compare two keys and returning the correct position.
                                   Worst case occurs when the table is full, or the key is not found and the loop returns to the
                                   initial position, indicating that the probing has gone through all available slots.
        """
        # Initial position with primary hash function
        # Both self.hash and self.hash2 are O(len(key))
        position = self.hash(key)
        step_size = self.hash2(key)  # Get step size for probing
        initial_position = position     # Save the initial position to detect if we loop back
        
        # While loop runs until it finds a valid position (empty or matching key) or it loops back.
        # Best case complexity: O(1) - Key found or empty slot at the first probe.
        # Worst case complexity: O(P * Comp(key)) - where P is the number of probes required to loop through the table
        # and making comparisons for each loop.
        while self.array[position] is not None:
            # Check if the current position contains the key we're looking for
            if self.array[position] != self.sentinel and self.array[position][0] == key:
                return position  # Return position if the key is found

            # If key is not found, move by the step size (double hashing)
            position = (position + step_size) % self.table_size 

            # If we loop back to the starting position, table is full or key is not found
            if position == initial_position:
                if is_insert:
                    raise FullError("Table is full!")
                else:
                    raise KeyError(key)

        # If inserting and an empty slot is found, return that position
        # O(1) - Empty slot found on the first probe.
        if self.array[position] is None and is_insert:
            return position
        else:
            raise KeyError(key)

    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See hashy probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.

        Complexity:
            Best case: O(hash + hash2) - The key is found in the first probe or raises a KeyError if the position is empty.
                       Both hash and hash2 depend on the length of the key O(len(key)).

            Worst Case: O(hash + hash2 + P * Comp(key))
                            - P is the number of probes, which can be at most equal to the table size (N) in the worst case.
                            - Comp(key) is the time taken to compare two keys and returning the correct position.
                            Worst case occurs when the table is full, or the key is not found and the loop returns to the
                            initial position, indicating that the probing has gone through all available slots.

        """
        position = self._hashy_probe(key, False)
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See hashy probe.
        :raises FullError: when the table cannot be resized further.

        Complexity:
            Best case: O(hash + hash2) - The key is found or the slot is empty on the first probe.
                       Both hash and hash2 depend on the length of the key O(len(key)).

            Worst case: O((hash + hash2 + P * Comp(key)) + rehash)
                        - First, we may need to probe several positions before finding an empty slot or the correct key.
                        - Probing can take O(hash + hash2 + P * Comp(key)), where P is the number of probes.
                        - If the table exceeds the load factor threshold (2/3 full), a rehash will occur.
                        - Rehashing takes O(M + N * (hash + hash2)) in the best case, and worst O(M + N * (hash + hash2) + N^2 * Comp(key)), 
                        where N is the number of elements to be rehashed, and M is the new table size.
        """

        position = self._hashy_probe(key, True)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

        if len(self) > self.table_size * 2 / 3:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) using lazy deletion

        Complexity:
        Best Case Complexity: O(1) - If the key is found immediately to be deleted
        Worst Case Complexity: O(P) - Where P is the number of probes to find the key. 
                                    Depends on the collision and size of table. 
        """
        # Find the position of the key using probing
        # Best Case Complexity: O(1) if the key is found immediately
        # Worst Case Complexity: O(P) where P is the number of probes to find the key. 
        position = self._hashy_probe(key, False)
        
        # If the key is not found or the position holds a sentinel
        if self.array[position] is None or self.array[position] == self.sentinel:
            raise KeyError(key)

        # Perform lazy deletion by marking it with the sentinel value
        self.array[position] = self.sentinel
        self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
        Best Case Complexity: O(M + N * (hash + hash2)) - where M is the new table size and N is the number of elements in the array.
                                The hash and hash2 are complexity of len(key) they are performed to reinsert the elements into the table.
                                The best case does not encounter any collisions and no probing required.
        Worst Case Complexity: O(M + N * (hash + hash2) + N^2 * Comp(key)) - where M is the new table size and N is the number
                                of elements in the array. The worst case perceives that there will be N number of elements
                                in the old array that has to be inserted, and almost each and every element collides and
                                probe to the end of the table before inserting. This process includes Comp(key) comparison time.

        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            raise FullError("Maximum table size reached.")

        # Create a new array with the next larger size
        # O(M) - where M is the new table size
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        # Reinsert all existing elements (skip sentinels and None)
        # O(N) - where N is the number of elements to be rehash into new table.
        for item in old_array:
            if item is not None and item != self.sentinel:
                # Calls __setitem__ 
                key, value = item
                self[key] = value
        
    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N * (str(key) + str(value))) where N is the table size
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
