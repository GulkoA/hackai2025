using UnityEngine;
using UnityEngine.AI;

public class DebugClickToMove : MonoBehaviour
{
    //Used for choices 1, 2, 3 in pathfinding.
    private Vector3 housingArea = new Vector3();
    private Vector3 shoppingArea = new Vector3();
    private Vector3 mountainArea = new Vector3();

    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        //change this to a 1, 2, 3, for housing, shopping, hill.
        //store each as a location vector3.
        out hit = null;

        switch (Input.getMouseButton())
        {
            case 1: //go to housing
                Ray ray = Camera.main.ScreenPointToRay(housingArea);
                Physics.Raycast(ray, out hit);
                break;
            case 2: //go to shopping area
                Ray ray = Camera.main.ScreenPointToRay(shoppingArea);
                Physics.Raycast(ray, out hit);
                break;
            case 3: //go to the mountain
                Ray ray = Camera.main.ScreenPointToRay(mountainArea);
                Physics.Raycast(ray, out hit);
                break;
            default:
                break;
        }
        if (hit != null) {
            agent.SetDestination(hit.point);
        }
    }
}
