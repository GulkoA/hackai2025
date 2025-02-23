using System.Collections;
using UnityEngine;

public class AgentActions : MonoBehaviour
{
    [SerializeField] private Animator animator;
    public void InterpretData(string data)
    {

    }
    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Farm" || other.tag == "House" || other.tag == "Market" || other.tag == "Dock")
        {
            StartCoroutine(startAction(4f, "tPerform", other.tag));
        }
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
