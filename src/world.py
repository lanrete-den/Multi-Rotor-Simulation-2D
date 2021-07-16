import math

from block import *
from utilities import *

class World:

    FLOOR_LEVEL = -0.05
    eps_dist = 1

    def init_block_slots(self):
        _, block_slot_nodes, tower_slot_nodes, _ = readNodesCoordsAndEdges("nodes.txt")
        block_slot_busy = dict()
        for slot in block_slot_nodes:
            block_slot_busy[slot] = False

    def __init__(self, ui):
        self.__blocks = []
        self.ui = ui

    def new_block(self, uColor, uX, uZ):
        b = Block(uColor)
        b.set_pose(uX, uZ, 0)
        self.__blocks.append(b)

    def count_blocks(self):
        return len(self.__blocks)

    def block_slot_busy(self, uX, uZ):
        for b in self.__blocks:
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, (uX, uZ))
            if dist < self.eps_dist:
                return True
        return False

    def sense_distance(self):
        robot_pose = self.quadrotor.get_pose_xz()
        L = self.ui.arm.element_3_model.L
        d = y - L - World.FLOOR_LEVEL
        min_dist = 9999999
        for b in self.__blocks:
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
        if min_dist < self.eps_dist:
            return min_dist
        else:
            return None

    def sense_color(self):
        robot_pose = self.quadrotor.get_pose_xz()
        L = self.ui.arm.element_3_model.L
        d = y - L - World.FLOOR_LEVEL
        min_dist = 9999999
        eps_dist = 1
        for b in self.__blocks:
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
                min_block = b
        if min_dist < eps_dist:
            return min_block.get_color()
        else:
            return None

    def paint(self, qp):
        for b in self.__blocks:
            b.paint(qp)

