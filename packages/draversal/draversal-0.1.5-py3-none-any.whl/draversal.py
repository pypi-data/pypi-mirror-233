from contextlib import contextmanager

class DictTraversal(dict):
    """
    Depth-first traverse Python dictionary with a uniform children (and label) field structure.

    Class initialization takes a dictionary data argument and a mandatory children field which must
    correspond to the dictionary children list field. Optionally data can be provided as keyword arguments.

    Except from child field, all other fields are optional and the rest of the dictionary can be formed freely.

    Example:
        ```python
        children_field = "sections"
        data = {
            'title': 'root',
            children_field: [
                {'title': 'Child 1'},
                {'title': 'Child 2', children_field: [
                    {'title': 'Grandchild 1'},
                    {'title': 'Grandchild 2', children_field: [
                        {'title': 'Grandgrandchild'}
                    ]}
                ]},
                {'title': 'Child 3'}
            ]
        }
        traversal = DictTraversal(data, children_field=children_field)
        ```

    After initialization, a certain methods are available for traversing and modifying the nested tree structure.

    Example:
        ```python
        (
            # iter brings to the root, from which the traversal starts, but actually the first items has not been reached yet
            str(iter(traversal)),  # {'title': 'root'}
            # next forwards iterator to the first/next item.
            # it yields StopIteration error when the end of the tree has been reached
            str(next(traversal)),  # {'title': 'Child 1'}
            # prev works similar way and it yields StopIteration error when the beginning of the tree has been reached
            str(prev(next(next(traversal)))),  # {'title': 'Child 2'}
            # first function brings to the first item in the list (after root)
            str(first(traversal)),  # {'title': 'Child 1'}
            # last function brings to the last item in the list
            str(last(traversal)),  # {'title': 'Child 3'}
            # root function brings to the root, from which the traversal starts.
            # next will be first item contra to iter which will give root as a first item only after callind next
            str(root(traversal))  # {'title': 'root'}
        )
        ```

    Root is a special place in a tree. When `DictTraversal` has been initialized, or `iter`/`root` functions are called,
    root is a starting point of the tree, which contains the first siblings. To traverse to the first sibling,
    either next, first, or move_to_next_item methods must be called.
    """

    def __init__(self, *args, children_field=None, **kwargs):
        """
        Initializes the `DictTraversal` object.

        Behavior:
            - Initializes the underlying dictionary with the given `*args` and `**kwargs`.
            - Sets the `children_field` attribute for identifying child nodes in the dictionary.
            - Initializes `path` as an empty list to keep track of the traversal path.
            - Sets `current` to point to the root node (`self`).
            - Sets `iter_method` to use `move_to_next_item` by default for iteration.
            - Initializes `inverted_context` as False.

        Parameters:
            *args: Variable-length argument list to initialize the dictionary.
            children_field (str): The key used to identify children in the dictionary.
            **kwargs: Arbitrary keyword arguments to initialize the dictionary.

        Raises:
            ValueError: If `children_field` is not provided or is not a string.

        Attributes:
            children_field (str): The key used to identify children in the dictionary.
            path (list): Keeps track of the traversal path.
            current (dict): Points to the current node in the traversal.
            iter_method (func): Function used for moving to the next/previous item during iteration.
            next_iteration_start (bool): Flag used to control the behavior of `__iter__()`/`__next__()`.
            prev_iteration_stop  (bool): Flag used to control the behavior of `__iter__()`/`prev()`.
            inverted_context (bool): Flag to indicate whether the iteration context ie. direction manipulated by `with` is inverted or not.

        Note:
            - Keyword arguments will override arguments in `*args` if overlapping keys are found.
        """
        super(DictTraversal, self).__init__(*args, **kwargs)
        if not children_field or not isinstance(children_field, str):
            raise ValueError("Childred field must be given and it must be a string")
        self.children_field = children_field
        # Path must always be absolute
        self.path = []
        self.current = self
        self.inverted_context = False
        # Default iteration method
        self.iter_method = self.move_to_next_item
        self.next_iteration_start = True
        self.prev_iteration_stop = False

    def __neg__(self):
        """
        Moves the traversal to the previous item.

        Behavior:
            - Can be invoked using the `-` unary operator.
            - Updates the `path` and `current` attributes to reflect the new traversal path.

        Returns:
            self: Returns the `DictTraversal` object itself, pointing to the previous node.

        Example:
            ```python
            print(last(traversal)["title])  # Outputs: "Child 3"
            print((-traversal)["title])  # Outputs: "Grandgrandchild"
            ```
        """
        self.move_to_prev_item()
        return self

    def __pos__(self):
        """
        Moves the traversal to the next item.

        Behavior:
            - Can be invoked using the `+` unary operator.
            - Updates the `path` and `current` attributes to reflect the new traversal path.

        Returns:
            self: Returns the `DictTraversal` object itself, pointing to the next node.

        Example:
            ```python
            print(root(traversal)["title])  # Outputs: "root"
            print((+traversal)["title])  # Outputs: "Child 1"
            ```
        """
        self.move_to_next_item()
        return self

    def __iter__(self):
        """
        Initializes the iterator for the `DictTraversal` object.

        Returns:
            self: Returns the `DictTraversal` object itself to make it an iterator.

        Attributes:
            path (list): Reset to an empty list.
            current (dict): Reset to point to the root node.

        Behavior:
            - Initializes the iterator for the `DictTraversal` object.
            - Resets the traversal to the root node.
            - Returns the `DictTraversal` object itself to make it an iterator.

        Note:
            - This method resets the traversal to the root node.

        Example:
            ```python
            # Using __iter__ to reset traversal to root, but next-function is actually required to move to the root!
            iter(traversal)  # Represents: {'title': 'root'}
            ```
        """
        self.next_iteration_start = False
        # For prev
        self.prev_iteration_stop = False
        self.current, self.path = self, []
        return self

    def __next__(self):
        """
        Advances the iterator to the next item in the traversal.

        Returns:
            self: Returns the `DictTraversal` object itself, pointing to the next node.

        Raises:
            StopIteration: If there are no more items to traverse.

        Attributes:
            path (list): Updated to reflect the new traversal path.
            current (dict): Updated to point to the next node in the traversal.

        Behavior:
            - Advances the iterator to the next item in the traversal.
            - Updates the path and current attributes to reflect the new traversal path.
            - Raises StopIteration if there are no more items to traverse.

        Note:
            - This method moves the traversal to the next node relative to the current node.
            - Unlike `move_to_next_item` and `move_to_prev_item`, which jump over the root and continue from start/end,
                `prev` will raise a StopIteration error when it reaches the end of the traversal.

        Example:
            ```python
            # Using __next__ to move to the next item
            try:
                iter(traversal)
                next(traversal)  # Represents: {'title': 'root'}
                next(traversal)  # Represents: {'title': 'Child 1'}
            except StopIteration:
                print("No more items to traverse.")
            ```
        """
        # Move current pointer in the second round
        if self.next_iteration_start:
            self.iter_method()
            if self.inverted_context:
                if self.prev_iteration_stop:
                    raise StopIteration
                if not self.path:
                    self.prev_iteration_stop = True
            else:
                if not self.path:
                    raise StopIteration
        # Start moving next time
        else:
            if self.inverted_context:
                # For prev, we need to move once
                self.iter_method()
            self.next_iteration_start = True
        return self


    class BackwardIterator:
        """
        An iterator class for backward traversal of the dictionary.

        Behavior:
            - Initializes with a `DictTraversal` object.
            - Sets the last item as the current item for traversal.
            - Moves to the previous item on each call to `__next__`.

        Attributes:
            traversal (DictTraversal): The `DictTraversal` object to iterate over.
        """

        def __init__(self, traversal):
            """
            Initializes the `BackwardIterator` object.

            Parameters:
                traversal (DictTraversal): The `DictTraversal` object to iterate over.
            """
            self.traversal = traversal

        def __iter__(self):
            """
            Initializes the iterator and sets the last item as the current item.
            """
            self.iteration_stop = False
            return self

        def __next__(self):
            """
            Moves to the previous item and returns it.

            Raises:
                StopIteration: If there are no more items to traverse.
            """
            if self.traversal.inverted_context:
                # Must be moved next before stop
                self.traversal.move_to_next_item()
                # Both stop flag must be on and path must be empty
                if not self.traversal.path and self.iteration_stop:
                    raise StopIteration
                # After first iteration stop flag has been activated
                self.iteration_stop = True
                return self.traversal
            else:
                # Must be stopped before prev
                if self.iteration_stop:
                    raise StopIteration
                self.traversal.move_to_prev_item()
                # Flag stop to raise StopIteration at next time
                if not self.traversal.path:
                    self.iteration_stop = True
                return self.traversal

        def __invert__(self):
            """
            Returns the forward iterator of the `DictTraversal` object.
            """
            return self.traversal.__iter__()


    def __invert__(self):
        """
        Returns a BackwardIterator object for backward traversal.

        Behavior:
            - Can be invoked using the `~` unary operator.
            - Due to `BackwardIterator.__invert__` it is possible to chain operators,
                while the practical usage is questionable in that case.

        Example:
            ```python
            # Forward traversal (internally for calls iter first and then next until StopIteration has been raised)
            # Note: in list comprehension [item for item in traversal] item will return the root, not item title!
            for item in traversal:
                print(item)

            # Backward traversal using the `~` unary operator
            for item in ~traversal:
                print(item)

            # Forward traversal again using double `~~` unary operator.
            # This is same as without operator at all.
            for item in ~~traversal:
                print(item)
            ```
        """
        return self.BackwardIterator(self)
        if self.inverted_context:
            return self.__iter__()
        else:
            return self.BackwardIterator(self)

    @contextmanager
    def inverted(self):
        """
        Context manager for backward traversal.

        Behavior:
            - Temporarily sets `iter_method` to `move_to_prev_item`.
            - Restores the original `iter_method` after exiting the context.
            - Affects the behavior of the following methods:
                - next, prev
                - peek_next, peek_prev
                - for loop iteration
                - first, last
                - root, move_to_next_item, and move_to_prev_item are NOT affected

        Yields:
            self (DictTraversal): The `DictTraversal` object for backward traversal.

        Example:
            ```python
            # Forward traversal (default behavior)
            for item in traversal:
                print(item)

            # Backward traversal using the 'inverted' context manager
            with traversal.inverted():
                for item in traversal:
                    print(item)
            ```

        Note:
            - This context manager can be nested.
            - The state of `inverted_context` will be restored after exiting each with-block.
        """
        self.inverted_context = not self.inverted_context
        self.iter_method = self.move_to_prev_item if self.inverted_context else self.move_to_next_item
        yield self
        self.inverted_context = not self.inverted_context
        self.iter_method = self.move_to_prev_item if self.inverted_context else self.move_to_next_item

    @contextmanager
    def new_root(self, merge=False):
        """
        Context manager for temporarily setting a new root for traversal.

        Behavior:
            - If `merge` is True, creates a new `DictTraversal` object with the current node as root.
            - If `merge` is False, creates a deep copy of the current `DictTraversal` object.
            - Yields the new `DictTraversal` object for use within the context.
            - If `merge` is True, updates the root fields and restores the original path after exiting the context.

        Parameters:
            merge (bool): Whether to merge the changes back to the original object. Default is False.

        Yields:
            DictTraversal: A new `DictTraversal` object with either the current node as root or a deep copy of the original.

        Attributes:
            current (dict): Points to the new root node in the traversal if `merge` is True.
            path (list): Restored to its original state if `merge` is True.
            inverted_context (bool): Inherits the value from the original object.

        Example:
            with traversal.new_root(merge=True) as new_obj:
                # Perform operations on new_obj from the relative traversal path perspective
                # Modifications will affect to the original traversal traversal after with block

            with traversal.new_root(merge=False) as new_obj:
                # Perform operations on new_obj from the relative traversal path perspective
                # Modifications will not affect to the original traversal object after with block
        """
        if merge:
            old_path = self.path
            # Current item as a root
            traversal = DictTraversal(self.current, children_field=self.children_field)
            traversal.inverted_context = self.inverted_context
        else:
            from copy import deepcopy
            traversal = deepcopy(self)
        yield traversal
        if merge:
            # Update root fields
            self.current.update(self._without_children(traversal.items()))
            # Restore path
            self.path = old_path

    def children(self, sibling_only=False):
        """
        Retrieves the children of the current node.

        Parameters:
            sibling_only (bool, optional): If True, returns only the siblings of the current node.

        Returns:
            list: A list of children nodes.

        Behavior:
            - If sibling_only is True, returns a list of siblings without their children.
            - Otherwise, returns a list of children including their own children.

        Example:
            ```python
            next(next(root(traversal)))  # Move to Child 2
            print(traversal.children())  # Output: [{'title': 'Grandchild 1'}, {'title': 'Grandchild 2', 'sections': [{'title': 'Grandgrandchild'}]}]
            print(traversal.children(sibling_only=True))  # Output: [{'title': 'Grandchild 1'}, {'title': 'Grandchild 2'}]
            ```
        """
        that = self.current
        if sibling_only:
            return [self._without_children(item.items()) for item in that.get(self.children_field, [])]
        return that.get(self.children_field, [])

    def get_last_item(self, sibling_only=False):
        """
        Retrieves the last item in the current traversal tree from the current item perspective.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            dict: The last item in the traversal.

        Example:
            ```python
            # Under root
            print(traversal.get_last_item())  # Output: {'title': 'Child 3'}
             # Under Child 2
            next(next(traversal))
            print(traversal.get_last_item())  # Output: {'title': 'Grandgrandchild'}
            ```
        """
        item, _ = self.get_last_item_and_path(sibling_only)
        return item

    def get_last_path(self, sibling_only=False):
        """
        Retrieves the path to the last item in the traversal from the current item perspective.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            list: The path to the last item.

        Example:
            ```python
            # Under root
            print(traversal.get_last_path())  # Output: [2]
            # Under Child 2
            next(next(traversal))
            print(traversal.get_last_path())  # Output: [1, 1, 0]
            ```
        """
        _, path = self.get_last_item_and_path(sibling_only)
        return path

    def set_last_item_as_current(self, sibling_only=False):
        """
        Sets the last item in the traversal as the current item from the current item perspective.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            self: Returns the DictTraversal object itself, pointing to the last node.

        Attributes:
            current (dict): Updated to point to the last node in the traversal.
            path (list): Updated to reflect the new traversal path.

        Example:
            ```python
            traversal.set_last_item_as_current()
            print(traversal)  # Output: {'title': 'Child 3'}
            ```
        """
        self.current, self.path = self.get_last_item_and_path(sibling_only)
        return self

    def get_last_item_and_path(self, sibling_only=False):
        """
        Retrieves the last item and its path in the traversal tree from the current item perspective.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            tuple: A tuple containing the last item (dict) and its path (list).

        Behavior:
            - If sibling_only is True, returns the last sibling and its path.
            - Otherwise, returns the last item in the deepest nested list and its path.

        Example:
            ```python
            item, path = traversal.get_last_item_and_path()
            print(item)  # Output: {'title': 'Child 3'}
            print(path)  # Output: [2]
            ```
        """
        # Current context aware, but inverse is not relevant
        path = self.path[:]
        siblings = self.current.get(self.children_field, [])
        if not siblings:
            return self.current, path
        last_siblings = siblings
        while True:
            if siblings:
                last_siblings = siblings
                path.append(len(last_siblings)-1)
                if sibling_only:
                    break
                siblings = last_siblings[-1].get(self.children_field, [])
            else:
                break
        return last_siblings[-1], path

    def get_parent_item(self):
        """
        Retrieves the parent item of the current item in the traversal.

        Returns:
            dict: The parent item of the current item, without its children.

        Behavior:
            - Returns the parent item without its children.
            - Returns None if the current item is the root.

        Example:
            ```python
            root(traversal)
            # Move to Grandchild 1
            (+++traversal).get_parent_item()  # Returns: {"title": "Child 2"}
            ```
        """
        item, _ = self.get_parent_item_and_path()
        return item

    def get_parent_path(self):
        """
        Retrieves the path to the parent of the current item in the traversal.

        Returns:
            list: The path to the parent of the current item.

        Behavior:
            - Returns an empty list if the current item is the root.

        Example:
            ```python
            root(traversal)
            # Move to Grandchild 1
            (+++traversal).get_parent_path()  # Returns: [1]
        """
        _, path = self.get_parent_item_and_path()
        return path

    def get_parent_item_and_path(self):
        """
        Retrieves both the parent item and the path to the parent of the current item in the traversal.

        Returns:
            tuple: A tuple containing the parent item (without its children) and the path to the parent.

        Note:
            - Returns (None, []) if the current item is the root.

        Example:
            ```python
            root(traversal)
            (+++traversal).get_parent_item_and_path()  # Returns: ({'title': 'Child 2'}, [1])
            ```
        """
        if self.path:
            item = self
            for i in self.path[:-1]:
                items = item.get(self.children_field, [])
                item = items[i]
            return self._without_children(item.items()), self.path[:-1]
        return None, []

    def move_to_next_item(self, sibling_only=False):
        """
        Moves the traversal to the next item.

        Parameters:
            sibling_only (bool, optional): If True, moves only among siblings.

        Returns:
            self: Returns the DictTraversal object itself, pointing to the next node.

        Behavior:
            - Moves the traversal to the next item relative to the current item.
            - If sibling_only is True, moves only among siblings.
            - Will start over beginning after reaching the end.

        Attributes:
            current (dict): Updated to point to the next node in the traversal.
            path (list): Updated to reflect the new traversal path.

        Example:
            ```python
            root(traversal)
            traversal.move_to_next_item()
            print(traversal)  # Output: {'title': 'Child 1'}
            ```
        """
        self.current, self.path = self.get_next_item_and_path(sibling_only)
        return self

    def get_next_item_and_path(self, sibling_only=False):
        """
        Retrieves the next item and its path without altering the state of the object.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            tuple: A tuple containing the next item (dict) and its path (list).

        Behavior:
            - Retrieves the next item and its path relative to the current item.
            - If sibling_only is True, returns the next sibling and its path.

        Example:
            ```python
            root(traversal)
            item, path = traversal.get_next_item_and_path()
            print(item)  # Output: {'title': 'Child 1'}
            print(path)  # Output: [0]
            ```
        """
        items = self.get(self.children_field, [])
        path = self.path
        if not path:
            return items[0], [0]
        current = items
        for index in path[:-1]:
            current = current[index][self.children_field]
        if not sibling_only and self.children_field in current[path[-1]] and len(current[path[-1]][self.children_field]) > 0:
            return current[path[-1]][self.children_field][0], path + [0]
        while path and len(current) <= path[-1] + 1:
            path = path[:-1]
            current = items
            for index in path[:-1]:
                current = current[index][self.children_field]
        return (current[path[-1] + 1], path[:-1] + [path[-1] + 1]) if path else (self, [])

    def move_to_prev_item(self, sibling_only=False):
        """
        Retrieves the previous item and its path without altering the state of the object.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            tuple: A tuple containing the previous item (dict) and its path (list).

        Behavior:
            - Retrieves the previous item and its path relative to the current item.
            - If sibling_only is True, returns the previous sibling and its path.
            - Will start over the the end after reaching the beginning.

        Example:
            ```python
            root(traversal)
            traversal.move_to_prev_item()
            print(traversal)  # Output: {'title': 'Child 3'}
            ```
        """
        self.current, self.path = self.get_previous_item_and_path(sibling_only)
        return self

    def get_previous_item_and_path(self, sibling_only=False):
        """
        Retrieves the previous item and its path without altering the state of the object.

        Parameters:
            sibling_only (bool, optional): If True, considers only the siblings.

        Returns:
            tuple: A tuple containing the previous item (dict) and its path (list).

        Behavior:
            - Retrieves the previous item and its path relative to the current item.
            - If sibling_only is True, returns the previous sibling and its path.

        Example:
            ```python
            root(traversal)
            item, path = traversal.get_previous_item_and_path()
            print(item)  # Output: {'title': 'Child 3'}
            print(path)  # Output: [2]
            ```
        """
        items = self.get(self.children_field, [])

        if self.path:
            path = self.path
        else:
            if sibling_only:
                path = [len(items)] if items else []
            else:
                # Current context affects, but inverse is not relevant
                path = self.get_last_path(sibling_only)
                path[-1] += 1

        if not path:
            return self, []

        current = items
        for index in path[:-1]:
            current = current[index][self.children_field]

        if path[-1] > 0:
            new_path = path[:-1] + [path[-1] - 1]
            new_current = current[new_path[-1]]
            if not sibling_only:
                while new_current.get(self.children_field):
                    new_path.append(len(new_current[self.children_field]) - 1)
                    new_current = new_current[self.children_field][-1]
            return new_current, new_path

        while path:
            path = path[:-1]
            if path:
                current = items
                for index in path[:-1]:
                    current = current[index][self.children_field]
                return current[path[-1]], path

        return self, []

    def count_children(self, sibling_only=False):
        """
        Counts the number of child nodes in the current traversal context.

        Behavior:
            - If `sibling_only` is True, counts only the immediate children of the current node.
            - If `sibling_only` is False, counts all descendants of the current node recursively.
            - Utilizes a private recursive function `_` for counting when `sibling_only` is False.

        Parameters:
            sibling_only (bool): Whether to count only immediate children. Default is False.

        Returns:
            int: The count of child nodes based on the `sibling_only` parameter.

        Attributes:
            current (dict): The current node in the traversal.
            children_field (str): The key used to identify children in the dictionary.

        Note:
            - `traversal.count_children()` is same as `len(traversal)`
            - `traversal.count_children(sibling_only=True)` is same as `len(traversal[:])`

        Example:
            ```python
            count = traversal.count_children(sibling_only=True)  # Counts only immediate children
            print(count)  # Outputs: 3
            count = traversal.count_children()  # Counts all descendants
            print(count)  # Outputs: 6
            ```
        """
        that = self.current
        # Excluding root of that
        if sibling_only:
            return len(that.get(self.children_field, []))
        def _(items):
            count = 0
            for item in items:
                count += 1 + _(item.get(self.children_field, []))
            return count
        return _(that.get(self.children_field, []))

    def add_child(self, **kwargs):
        """
        Adds a new child node to the current node's children.

        Behavior:
            - Adds a new child node with the given keyword arguments to the current node's children list.
            - Initializes the children list if it doesn't exist.

        Parameters:
            **kwargs: Arbitrary keyword arguments to define the new child node.

        Returns:
            self: Returns the `DictTraversal` object for method chaining.

        Attributes:
            current (dict): The current node in the traversal, updated with the new child.

        Example:
            ```python
            traversal.add_child(title="Child X")
            print(last(traversal))  # Outputs: {'title': 'Child X'}
            ```
        """
        if not self.children_field in self.current:
            self.current[self.children_field] = []
        self.current[self.children_field].append(kwargs)
        return self

    def insert_child(self, idx, **kwargs):
        """
        Inserts a new child node at a specific index in the current node's children.

        Behavior:
            - Inserts a new child node with the given keyword arguments at the specified index.
            - Initializes the children list if it doesn't exist.

        Parameters:
            idx (int): The index at which to insert the new child.
            **kwargs: Arbitrary keyword arguments to define the new child node.

        Returns:
            self: Returns the `DictTraversal` object for method chaining.

        Attributes:
            current (dict): The current node in the traversal, updated with the new child.

        Example:
            ```python
            traversal.insert_child(0, title="Child X")
            print(first(traversal))  # Outputs: {'title': 'Child X'}
            ```
        """
        if not self.children_field in self.current:
            self.current[self.children_field] = [kwargs]
        else:
            self.current[self.children_field].insert(idx, kwargs)
        return self

    def replace_child(self, idx, **kwargs):
        """
        Replaces an existing child node at a specific index in the current node's children.

        Behavior:
            - Replaces the child node at the specified index with a new node defined by the keyword arguments.
            - Initializes the children list if it doesn't exist.

        Parameters:
            idx (int): The index of the child to replace.
            **kwargs: Arbitrary keyword arguments to define the new child node.

        Returns:
            self: Returns the `DictTraversal` object for method chaining.

        Attributes:
            current (dict): The current node in the traversal, updated with the new child.

        Example:
            ```python
            traversal.replace_child(0, title="CHILD 1")
            print(first(traversal))  # Outputs: {'title': 'CHILD 1'}
            ```
        """
        if not self.children_field in self.current:
            self.current[self.children_field] = [kwargs]
        else:
            self.current[self.children_field][idx] = kwargs
        return self

    def modify(self, key=None, value=None, **kwargs):
        """
        Modifies the current node's attributes.

        Behavior:
            - Updates the current node's attributes based on the provided key-value pairs.
            - If `key` and `value` are provided, updates that specific attribute.
            - If `kwargs` are provided, updates multiple attributes.

        Parameters:
            key (str, optional): The key of the attribute to modify.
            value: The new value for the specified key.
            **kwargs: Arbitrary keyword arguments to update multiple attributes.

        Returns:
            self: Returns the `DictTraversal` object for method chaining.

        Attributes:
            current (dict): The current node in the traversal, updated with the new attributes.

        Example:
            ```python
            traversal.modify(title="ROOT")
            print(traversal)  # Outputs: {'title': 'ROOT'}
            ```
        """
        if key:
            self.current[key] = value
        if kwargs:
            self.current.update(**kwargs)
        return self

    def __getitem__(self, idx):
        """
        Retrieves an item based on the given index.

        Behavior:
            - If index is an int or slice, retrieves child nodes from the current node.
            - If index is a tuple or list, traverses the nested children to retrieve the item.
            - If index is a string, retrieves the value of the corresponding attribute in the current node.

        Parameters:
            idx (int, slice, tuple, list, str): The index to retrieve the item.

        Returns:
            dict or any: The retrieved item or attribute value.

        Raises:
            IndexError: If children are not found at the given index.
            ValueError: If index type is not supported.

        Attributes:
            current (dict): The current node in the traversal.
            children_field (str): The key used to identify children in the dictionary.

        Example:
            ```python
            item = traversal[0]  # Retrieves the first child of the current node
            item = traversal[(0, 0)]  # Retrieves the first child of the first child of the current node
            items = traversal[1:2]  # Retrieves the children of the current node
            item = traversal['name']  # Retrieves the 'name' attribute of the current node
            ```
        """
        that = self.current
        if isinstance(idx, int) or isinstance(idx, slice):
            if self.children_field in that:
                return that[self.children_field][idx]
            else:
                return {}
        if isinstance(idx, tuple) or  isinstance(idx, list):
            item = that
            for i in idx:
                if self.children_field in item:
                    item = item[self.children_field][i]
                else:
                    raise IndexError("Children not found from the given index")
            return item
        elif isinstance(idx, str):
            return that.get(idx, None)
        else:
            raise ValueError("Index must be one of the types: int, splice, tuple, list, or str.")

    def __delitem__(self, idx):
        """
        Deletes an item based on the given index.

        Behavior:
            - If index is an int or slice, deletes child nodes from the current node.
            - If index is a tuple or list, traverses the nested children to delete the item.
            - If index is a string, deletes the corresponding attribute in the current node.

        Parameters:
            idx (int, slice, tuple, list, str): The index to delete the item.

        Raises:
            IndexError: If children are not found at the given index.
            ValueError: If index type is not supported.

        Attributes:
            current (dict): The current node in the traversal, updated after deletion.

        Example:
            ```python
            del obj[0]  # Deletes the first child of the current node
            del traversal[(0, 0)]  # Deleted the first child of the first child of the current node
            del traversal[1:2]  # Deleted the children of the current node
            del obj['name']  # Deletes the 'name' attribute of the current node
            ```
        """
        that = self.current
        if isinstance(idx, int) or isinstance(idx, slice):
            del that[self.children_field][idx]
        elif isinstance(idx, tuple) or  isinstance(idx, list):
            item = that
            for i in idx[:-1]:
                if self.children_field in item:
                    item = item[self.children_field][i]
                else:
                    raise IndexError("Children not found from the given index")
            if self.children_field in item:
                del item[self.children_field][idx[-1]]
            else:
                raise IndexError("Children not found from the given index")
        elif isinstance(idx, str):
            if isinstance(that, DictTraversal):
                super().__delitem__(idx)
            else:
                del that[idx]
        else:
            raise ValueError("Index must be one of the types: int, splice, tuple, list, or str.")

    def _without_children(self, items):
        """
        Helper method to remove the children field from a dictionary.

        Parameters:
            items (dict): The dictionary from which to remove the children field.

        Returns:
            dict: The dictionary without its children field.

        Behavior:
            - Removes the children field specified by `self.children_field` from the dictionary.
        """
        return {k: v for k, v in items if k != self.children_field}

    def __repr__(self):
        """
        Returns a string representation of the current item in the traversal.

        Returns:
            str: A string representation of the current item, excluding the children field.

        Behavior:
            - Provides a string representation of the current item in the traversal.
            - Excludes the children field from the representation.

        Example:
            ```python
            print(repr(traversal))  # Output: {'title': 'root'}
            ```
        """
        if not self.current:
            raise ValueError("Internal error: missing the current item.")
        return str(self._without_children(self.current.items()))

    def __len__(self):
        """
        Returns the total number of children nodes relative to the root node, excluding the root itself.
        Can also be used with slicing `len(traversal[:])` to get the number of siblings. In that case,
            count is actually retrieved by __getitem__ from the children.

        Returns:
            int: The total number of children nodes or siblings, depending on usage.

        Note:
            - This method operates relative to the root node and delegates to the count_children method to get the count.

        Example:
            ```python
            print(len(traversal))  # Output: 3
            print(len(traversal[:]))  # Output: 2 (number of siblings)
            ```
        """
        return self.count_children()

    def max_depth(self):
        """
        Returns the maximum depth of the traversal tree of the current node.

        Returns:
            int: The maximum depth of the traversal tree.

        Behavior:
            - Calculates the maximum depth of the traversal tree.
            - Depth starts from 0 at the root.

        Example:
            ```python
            print(traversal.max_depth())  # Output: 3
            ```
        """
        depth = 0
        def _(items, level=0):
            nonlocal depth
            if level > depth:
                depth += 1
            for item in items:
                _(item.get(self.children_field, []), level + 1)
            return depth
        return _(self.current.get(self.children_field, []))

    def peek_next(self, steps=1):
        """
        Peeks at the next item(s) in the traversal without altering the current pointer.

        Parameters:
            steps (int, optional): Number of steps to peek ahead. Defaults to 1.

        Returns:
            dict: The item that would be reached if moved `steps` ahead.

        Behavior:
            - Cycles back to the root if the end is reached.
            - Temporarily alters the current item and path, restoring them before returning.

        Note:
            - `steps` must be a positive integer.
            - Influenced by the `inverted` context manager.

        Example:
            ```python
            print(traversal.peek_next(2))  # Output: {'title': 'Child 2'}

            # With inverted context
            with traversal.inverted():
                print(traversal.peek_next(2))  # Output: {'title': 'Grandgrandchild'}
            ```
        """
        current, path = self.current.copy(), self.path.copy()
        func = self.move_to_prev_item if self.inverted_context else self.move_to_next_item
        for _ in range(steps if steps > 0 else 1):
            item = func().current
        self.current, self.path = current, path
        return self._without_children(item.items())

    def peek_prev(self, steps=1):
        """
        Peeks at the previous item(s) in the traversal without altering the current pointer.

        Parameters:
            steps (int, optional): Number of steps to peek back. Defaults to 1.

        Returns:
            dict: The item that would be reached if moved `steps` back.

        Behavior:
            - Cycles back to the end if the start is reached.
            - Temporarily alters the current item and path, restoring them before returning.

        Note:
            - `steps` must be a positive integer.
            - Influenced by the `inverted` context manager.

        Example:
            ```python
            print(traversal.peek_prev(2))  # Output: {'title': 'Grandgrandchild'}

            # With inverted context
            with traversal.inverted():
                traversal.peek_prev(2)  # Output: {'title': 'Child 2'}
            ```
        """
        current, path = self.current.copy(), self.path.copy()
        func = self.move_to_next_item if self.inverted_context else self.move_to_prev_item
        for _ in range(steps if steps > 0 else 1):
            item = func().current
        self.current, self.path = current, path
        return self._without_children(item.items())

    def find_paths(self, label_field, titles):
        """
        Locate nodes by matching their titles to a list of specified field values.

        Parameters:
            label_field (str): Field name to be used as label of each node. Default is None.
            titles (list or str): Field values to match against node titles. Can be a single string or a list of strings.

        Returns:
            list: A list of tuples, each containing a node and its path that matches the field values.

        Behavior:
            - Converts 'titles' to a list if it's a single string.
            - Initializes an empty list `results` to store matching nodes and their paths.
            - Defines a recursive function `_` to search for nodes with matching titles.
            - Calls `_` starting from the current node's subnodes, passing the list of remaining titles to match.
            - Appends matching items and their paths to `results`. Items in the result list do not contain childrens.

        Example:
            ```python
            traversal.find_paths("title", ["Child 2", "Grandchild 1"])  # Returns: [({'title': 'Grandchild 1'}, [1, 0])
            ```
        """
        if not isinstance(titles, list):
            titles = [titles]

        results = []

        def _(subitems, remaining_titles, new_path=[]):
            for i, item in enumerate(subitems):
                if remaining_titles and item[label_field] == remaining_titles[0]:
                    local_path = new_path + [i]
                    if len(remaining_titles) == 1:
                        results.append((self._without_children(item.items()), local_path))
                    subitems = item.get(self.children_field, [])
                    if subitems:
                        return _(subitems, remaining_titles[1:], local_path)
        _(self.current.get(self.children_field, []), titles)
        return results

    def pretty_print(self, label_field=None):
        """
        Recursively print the tree from the relative current item in a formatted manner.

        Parameters:
            label_field (str): Field name to be used as label of each node. Default is None.

        Behavior:
            - Prints the string representation of the traversal tree, indented by the specified amount.
            - If label_field is not given, repr is used to show the item excluding its children.
            - Recursively traverses (inner function `_`) and prints all children,
                incrementing the indentation level by 1 for each level.

        Example:
            ```python
            traversal.pretty_print(label_field="title")  # Output:
            # root
            #   Child 1
            #   Child 2
            #      Grandchild 1
            #      Grandchild 2
            #          Grandchildchild
            #   Child 3
            ```
        """
        that = self.current
        print(that[label_field] if label_field else "root")
        def _(indent, items):
            for item in items:
                print('  ' * indent + (item[label_field] if label_field and label_field in item else repr(self._without_children(item.items()))))
                _(indent + 1, item.get(self.children_field, []))
        _(1, that.get(self.children_field, []))

    def visualize(self, label_field=None, from_root=False):
        """
        Generates a string representation of the traversal tree.

        Behavior:
            - If `from_root` is True, starts the visualization from the root node.
            - If `label_field` is provided, uses it as the label for each node.
            - Marks the current node with an asterisk (*).

        Parameters:
            label_field (str, optional): Field name to be used as the label for each node. Default is None.
            from_root (bool): Whether to start the visualization from the root node. Default is False.

        Returns:
            str: A string representing the traversal tree, with indentation to indicate nesting levels.

        Attributes:
            current (dict): The current node in the traversal.
            children_field (str): The key used to identify children in the dictionary.

        Example:
            ```python
            print(next(root(traversal)).visualize("title", from_root=True))  # Output:
            # root
            # ├── Child 1*
            # ├── Child 2
            # │   ├── Grandchild 1
            # │   └── Grandchild 2
            # │       └── Grandgrandchild
            # └── Child 3

            print(next(next(root(traversal))).visualize("title"))  # Output:
            # Child 2*
            # ├── Grandchild 1
            # └── Grandchild 2
            #     └── Grandgrandchild
            ```
        """
        that = self if from_root else self.current
        current_item = self.current
        current_title = (current_item[label_field] if label_field in current_item else self._without_children(current_item.items())) if current_item else ""
        # We can not use __getitems__ directly, because it gets values from current item context
        labels = [v for k, v in that.items() if k == label_field]
        item_label = labels[0] if labels else "Untitled"
        toc = [item_label + ("*" if item_label == current_title else "")]
        def _(items, level=1, prefix=''):
            items_length = len(items[:])
            for i, item in enumerate(items):
                is_last = i == items_length - 1
                new_prefix, spacer = ('└── ', '    ') if is_last else ('├── ', '│   ')
                item_label = item[label_field] if label_field in item else self._without_children(item.items())
                toc.append(f"{prefix}{new_prefix}{item_label}{'*' if item_label == current_title else ''}")
                subitems = item.get(self.children_field, [])
                if subitems:
                    _(subitems, level + 1, prefix + spacer)
        items = [v for k, v in that.items() if k == self.children_field]
        if items:
            _(items[0])
        return '\n'.join(toc)


