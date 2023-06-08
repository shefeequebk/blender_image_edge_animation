import math


def group_nearby_curves(curves_end_removed):
    def distance(point1, point2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    # Define your list of curves here, each curve is a list of pixel coordinates.
    curves = curves_end_removed

    threshold = 10

    changes = True
    while changes:
        changes = False
        for i in range(len(curves)):
            for j in range(i + 1, len(curves)):
                # Check the distance between the last point of the i-th curve and the first point of the j-th curve
                if distance(curves[i][-1], curves[j][0]) < threshold:
                    curves[i] = curves[i] + curves[j]
                    del curves[j]
                    changes = True
                    break

                # Check the distance between the first point of the i-th curve and the last point of the j-th curve
                elif distance(curves[i][0], curves[j][-1]) < threshold:
                    curves[i] = curves[j] + curves[i]
                    del curves[j]
                    changes = True
                    break

                # Check the distance between the last point of the i-th curve and the last point of the j-th curve
                elif distance(curves[i][-1], curves[j][-1]) < threshold:
                    curves[i] += curves[j][::-1]
                    del curves[j]
                    changes = True
                    break

                # Check the distance between the first point of the i-th curve and the first point of the j-th curve
                elif distance(curves[i][0], curves[j][0]) < threshold:
                    curves[i] = curves[i][::-1] + curves[j]
                    del curves[j]
                    changes = True
                    break

            if changes:
                break

    curves = [crv for crv in curves if len(crv) > 20]

    return curves
