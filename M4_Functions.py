import pygame


def collide_line_rect(line, rect):
    points = [False, False, False, False]
    k1 = ((line.end_cord[1] - line.cord[1]) / (
            line.end_cord[0] - line.cord[0])) if line.end_cord[0] != line.cord[0] else 1000000000
    b1 = line.cord[1] - (k1 * line.cord[0])
    k2 = 0
    b2 = rect.cord[1] - (rect.height / 2)
    # print(k1, b1 ,k2, b2)
    x = (((b2 - b1) / (k1 - k2)) if k1 != k2 else False) if abs(k1 - k2) >= 10 ** -6 else False
    # print(abs(k1 - k2))
    if x:
        y = k2 * x + b2
        if x > min(line.end_cord[0], line.cord[0]) and x < max(line.end_cord[0], line.cord[0]) and x > min(
                rect.cord[0] + rect.width / 2, rect.cord[0] - rect.width / 2) and x < max(rect.cord[0] + rect.width / 2,
                                                                                          rect.cord[
                                                                                              0] - rect.width / 2):
            points[0] = (x, y)
            # print(0, (x, y))

    k2 = 0
    b2 = rect.cord[1] + (rect.height / 2)
    # print(k1, b1 ,k2, b2)
    x = (((b2 - b1) / (k1 - k2)) if k1 != k2 else False) if abs(k1 - k2) >= 10 ** -6 else False
    # print(abs(k1 - k2))
    if x:
        y = k2 * x + b2
        if x > min(line.end_cord[0], line.cord[0]) and x < max(line.end_cord[0], line.cord[0]) and x > min(
                rect.cord[0] + rect.width / 2, rect.cord[0] - rect.width / 2) and x < max(rect.cord[0] + rect.width / 2,
                                                                                          rect.cord[
                                                                                              0] - rect.width / 2):
            points[1] = (x, y)
            # print(1, (x, y))

    k1 = ((line.end_cord[0] - line.cord[0]) / (
            line.end_cord[1] - line.cord[1])) if line.end_cord[1] != line.cord[1] else 1000000000
    b1 = line.cord[0] - (k1 * line.cord[1])
    k2 = 0
    b2 = rect.cord[1] - (rect.height / 2)
    y = (((b2 - b1) / (k1 - k2)) if k1 != k2 else False) if abs(k1 - k2) >= 10 ** -6 else False
    if y:
        x = k2 * y + b2
        # print(x, y)
        if y > min(line.end_cord[1], line.cord[1]) and y < max(line.end_cord[1], line.cord[1]) and y < max(
                rect.cord[1] + rect.height / 2, rect.cord[1] - rect.height / 2) and y > min(
                rect.cord[1] + rect.height / 2, rect.cord[1] - rect.height / 2):
            points[2] = (x, y)

    k2 = 0
    b2 = rect.cord[1] + (rect.height / 2)
    y = (((b2 - b1) / (k1 - k2)) if k1 != k2 else False) if abs(k1 - k2) >= 10 ** -6 else False
    if y:
        x = k2 * y + b2
        # print(x, y)
        if y > min(line.end_cord[1], line.cord[1]) and y < max(line.end_cord[1], line.cord[1]) and y < max(
                rect.cord[1] + rect.height / 2, rect.cord[1] - rect.height / 2) and y > min(
            rect.cord[1] + rect.height / 2, rect.cord[1] - rect.height / 2):
            points[3] = (x, y)

    return points
