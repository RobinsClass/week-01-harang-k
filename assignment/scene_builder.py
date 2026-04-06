"""
DIGM 131 - Assignment 1: Procedural Scene Builder
==================================================

OBJECTIVE:
    Build a simple 3D scene in Maya using Python scripting.
    You will practice using maya.cmds to create and position geometry,
    and learn to use descriptive variable names.

REQUIREMENTS:
    1. Create a ground plane (a large, flat polygon plane).
    2. Create at least 5 objects in your scene.
    3. Use at least 2 different primitive types (e.g., cubes AND spheres,
       or cylinders AND cones, etc.).
    4. Position every object using descriptive variable names
       (e.g., house_x, tree_height -- NOT x1, h).
    5. Add comments explaining what each section of your code does.

GRADING CRITERIA:
    - [20%] Ground plane is created and scaled appropriately.
    - [30%] At least 5 objects are created using at least 2 primitive types.
    - [25%] All positions/sizes use descriptive variable names.
    - [15%] Code is commented clearly and thoroughly.
    - [10%] Scene is visually coherent (objects are placed intentionally,
            not overlapping randomly).

TIPS:
    - Run this script from Maya's Script Editor (Python tab).
    - Use maya.cmds.polyCube(), maya.cmds.polySphere(), maya.cmds.polyCylinder(),
      maya.cmds.polyCone(), maya.cmds.polyPlane(), etc.
    - Use maya.cmds.move(x, y, z, objectName) to position objects.
    - Use maya.cmds.scale(x, y, z, objectName) to resize objects.
    - Use maya.cmds.rename(oldName, newName) to give objects meaningful names.
"""

import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Clear the scene so we start fresh each time the script runs.
# (This is provided for you -- do not remove.)
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)

# ---------------------------------------------------------------------------
# Ground Plane
# ---------------------------------------------------------------------------
# Descriptive variables for the ground plane dimensions and position.
ground_width = 30
ground_depth = 30
ground_y_position = 0

ground = cmds.polyPlane(
    name="ground_plane",
    width=ground_width,
    height=ground_depth,
    subdivisionsX=1,
    subdivisionsY=1,
)[0]
cmds.move(0, ground_y_position, 0, ground)

# Give the ground a sand color using a Lambert shader
ground_shader = cmds.shadingNode("lambert", asShader=True, name="groundMat")
cmds.setAttr(ground_shader + ".color", 0.5, 0.45, 0.35, type="double3")
cmds.select(ground)
cmds.hyperShade(assign=ground_shader)

# ---------------------------------------------------------------------------
# Object 1 - Stepped Pyramid
# ---------------------------------------------------------------------------
pyramidStep_count = 9          # how many steps of the pyramid
pyramidStep_base = 10           # how wide the first step is
pyramidStep_height = 0.4       # how tall each step is
pyramidStep_scale = 1        # how small each step is compared to the one below
cmds.group( em=True, name='Pyramid' )

for i in range(pyramidStep_count):
    pyramidStep_name = f"pyramidStep_{i+1}"
    pyramidStep_size = pyramidStep_base - (pyramidStep_scale * (i+1))
    cmds.polyCube(name=pyramidStep_name,
                  width=pyramidStep_size,
                  height=pyramidStep_height,
                  depth=pyramidStep_size)

    # Position
    pyramidStep_x = 0
    pyramidStep_y = pyramidStep_height * (i + 1)   # each step is stacked on the one below
    pyramidStep_z = 0

    cmds.move(pyramidStep_x, pyramidStep_y - (pyramidStep_height/2), pyramidStep_z, pyramidStep_name)

    # Color gradient: dark at bottom, light at top
    ps_fraction = i / pyramidStep_count
    ps_shader_name = f"pyramidStepMat_{i}"
    pyramid_Shader = cmds.shadingNode("lambert", asShader=True, name=ps_shader_name)
    cmds.setAttr(f"{ps_shader_name}.color",
                 0.25 + 0.25 * ps_fraction,    # red:   dark -> bright
                 0.18 + 0.25 * ps_fraction,    # green: slight shift
                 0.1 + 0.25 * ps_fraction,    # blue:  cool -> warm
                 type="double3")
    cmds.select(pyramidStep_name)
    cmds.hyperShade(assign=pyramid_Shader)
    # Group the Pyramid
    cmds.parent( pyramidStep_name, 'Pyramid' )

cmds.move(-5, 0, -5, 'Pyramid')
cmds.scale( 1.5, 1.5, 1.5, 'Pyramid' )