def validate_data(data, children_field, label_field=None):
    """
    Validates a nested dictionary structure for specific field requirements.

    Parameters:
        - data (dict): The nested dictionary to validate.
        - children_field (str): The field name that contains child dictionaries.
        - label_field (str, optional): The field name that should exist in each dictionary, including the root.

    Behavior:
        - Validates that the root is a non-empty dictionary.
        - Validates that the `children_field` exists in the root if `label_field` is not provided.
        - Validates that `label_field` exists in each nested dictionary, if specified.
        - Validates that each `children_field` is a list.
        - Validates that each child in `children_field` is a non-empty dictionary.

    Raises:
        - ValueError: If any of the validation conditions are not met.

    Example:
        ```python
        try:
            validate_data({'title': 'root', 'sections': [{'title': 'Child'}]}, 'sections', 'title')
            print(f"Given data is valid.")
        except ValueError as e:
            print(f"Given data is invalid. {e}")
        ```
    """
    if not isinstance(data, dict) or not data:
        raise ValueError("Data must be a dictionary and not empty.")

    if not label_field and children_field not in data:
            raise ValueError(f"The field '{children_field}' must exist in root when label field has not been given.")

    def _validate(item):
        if label_field and label_field not in item:
            raise ValueError(f"The field '{label_field}' must exist in root and every nested item.")
        if children_field in item:
            children = item[children_field]
            if not isinstance(children, list):
                raise ValueError(f"The field '{children_field}' must be a list.")
            for child in children:
                if not isinstance(child, dict) or not child:
                    raise ValueError(f"Child must be a dictionary and it must contain data.")
                _validate(child)

    _validate(data)


