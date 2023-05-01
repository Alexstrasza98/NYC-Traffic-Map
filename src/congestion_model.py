def simple_congestion_model(expected_speed: int, actual_speed: int) -> int:
    """
    Evalute congestion level of a road segment depending on the difference between expected and actual speed.
    This model is a naive version, which only considers the speed difference.
    Reference: https://developer.tomtom.com/traffic-api/documentation/traffic-flow/raster-flow-tiles

    Params:
        expected_speed: Expected speed of a road segment
        actual_speed: Actual speed of a road segment

    Returns:
        congestion_level: Congestion level of a road segment
    """

    speed_percentage = actual_speed / expected_speed

    assert (
        speed_percentage >= 0 and speed_percentage <= 1
    ), f"Speed percentage must be between 0 and 1, got {speed_percentage}"

    # 0 is reserved for road closed
    if speed_percentage < 0.15:
        congestion_level = 1
    elif speed_percentage < 0.35:
        congestion_level = 2
    elif speed_percentage < 0.75:
        congestion_level = 3
    else:
        congestion_level = 4

    return congestion_level


def generate_congestion_level(road_closure, free_flow_speed, current_speed):
    """
    Generate congestion level for one piece of road segment
    """

    if road_closure:
        return 0
    else:
        return simple_congestion_model(free_flow_speed, current_speed)
