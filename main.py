# Extra features exceeding the minimum challenge criteria:
# Support for floating point numbers
# Checks user input for correctness
# Returns intersecting points
# Supports intersections with 3D lines and cylinders
# Allows line points to be inside the circle or cylinder
# Supports intersections for line segments, not just infinitely long lines

import math
from decimal import Decimal, InvalidOperation

# Coordinate, radius, and height parameters
lineX1, lineY1, lineZ1 = 0, 0, 0
lineX2, lineY2, lineZ2 = 0, 0, 0

circX, circY, circR = 0, 0, 0

cyliX, cyliY, cyliZ = 0, 0, 0
cyliR, cyliH = 0, 0

# Keeps track of input status
validLine = False
validCircle = False
validCylinder = False
inputComplete = False


# Returns whether an input is valid or not
def isvalid(value):
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


# Returns the length of a 2D line
def linelength(x1, y1, x2, y2):
    return Decimal(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


# Returns the slope of a 2D line
def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


# Returns the y-intercept of a 2D line
def yintercept(x, y, slope):
    return y - slope * x


# Returns the direction vector along an axis
def directionvector(point1, point2):
    return point2 - point1


# Returns the parameter used in parametric form of a line
def parameterize(point1, point2, direction):
    return (point2 - point1) / direction


# Returns whether a point is inside a circle or not
def insidecircle(x, y, circX, circY, circR):
    return (x - circX) ** 2 + (y - circY) ** 2 < circR ** 2


# Returns whether a line's z-coordinates are inside a cylinder or not
def insidecylinder(z1, z2, cyliMaxZ, cyliMinZ):
    return cyliMaxZ > z1 > cyliMinZ and cyliMaxZ > z2 > cyliMinZ

# create a function to verify whether a 2D intersection is on the perimeter

# Returns line intersection with bases
def baseintersection(lineX, lineY, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector):
    # Check for top base intersection
    if lineZ1 >= cyliMaxZ >= lineZ2 or lineZ2 >= cyliMaxZ >= lineZ1:
        scalar1 = parameterize(lineZ1, cyliMaxZ, zvector)
        x1 = lineX + scalar1 * xvector
        y1 = lineY + scalar1 * yvector

        # Check for bottom base intersection
        if lineZ2 <= cyliMinZ or lineZ1 <= cyliMinZ:
            scalar2 = parameterize(lineZ1, cyliMinZ, zvector)
            x2 = lineX + scalar2 * xvector
            y2 = lineY + scalar2 * yvector

            if insidecircle(x1, y1, cyliX, cyliY, cyliR):
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, cyliMaxZ))
            if insidecircle(x2, y2, cyliX, cyliY, cyliR):
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x2, y2, cyliMinZ))
            return True
        else:
            print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, cyliMaxZ))
            return True
    # Check for bottom base intersection
    elif lineZ1 <= cyliMinZ <= lineZ2 or lineZ2 <= cyliMinZ <= lineZ1:
        scalar1 = parameterize(lineZ1, cyliMinZ, zvector)
        x1 = lineX + scalar1 * xvector
        y1 = lineY + scalar1 * yvector

        # Check for top base intersection
        if lineZ2 >= cyliMaxZ or lineZ1 >= cyliMaxZ:
            scalar2 = parameterize(lineZ1, cyliMaxZ, zvector)
            x2 = lineX + scalar2 * xvector
            y2 = lineY + scalar2 * yvector

            if insidecircle(x1, y1, cyliX, cyliY, cyliR):
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, cyliMaxZ))
            if insidecircle(x2, y2, cyliX, cyliY, cyliR):
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x2, y2, cyliMinZ))
            return True
        else:
            print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, cyliMinZ))
            return True


