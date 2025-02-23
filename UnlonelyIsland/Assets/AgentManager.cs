using UnityEngine;

public class AgentManager : MonoBehaviour
{
    public static AgentManager Instance { get; private set; }
    [SerializeField] private GameObject[] agentArray;
    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    public void DistributeToAgent(int id, string command, string parameters)
    {
        if (id < agentArray.Length)
        {
            Debug.Log("distributing data");
            MainThreadDispatcher.Enqueue(() =>
            {
                AgentActions aa = agentArray[id].GetComponent<AgentActions>();
                if (aa != null)
                {
                    Debug.Log("interpreting data");
                    aa.InterpretData(command, parameters);
                }
            });

        }
    }
}
