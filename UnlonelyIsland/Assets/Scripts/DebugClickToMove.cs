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
        housingArea = new Vector3(4.15f, 4.28f, -8.94f);
        market = new Vector3(-17.50f, 8.09f, -9.73f);
        dock = new Vector3(-46.64f, 3.33f, -11.94f);
    }

    void Update()
    {
        Ray ray;
        RaycastHit hit;

        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            ray = Camera.main.ScreenPointToRay(housingArea);
            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point);
                Debug.Log("Hit! "+ hit.point);
            }
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            ray = Camera.main.ScreenPointToRay(market);
            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point);
            }
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            ray = Camera.main.ScreenPointToRay(dock);
            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point);
            }
        }

        
    }
}
