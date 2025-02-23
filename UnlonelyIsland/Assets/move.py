import UnityEngine
from UnityEngine import Debug
from System import Type

# Find all GameObjects in the scene
all_objects = UnityEngine.Object.FindObjectsOfType(UnityEngine.GameObject)

for go in all_objects:
  # Check for GameObject named 'testScript'
  if go.name == "testScript":
    Debug.Log(f"Found GameObject: {go.name}")

    # Use GetComponent with Type.GetType to get the script
    component_type = Type.GetType("samplescript, Assembly-CSharp")
    if component_type:
      sample_script = go.GetComponent(component_type)
      
      if sample_script:
        Debug.Log("Samplescript component found.")

        # Call the method using Invoke
        sample_script.SendMessage("TestTheScript")
      else:
        Debug.Log("Samplescript component not found on 'testScript' GameObject.")
    else:
      Debug.Log("Type 'Samplescript' not found.")

  # if go.name == "testScript":
  #   Debug.Log(f"Found GameObject: {go.name}")

  #   # Use the type-safe method to get the component
  #   sample_script = go.GetComponent[UnityEngine.MonoBehaviour]()

  #   # Check if the component is found and call the method via reflection
  #   if sample_script:
  #     # Use reflection to invoke the method
  #     method = sample_script.GetType().GetMethod("TestTheScript")
  #     if method:
  #       method.Invoke(sample_script, None)
  #     else:
  #       Debug.Log("Method 'TestTheScript' not found.")
  #   else:
  #     Debug.Log("Samplescript component not found on 'testScript' GameObject.")
  
  # Check if the object is named 'some guy'
  if go.name == "some guy":
    # Get the NavMeshAgent component
    agent = go.GetComponent(UnityEngine.AI.NavMeshAgent)
    if agent:
      # Debug.Log("NavMeshAgent found. Starting movement...")

      # Initial position and movement increment
      position_y = go.transform.position.y
      # Debug.Log(f"Agent's initial position: {position_y}")
      move_increment = 10  # Distance to move per step
      steps = 10  # Number of steps

      # Move the agent up incrementally
      for _ in range(steps):
        position_y += move_increment
        target_position = UnityEngine.Vector3(go.transform.position.x - 30, position_y, go.transform.position.z)

        # Set the destination
        agent.SetDestination(target_position)

        # Log the position change
        # Debug.Log(f"Moving 'some guy' to position: {target_position}")
    else:
      Debug.Log("No NavMeshAgent found on 'some guy'.")