# Returns circle and line intersection
def intersect2d(lineX1, lineY1, lineX2, lineY2, circX, circY, circR):
    # Variables needed to initialize quadratic equation variables
    lineSlope = slope(lineX1, lineY1, lineX2, lineY2)
    yIntercept = yintercept(lineX1, lineY1, lineSlope)

    # Variables used in quadratic equation
    a = 1 + lineSlope ** 2
    b = 2 * (lineSlope * (yIntercept - circY) - circX)
    c = (yIntercept - circY) ** 2 + circX ** 2 - circR ** 2
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        print("\nNo intersection.")
    elif discriminant == 0:
        x = -b / (2 * a)
        y = lineSlope * x + yIntercept
        print("One intersection: ({:.3f},{:.3f})".format(x, y))
    else:
        x1 = (-b + Decimal(math.sqrt(discriminant))) / (2 * a)
        x2 = (-b - Decimal(math.sqrt(discriminant))) / (2 * a)
        y1 = lineSlope * x1 + yIntercept
        y2 = lineSlope * x2 + yIntercept
        # Quadratic formula assumes infinite line so this restricts it into a line segment
        if (lineX1 <= x1 <= lineX2 or lineX1 >= x1 >= lineX2) and (lineY1 <= y1 <= lineY2 or lineY1 >= y1 >= lineY2):
            print("One intersection: ({:.3f},{:.3f})".format(x1, y1))
        if (lineX1 <= x2 <= lineX2 or lineX1 >= x2 >= lineX2) and (lineY1 <= y2 <= lineY2 or lineY1 >= y2 >= lineY2):
            print("One intersection: ({:.3f},{:.3f})".format(x2, y2))
        else:
            print("No intersection.")


