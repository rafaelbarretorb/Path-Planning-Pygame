import math

def dist(p1, p2):    
    """ Class method for compute the distance between two points.

    Args:
        p1: Point 1 tuple.
        p2: Poinf 2 tuple.

    Returns:
        The distance between two points the in cartesian plan.

    """
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
