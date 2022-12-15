import pygame


def check_id_in_group(all_objekts, idd):
    for i in all_objekts:
        if i.id == idd:
            return i
    return False