# Returns cylinder and line intersection
def intersect3d(lineX1, lineY1, lineZ1, lineX2, lineY2, lineZ2, cyliX, cyliY, cyliZ, cyliR, cyliH):
    # Variables needed to initialize quadratic equation variables
    lineSlope = slope(lineX1, lineY1, lineX2, lineY2)
    yIntercept = yintercept(lineX1, lineY1, lineSlope)

    # Variables used in quadratic equation
    a = 1 + lineSlope ** 2
    b = 2 * (lineSlope * (yIntercept - cyliY) - cyliX)
    c = (yIntercept - cyliY) ** 2 + cyliX ** 2 - cyliR ** 2
    discriminant = b ** 2 - 4 * a * c

    # Highest and lowest points of cylinder along the z-axis
    cyliMaxZ = cyliZ + cyliH / 2
    cyliMinZ = cyliZ - cyliH / 2

    # Direction vectors of the line for each axis
    xvector = directionvector(lineX1, lineX2)
    yvector = directionvector(lineY1, lineY2)
    zvector = directionvector(lineZ1, lineZ2)

    # Special variable to switch between intersection cases
    case = 0

    # Checks if the line's 2D projection is inside the base
    if insidecircle(lineX1, lineY1, cyliX, cyliY, cyliR) and insidecircle(lineX2, lineY2, cyliX, cyliY, cyliR):
        # Checks if the line's z-coordinates are inside the cylinder
        if insidecylinder(lineZ1, lineZ2, cyliMaxZ, cyliMinZ):
            case = -1
        else:
            case = -2
    # Checks if the line's 2D projection is outside the base
    elif (not (insidecircle(lineX1, lineY1, cyliX, cyliY, cyliR) or insidecircle(lineX2, lineY2, cyliX, cyliY, cyliR))
          and linelength(lineX1, lineY1, lineX2, lineY2) < cyliR * 2):
        case = -1
    # Check if only one point of the line's 2D projection is inside the base
    elif (insidecircle(lineX1, lineY1, cyliX, cyliY, cyliR) and not insidecircle(lineX2, lineY2, cyliX, cyliY, cyliR) or
          insidecircle(lineX2, lineY2, cyliX, cyliY, cyliR) and not insidecircle(lineX1, lineY1, cyliX, cyliY, cyliR)):
        case = 1

    # Zero 2D intersections
    if case < 0:
        if case == -1:
            print("No intersections.")
        else:
            baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)

    # One 2D intersection
    elif case == 1:
        # 2D intersection coordinates (due to quadratic equation treating line as infinite, only 1 pair is correct)
        x1 = (-b + Decimal(math.sqrt(discriminant))) / (2 * a)
        x2 = (-b - Decimal(math.sqrt(discriminant))) / (2 * a)
        y1 = lineSlope * x1 + yIntercept
        y2 = lineSlope * x2 + yIntercept

        # Checking if the first pair of coordinates is actually on the line
        if (lineX1 <= x1 <= lineX2 or lineX1 >= x1 >= lineX2) and (lineY1 <= y1 <= lineY2 or lineY1 >= y1 >= lineY2):
            # Computing intersection z-coordinate using parametric form of a line
            scalar = parameterize(lineX1, x1, xvector)
            z1 = lineZ1 + scalar * zvector

            # Check for base perimeter or lateral surface intersection
            if cyliMaxZ >= z1 >= cyliMinZ:
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, z1))
                # Check for base intersection
                baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)
            # Check if z-coordinate is outside the cylinder
            elif z1 > cyliMaxZ or z1 < cyliMinZ:
                if not baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector):
                    print("No intersection.")

        # Checking if the second pair of coordinates is actually on the line
        elif (lineX1 <= x2 <= lineX2 or lineX1 >= x2 >= lineX2) and (lineY1 <= y2 <= lineY2 or lineY1 >= y2 >= lineY2):
            # Computing intersection z-coordinate using parametric form of a line
            scalar = parameterize(lineX1, x2, xvector)
            z2 = lineZ1 + scalar * zvector

            # Check for base perimeter or lateral surface intersection
            if cyliMaxZ >= z2 >= cyliMinZ:
                print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x2, y2, z2))
                # Check for base intersection
                baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)
            # Check if z-coordinate is outside the cylinder
            elif z2 > cyliMaxZ or z2 < cyliMinZ:
                if not baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector):
                    print("No intersection.")

    # Two 2D intersections
    else:
        # 2D intersection coordinates
        x1 = (-b + Decimal(math.sqrt(discriminant))) / (2 * a)
        x2 = (-b - Decimal(math.sqrt(discriminant))) / (2 * a)
        y1 = lineSlope * x1 + yIntercept
        y2 = lineSlope * x2 + yIntercept

        # Computing intersection z-coordinates using parametric form of a line
        scalar1 = parameterize(lineX1, x1, xvector)
        scalar2 = parameterize(lineX1, x2, xvector)
        z1 = lineZ1 + scalar1 * zvector
        z2 = lineZ1 + scalar2 * zvector

        # Check for intersection with base perimeter twice, lateral surface twice, or once each
        if cyliMaxZ >= z1 >= cyliMinZ and cyliMaxZ >= z2 >= cyliMinZ:
            print("Two intersections: ({:.3f},{:.3f},{:.3f}) and ({:.3f},{:.3f},{:.3f})".format(x1, y1, z1, x2, y2, z2))
        # Check for intersection with base twice
        elif z1 > cyliMaxZ and z2 < cyliMinZ or z2 > cyliMaxZ and z1 < cyliMinZ:
            # Check for base intersection
            baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)
        # Check for intersection with either base and either the lateral surface or other base perimeter
        elif z2 > cyliMaxZ >= z1 >= cyliMinZ or z2 < cyliMinZ <= z1 <= cyliMaxZ:
            print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x1, y1, z1))
            # Check for base intersection
            baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)
        # Check for intersection with either base and either the lateral surface or other base perimeter
        elif z1 > cyliMaxZ >= z2 >= cyliMinZ or z1 < cyliMinZ <= z2 <= cyliMaxZ:
            print("One intersection: ({:.3f},{:.3f},{:.3f})".format(x2, y2, z2))
            # Check for base intersection
            baseintersection(lineX1, lineY1, lineZ1, lineZ2, cyliMaxZ, cyliMinZ, xvector, yvector, zvector)
        else:
            print("No intersections.")


# Program start
print("Hi, please separate multiple inputs with commas as shown: input1,input2,input3 etc.")

