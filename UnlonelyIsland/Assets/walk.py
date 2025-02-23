import UnityEngine
from UnityEngine import Debug, GameObject


def walk(id, destination):
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

        if destination == "housingArea":
          target_position = UnityEngine.Vector3(2.48, 4.28, -9.53)
          agent.SetDestination(target_position)
          Debug.Log(f"Moving 'some guy' to Housing Area at position: {target_position}")

        elif destination == "market":
          target_position = UnityEngine.Vector3(-17.03, 8.09, -10.14)
          agent.SetDestination(target_position)
          Debug.Log(f"Moving 'some guy' to Market at position: {target_position}")

        elif destination == "dock":
          target_position = UnityEngine.Vector3(-47.63, 3.32, -10.69)
          agent.SetDestination(target_position)
          Debug.Log(f"Moving 'some guy' to Dock at position: {target_position}")

        elif destination == "farm":
          target_position = UnityEngine.Vector3(26.37, 4.21, 22.57)
          agent.SetDestination(target_position)
          Debug.Log(f"Moving 'some guy' to Farm at position: {target_position}")

        else:
          Debug.Log("Invalid destination provided.")
      else:
        Debug.Log("No NavMeshAgent found on 'some guy'")

walk(0, "housingArea")
