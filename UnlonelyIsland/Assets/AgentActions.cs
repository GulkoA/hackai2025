using System.Collections;
using UnityEngine;
using UnityEngine.AI;

public class AgentActions : MonoBehaviour
{
    [SerializeField] private Animator animator;
    public void InterpretData(string command, string parameters)
    {
        NavMeshAgent agent = GetComponent<NavMeshAgent>();
        if (command.Equals("start_walk"))
        {
            switch (parameters)
            {
                case "housing":
                    agent.SetDestination(new Vector3(2.48f, 4.28f, -9.53f));
                    break;
                case "market":
                    agent.SetDestination(new Vector3(-17.03f, 8.09f, -10.14f));
                    break;
                case "farm":
                    agent.SetDestination(new Vector3(26.37f, 4.21f, 22.57f));
                    break;
                case "dock":
                    agent.SetDestination(new Vector3(-47.63f, 3.32f, -10.69f));
                    break;
                default: break;
            }
        }
        else if (command.Equals("start_action"))
        {
            switch (parameters)
            {
                case "fishing":
                    StartCoroutine(startAction(3, "tPerform", parameters));
                    break;
                case "farming":
                    StartCoroutine(startAction(3, "tPerform", parameters));
                    break;
                case "cooking":
                    StartCoroutine(startAction(3, "tPerform", parameters));
                    break;
                default: break;
            }
        }
        else if (command.Equals("start_conversation"))
        {
            CharacterDialogue cd = GetComponent<CharacterDialogue>();
            cd.UpdateDialogue(parameters);
        }
        else if (command.Equals("say_in_conversation"))
        {
            CharacterDialogue cd = GetComponent<CharacterDialogue>();
            cd.UpdateDialogue(parameters);
        }
    }
    private void OnTriggerEnter(Collider other)
    {
        //if (other.tag == "Farm" || other.tag == "House" || other.tag == "Market" || other.tag == "Dock")
        //{
        //    StartCoroutine(startAction(4f, "tPerform", other.tag));
        //}
    }
    private void OnTriggerExit(Collider other)
    {
        // not needed for now
    }
    private IEnumerator startAction(float actionTime, string animationName, string taskName = null)
    {
        if (taskName is not null)
        {
            Debug.Log(taskName + " task started.");
        }
        else
        {
            Debug.Log("Task started.");
        }
        animator.SetTrigger(animationName);
        yield return new WaitForSeconds(actionTime);
        animator.SetTrigger("tIdle");
        if (taskName is not null)
        {
            Debug.Log(taskName + " task ended.");
        }
        else
        {
            Debug.Log("Task ended.");
        }
    }
}
