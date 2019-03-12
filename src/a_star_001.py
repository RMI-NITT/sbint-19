#!/usr/bin/env python
import math


class Node(object):
    """Node object for A* Algorithm"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.val = 0
        self.dist = 0
        self.heuristic = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, goal):
    """Returns shortest path from initial to the final node based on Euclidean for Heuristic

    maze - grid of 0 and 1. 0 - free cell, 1 - obstacle cell
    start - tuple indicating the (x, y) of start node
    goal - tuple indicating the (x, y) of the goal node

    :returns list of tuples, the path from the start to the goal. None if no path is found
    """
    fnode = Node(None, start)
    enode = Node(None, goal)

    # Make sure within range
    if start[0] > (len(maze) - 1) or start[0] < 0 or start[1] > (
            len(maze[len(maze) - 1]) - 1) or start[1] < 0:
        return "Invalid Start!!"

    # Make sure within range
    if goal[0] > (len(maze) - 1) or goal[0] < 0 or goal[1] > (
            len(maze[len(maze) - 1]) - 1) or goal[1] < 0:
        return "Invalid Goal!!"

    if maze[goal[0]][goal[1]] == 1:
        return "No PATH to obstacle!!"

    if maze[start[0]][start[1]] == 1:
        return "No PATH from obstacle!!"

    adj_mat = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    gray_list = []
    visited = []

    gray_list.append(fnode)

    while len(gray_list) > 0:
        cur_node = gray_list[0]
        cur_ind = 0
        for i, n in enumerate(gray_list):
            if n.val < cur_node.val:
                cur_node = n
                cur_ind = i
        gray_list.pop(cur_ind)
        visited.append(cur_node)
        #print(cur_node.position)

        # Goal found
        if cur_node == enode:
            path = []
            cur = cur_node
            while cur is not None:
                path.append(cur.position)
                cur = cur.parent
            return path[::-1]

        children = []
        for pos in adj_mat:
            node_position = (cur_node.position[0] + pos[0], cur_node.position[1] + pos[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(cur_node, node_position)
            children.append(new_node)

        for child in children:
            # for vis_child in visited:
            #     if child == vis_child:
            #         continue
            if child in visited:
                continue
            child.dist = cur_node.dist + 1

            # Eculidean Squared
            # child.heuristic = ((child.position[0] - enode.position[0]) ** 2) \
            #                    + ((child.position[1] - enode.position[1]) ** 2)

            # Euclidean distance
            # child.heuristic = math.sqrt(((child.position[0] - enode.position[0]) ** 2)
            #                             + ((child.position[1] - enode.position[1]) ** 2))

            # Modifying with Diagonal distance
            child.heuristic = max(abs(child.position[0] - enode.position[0])
                                  , abs(child.position[1] - enode.position[1]))
            child.val = child.dist + child.heuristic

            is_cur = False
            for gray_node in gray_list:
                if child == gray_node and child.val > gray_node.val:
                    is_cur = True
                    break
            if not is_cur:
                gray_list.append(child)
        #print(len(gray_list))


def main():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    goal = (7, 6)
    path = astar(maze, start, goal)
    print(path)


if __name__ == "__main__":
    main()