while not inputComplete:
    selectedShape = input("\nCalculate line intersection with circle or cylinder: ")
    # Circle option
    if selectedShape.strip().lower() == "circle":
        while not validCircle:
            try:
                circX, circY, circR = input("\nEnter center coordinates and radius: ").split(",")

                if not (isvalid(circX) and isvalid(circY) and isvalid(circR)):
                    print("Incorrect input. Please only enter integer or decimal values.")
                    continue
                # Converting string inputs to decimal
                circX = Decimal(circX)
                circY = Decimal(circY)
                circR = Decimal(circR)

                validCircle = True
            except ValueError:
                print("Incorrect number of arguments. Please try again.")

        while not validLine:
            try:
                lineX1, lineY1, lineX2, lineY2 = input("\nEnter line coordinates in order of x1,y1,x2,y2: ").split(",")

                if not (isvalid(lineX1) and isvalid(lineY1) and isvalid(lineX2) and isvalid(lineY2)):
                    print("Incorrect input. Please only enter integer or decimal values.")
                    continue
                elif lineX1 == lineX2 and lineY1 == lineY2:
                    print("Error. A point cannot be entered twice.")
                    continue
                elif lineX1 == lineX2:
                    print("Error. A function cannot map one x-coordinate to two different y-coordinates.")
                    continue
                # Converting string inputs to decimal
                lineX1 = Decimal(lineX1)
                lineY1 = Decimal(lineY1)
                lineX2 = Decimal(lineX2)
                lineY2 = Decimal(lineY2)

                validLine = True
            except ValueError:
                print("Incorrect number of arguments. Please try again.")
        # Print result of intersections
        intersect2d(lineX1, lineY1, lineX2, lineY2, circX, circY, circR)

        inputComplete = True

    # Cylinder option
    elif selectedShape.strip().lower() == "cylinder":
        while not validCylinder:
            try:
                cyliX, cyliY, cyliZ, cyliR, cyliH = input("\nEnter center coordinates, radius, and height: ").split(",")

                if not (isvalid(cyliX) and isvalid(cyliY) and isvalid(cyliZ) and isvalid(cyliR) and isvalid(cyliH)):
                    print("Incorrect input. Please only enter integer or decimal values.")
                    continue
                # Converting string inputs to decimal
                cyliX = Decimal(cyliX)
                cyliY = Decimal(cyliY)
                cyliZ = Decimal(cyliZ)
                cyliR = Decimal(cyliR)
                cyliH = Decimal(cyliH)

                validCylinder = True
            except ValueError:
                print("Incorrect number of arguments.")

        while not validLine:
            try:
                lineX1, lineY1, lineZ1, lineX2, lineY2, lineZ2 = input("\nEnter line coordinates in order of x1,y1,z1,"
                                                                       "x2,y2,z2: ").split(",")

                if not (isvalid(lineX1) and isvalid(lineY1) and isvalid(lineZ1) and isvalid(lineX2) and isvalid(lineY2)
                        and isvalid(lineZ2)):
                    print("Incorrect input. Please only enter integer or decimal values.")
                elif lineX1 == lineX2 and lineY1 == lineY2 and lineZ1 == lineZ2:
                    print("Error. A point cannot be entered twice.")
                    continue
                elif lineX1 == lineX2 and lineY1 == lineY2:
                    print("Error. Vertical line along z-axis not allowed.")
                    continue
                elif lineX1 == lineX2:
                    print("Error. Line cannot have same x-coordinate.")
                    continue
                # Converting string inputs to decimal
                lineX1 = Decimal(lineX1)
                lineY1 = Decimal(lineY1)
                lineZ1 = Decimal(lineZ1)
                lineX2 = Decimal(lineX2)
                lineY2 = Decimal(lineY2)
                lineZ2 = Decimal(lineZ2)

                validLine = True
            except ValueError:
                print("Incorrect number of arguments.")
        # Print result of intersections
        intersect3d(lineX1, lineY1, lineZ1, lineX2, lineY2, lineZ2, cyliX, cyliY, cyliZ, cyliR, cyliH)

        inputComplete = True
    else:
        print("Incorrect input. Please enter either circle or cylinder.\n")
        continue
