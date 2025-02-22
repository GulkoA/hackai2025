import UnityEngine
from UnityEngine import Debug

# Find all GameObjects in the scene
all_objects = UnityEngine.Object.FindObjectsOfType(UnityEngine.GameObject)

# Path for output file
file_path = 'output.txt'

# Open the file in write mode
with open(file_path, "w") as file:
  for go in all_objects:
    # Print the current GameObject's name
    print(go.name)
    
    # Write the name to the file
    file.write(go.name + "\n")
    
    # If the GameObject's name doesn't end with '_', append '_'
    if go.name[-1] != '_':
      go.name = go.name + '_'
    
    # Check if the object is named 'Cube_'
    if go.name == 'Cube_':
      # Change the color of the Cube_ object to red
      renderer = go.GetComponent(UnityEngine.Renderer)
      if renderer:
        renderer.material.color = UnityEngine.Color.red
        Debug.Log("Changed color of Cube_ to red")
    
    # Log the updated name
    Debug.Log(go.name)
