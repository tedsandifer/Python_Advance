"""
content = assignment
course  = Python Advanced
 
date    = 16.02.2026
email   = tedsandifer@gmail.com
"""

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""


class Object:

   def __init__(self, name):
      self.name = name
      self.color = [.5, .5, .5]
      self.trans = [0, 0, 0]
      self.rot = [0, 0, 0]
      self.scale = [1, 1, 1]
      
   # simple print to confirm new object and parameters
   def print_status(self):
      print(f"{self.name} created"
         f"\nColor: {self.color}"
         f"\nTranslation: {self.trans}"
         f"\nRotation: {self.rot}"
         f"\nScale: {self.scale}")

   # object modification functions
   def object_translate(self, value_x, value_y, value_z):
      self.trans = [value_x, value_y, value_z]
      print(f"{self.name} has been translated to: {self.trans}")

   def object_rotate(self, value_x, value_y, value_z):
      self.rot = [value_x, value_y, value_z]
      print(f"{self.name} has been rotated: {self.rot}")

   def object_scale(self, value_x, value_y, value_z):
      self.scale = [value_x, value_y, value_z]
      print(f"{self.name} has been scaled to: {self.scale}")

   def object_color(self, value_x, value_y, value_z):
      self.color = [value_x, value_y, value_z]
      print(f"{self.name}'s color has been changed to: {self.color}")



   def update_transform(self, ttype, value):
      """this function updates the objects"""

      value_list = value.split(',')
      value_x = float(value_list[0].strip())
      value_y = float(value_list[1].strip())
      value_z = float(value_list[2].strip())


      transform_funcs = {
         'translate' : self.object_translate,
         'rotate' : self.object_rotate,
         'scale' : self.object_scale,
         'color' : self.object_color,
      }
 
      transform_funcs[ttype](value_x, value_y, value_z)

      
class Cube(Object):

   def __init__(self, name):
      super().__init__(name)




my_object = Object("ted's cube")
my_object.print_status()

my_object.update_transform("color", "7,5,6")

new_cube = Cube("new_cube")
new_cube.print_status()
new_cube.update_transform('rotate', '8, 1.5, .5')