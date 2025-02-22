using UnityEngine;
using UnityEngine.AI;

public class DebugClickToMove : MonoBehaviour
{
    //Used for choices 1, 2, 3 in pathfinding.
    private Vector3 housingArea;
    private Vector3 market;
    private Vector3 dock;

    private NavMeshAgent agent;
    [SerializeField] private Animator animator;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();

        //1, 2, 3, for housing, shopping, hill options to raycast to.
        housingArea = new Vector3(407.20f, 248.40f, 0.00f);
        market = new Vector3(536.00f, 370.80f, 0.00f);
        dock = new Vector3(836.00f, 382.00f, 0.00f);
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
                animator.SetTrigger("tWalk");
            }
        }
        if (!agent.pathPending && agent.remainingDistance <= agent.stoppingDistance)
        {
            if (!agent.hasPath || agent.velocity.sqrMagnitude == 0f)
            {
                animator.SetTrigger("tIdle");
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