def prev(traversal):
    """
    Moves the traversal to the previous item relative to the current item.

    Parameters:
        traversal (DictTraversal): The `DictTraversal` object to operate on.

    Returns:
        DictTraversal: The updated `DictTraversal` object pointing to the previous item.

    Behavior:
        - Updates the `current` attribute to point to the previous item in the tree.
        - Raises StopIteration if there is no previous item.
        - Influenced by the `inverted` context manager.

    Note:
        - Serves as a counterpart to Python's built-in `next` function.
        - Does not support a `siblings_only` argument; use `move_to_next_item` or `move_to_prev_item` directly for that.
        - Unlike `move_to_next_item` and `move_to_prev_item`, which cycle through the tree, `prev` raises StopIteration when reaching the end.

    Raises:
        StopIteration: If there are no more items to traverse in the backward direction.

    Example:
        ```python
        last(traversal)
        try:
            print(traversal['title'])  # Output: Grandgrandchild
            prev(traversal)
            print(traversal['title'])  # Output: Grandchild 2
        except StopIteration:
            print("No more items to traverse.")

        # With inverted context
        last(traversal)
        with traversal.inverted():
            try:
                print(traversal['title'])  # Output: Grandgrandchild
                prev(traversal)
                print(traversal['title'])  # Output: Child 3
            except StopIteration:
                print("No more items to traverse.")
        ```
    """
    if traversal.inverted_context:
        traversal.move_to_next_item()
        if not traversal.path:
            raise StopIteration
    else:
        if not traversal.path:
            raise StopIteration
        traversal.move_to_prev_item()
    return traversal


