import UnityEngine
from UnityEngine import Debug, GameObject


def walk():
  # Find all GameObjects in the scene
  all_objects = UnityEngine.Object.FindObjectsOfType(UnityEngine.GameObject)
  for go in all_objects:

    # Check if the object is named 'some guy_'
    if go.name == "some guy":
      # Get the NavMeshAgent component
      agent = go.GetComponent(UnityEngine.AI.NavMeshAgent)
      if agent:
        Debug.Log("NavMeshAgent found. Starting movement...")

        # Initial position and movement increment
        position_y = go.transform.position.y
        Debug.Log(f"Agent's position: {position_y}")
        move_increment = 10  # Distance to move per step
        steps = 10  # Number of steps

        # Move the agent up incrementally
        for _ in range(steps):
          move_increment += 10
          target_position = UnityEngine.Vector3(go.transform.position.x - 30, position_y, go.transform.position.z)

          # Set the destination
          agent.SetDestination(target_position)

          # Log the position change
          Debug.Log(f"Moving 'some guy' to position: {target_position}")

          # Wait for the next frame
          UnityEngine.YieldInstruction()
      else:
        Debug.Log("No NavMeshAgent found on 'some guy'")

walk()
