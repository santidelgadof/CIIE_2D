import random
import pygame
from TrashGame.TrashItem import TrashItem


class Spawner:
    def __init__(self, spawn_interval, distance_between_items, velocity, available_pngs):
        self.spawn_interval = spawn_interval  # Spawn a new TrashItem every spawn_interval milliseconds
        self.distance_between_items = distance_between_items  # Desired distance between each trash item
        self.velocity = velocity  # Velocity of the trash items
        self.last_spawn_time = pygame.time.get_ticks()
        self.available_trash_items = available_pngs

    def update(self, trash_items, current_time):
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = current_time
            trash_items.append(self.generate_trash_item())
            return trash_items  # Indicates that a new TrashItem should be spawned
        return trash_items  # Indicates that no new TrashItem should be spawned yet

    def generate_trash_item(self) -> TrashItem:
        random_item = random.choice(self.available_trash_items)
        trash_item = TrashItem(random_item[0], (80, 80), (360, -100), self.velocity, random_item[1])
        return trash_item