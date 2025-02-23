using UnityEngine;
using UnityEngine.AI;

public class DebugClickToMove : MonoBehaviour
{
    //Used for choices 1, 2, 3 in pathfinding.
    private Vector3 housingArea;
    private Vector3 market;
    private Vector3 dock;

    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();

        //1, 2, 3, for housing, shopping, hill options to raycast to.
        housingArea = new Vector3(2.48f, 4.28f, -9.53f);
        market = new Vector3(-17.03f, 8.09f, -10.14f);
        dock = new Vector3(-47.63f, 3.32f, -10.69f);
    }

    void Update()
    {

        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            agent.SetDestination(housingArea);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            agent.SetDestination(market);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            agent.SetDestination(dock);
        }


    }
}