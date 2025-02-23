using System;
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
                    StartCoroutine(startAction(10, "tPerform", parameters));
                    break;
                case "farming":
                    StartCoroutine(startAction(10, "tPerform", parameters));
                    break;
                case "cooking":
                    StartCoroutine(startAction(10, "tPerform", parameters));
                    break;
                case "eating":
                    StartCoroutine(startAction(10, "tPerform", parameters));
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
        animator.SetTrigger(animationName);
        AgentInventory ai = GetComponent<AgentInventory>();
        yield return new WaitForSeconds(actionTime);
        switch (taskName)
            {
                case "fishing":
                    ai.NumFish += UnityEngine.Random.Range(1, 11);
                    break;
                case "farming":
                    ai.NumTomatoes += UnityEngine.Random.Range(1, 11);
                    break;
                case "cooking":
                    int remove = Mathf.Min(ai.NumTomatoes, ai.NumFish, 5);
                    ai.NumMeals += remove;
                    ai.NumFish -= remove;
                    ai.NumTomatoes -= remove;
                    break;
                case "eating":
                    ai.NumMeals--;
                    ai.Vitals -= UnityEngine.Random.Range(2, 9);
                    ai.Vitals = Mathf.Clamp(ai.Vitals, 0 , 10);
                    break;
                default: break;
            }
        animator.SetTrigger("tIdle");
        ai.packageJson();
    }
}