# ---------------------------------------------------------------------------
# Object 2 - Temple
# ---------------------------------------------------------------------------
column_count = 4
column_height = 2
column_radius = 0.2
column_distance = 0.8
column_row = 3

cmds.group( em=True, name='Temple')
for i in range(column_row):

    row_name = f"row_{i+1}"
    cmds.group( em=True, name=row_name)

    for j in range(column_count):
        column_name = f"column_{j+1+(4*i)}"

        cmds.polyCylinder(name=column_name,
                            radius=column_radius,
                            height=column_height)
            
        # Position
        column_x = column_distance * (j)
        column_y = column_height / 2
        column_z = 0
            
        cmds.move(column_x, column_y, column_z, column_name)

        # Group the columns
        cmds.parent( column_name, row_name)

    # Top plate
    plate_name = f"plate_{i+1}"
    cmds.polyCube(name=plate_name,
                width=(column_distance) * column_count,
                height=column_radius,
                depth=column_radius * 4)

    plate_x = column_distance * column_count/2 - column_distance/2
    plate_y = column_height
    plate_z = 0

    cmds.move(plate_x, plate_y, plate_z)
    cmds.parent(plate_name, row_name)

    # Row Position
    row_x = 0
    row_y = 0
    row_z = column_distance * (i+1)

    cmds.move(row_x, row_y, row_z, row_name)
    cmds.parent(row_name, 'Temple')

cmds.move(4, 0, 6, 'Temple')

sand_shader = cmds.shadingNode("lambert", asShader=True, name="sandMat")
cmds.setAttr(sand_shader + ".color", 0.3, 0.25, 0.2, type="double3")
cmds.select('Temple')
cmds.hyperShade(assign=sand_shader)

  

# ---------------------------------------------------------------------------
# Object 3 - House 1
# ---------------------------------------------------------------------------
house1_width = 2
house1_height = 1
house1_depth = 2
house1_x = 8.5
house1_z = -3.5

house_1 = cmds.polyCube(name="house_1",
                           width=house1_width,
                           height=house1_height,
                           depth=house1_depth)[0]
cmds.move(house1_x, house1_height / 2.0, house1_z, house_1)

cmds.select('house_1')
cmds.hyperShade(assign=sand_shader)

# ---------------------------------------------------------------------------
# Object 4 - House 2
# ---------------------------------------------------------------------------
house2_width = 1
house2_height = 1
house2_depth = 2.5
house2_x = 12
house2_z = 0

house_2 = cmds.polyCube(name="house_2",
                           width=house2_width,
                           height=house2_height,
                           depth=house2_depth)[0]
cmds.move(house2_x, house2_height / 2.0, house2_z, house_2)

cmds.select('house_2')
cmds.hyperShade(assign=sand_shader)

# ---------------------------------------------------------------------------
# Object 5 - House 3
# ---------------------------------------------------------------------------
house3_width = 1.5
house3_height = 1
house3_depth = 1.2
house3_x = 8
house3_z = 2

house_3 = cmds.polyCube(name="house_3",
                           width=house3_width,
                           height=house3_height,
                           depth=house3_depth)[0]
cmds.move(house3_x, house3_height / 2.0, house3_z, house_3)

cmds.select('house_3')
cmds.hyperShade(assign=sand_shader)

# ---------------------------------------------------------------------------
# Object 6 - Wall
# ---------------------------------------------------------------------------
wall_depth = 0.5
wall_height = 1
area_width = 11
area_depth = 20

# Walls for the width
wall_1 = cmds.polyCube(n= 'wall_1', w=area_width, h=wall_height, d=wall_depth, )
cmds.duplicate('wall_1')
cmds.move(0, wall_height/2, -area_depth/2, 'wall_1')
cmds.move(0, wall_height/2, area_depth/2, 'wall_2')

# Walls for the depth
wall_3 = cmds.polyCube(n= 'wall_3', w=wall_depth, h=wall_height, d=area_depth)
cmds.duplicate( 'wall_3')

cmds.move(-area_width/2+wall_depth/2, wall_height/2, 0, 'wall_3' )
cmds.move(area_width/2-wall_depth/2, wall_height/2, 0, 'wall_4')

# Group walls
cmds.group('wall_1', 'wall_2', 'wall_3', 'wall_4', n='Wall')
cmds.move(8.1, 0, 1, 'Wall')

cmds.select('Wall')
cmds.hyperShade(assign=sand_shader)

# ---------------------------------------------------------------------------
# Frame All -- so the whole scene is visible in the viewport.
# (This is provided for you -- do not remove.)
# ---------------------------------------------------------------------------
cmds.viewFit(allObjects=True)
print("Scene built successfully!")