def root(traversal):
    """
    Resets the traversal to the root item.

    Parameters:
        - traversal (DictTraversal): The `DictTraversal` object to operate on.

    Behavior:
        - Resets the traversal to the root item, updating the `current` attribute.

    Returns:
        traversal (DictTraversal): The updated `DictTraversal` object pointing to the root item.

    Example:
        ```python
        root(traversal)  # Returns: {"title": "root"}
        ```
    """
    iter(traversal)
    if traversal.inverted_context:
        return traversal
    return next(traversal)


def first(traversal):
    """
    Moves the traversal to the first item relative to the root.

    Parameters:
        - traversal (DictTraversal): The `DictTraversal` object to operate on.

    Behavior:
        - Moves the traversal to the first item in the tree, updating the `current` attribute.

    Returns:
        traversal (DictTraversal): The updated `DictTraversal` object pointing to the first item.

    Example:
        ```python
        first(traversal)  # Returns: {"title": "Child 1"}
        ```
    """
    if traversal.inverted_context:
        root(traversal)
        return traversal.set_last_item_as_current()
    return next(root(traversal))


def last(traversal):
    """
    Moves the traversal to the last item from the current item perspective.

    Parameters:
        - traversal (DictTraversal): The `DictTraversal` object to operate on.

    Behavior:
        - Moves the traversal to the last item in the tree, updating the `current` attribute.

    Returns:
        traversal (DictTraversal): The updated `DictTraversal` object pointing to the last item.

    Example:
        ```python
        last(traversal)  # Returns: {"title": "Child 3"}
        # Calling the end node, same will be returned
        last(traversal)  # Returns: {"title": "Child 3"}
        ```
    """
    if traversal.inverted_context:
        return iter(traversal).move_to_next_item()
    return traversal.set_last_item_as_current()


def demo():
    """
    Initializes and returns a `DictTraversal` object with sample data.

    Behavior:
        - Creates a nested dictionary structure with `title` and `sections` fields.
        - Initializes a `DictTraversal` object with the sample data.

    Returns:
        - DictTraversal: An initialized `DictTraversal` object.

    Example:
        ```python
        traversal = demo()
        traversal.pretty_print()  # Outputs:
        root
          Child 1
          Child 2
            Grandchild 1
            Grandchild 2
              Grandgrandchild
          Child 3
        ```
    """
    children_field = 'sections'
    sample_data = {
        'title': 'root',
        children_field: [
            {'title': 'Child 1'},
            {'title': 'Child 2', children_field: [
                {'title': 'Grandchild 1'},
                {'title': 'Grandchild 2', children_field: [
                    {'title': 'Grandgrandchild'}
                ]}
            ]},
            {'title': 'Child 3'}
        ]
    }

    # Initialize the DictTraversal class with revised nested sample_data and 'sections' as the children_field
    return DictTraversal(sample_data, children_field=children_field)
