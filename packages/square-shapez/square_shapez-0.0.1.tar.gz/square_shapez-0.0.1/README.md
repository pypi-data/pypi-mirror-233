# Shapes square library #

## What is this? ##
The module allows you to work with shapes, calculate perimetr and area.

### Using ###


Using the library is as simple and convenient as possible:

Let's import it first:\
First, import everything from the library (use the `from `...` import *` construct).

Examples of all operations:

Create circle shape, using `radius`:

    circle = Circle(radius=radius)

Create triangle shape, using `side_1`, `side_2`, `side_3`:

    triangle = Triangle(a=side_1, b=side_2, c=side_3)


You can calculate perimetr for each shape, `using get_perimetr()`:

    shape_perimetr = shape.get_perimetr()

You can calculate are for each shape, `using get_area()`:

    shape_area = shape.get_area()

Also, you can use `calculate_area()` which takes as input a parameter of type Shape (an abstract class for all shapes)

    shape_area = calculate_area(shape=some_shape)