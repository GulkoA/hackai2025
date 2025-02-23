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

    private void OnEnable()
    {
        // Subscribe to the AgentInventory event
        AgentInventory.OnJsonPublished += HandleJsonPublished;
    }

    private void OnDisable()
    {
        // Unsubscribe to avoid memory leaks
        AgentInventory.OnJsonPublished -= HandleJsonPublished;
    }

    // Event handler to receive the JSON string
    private void HandleJsonPublished(string jsonData)
    {
        Debug.Log($"AgentManager received JSON: {jsonData}");

        DistributeToAgent(0, "UpdateInventory", jsonData);
    }

    public void DistributeToAgent(int id, string command, string parameters)
    {
        if (id < agentArray.Length)
        {
            Debug.Log("Distributing data to agent...");
            MainThreadDispatcher.Enqueue(() =>
            {
                AgentActions aa = agentArray[id].GetComponent<AgentActions>();
                if (aa != null)
                {
                    Debug.Log("Interpreting data...");
                    aa.InterpretData(command, parameters);  // Pass the JSON string as parameters
                }
                else
                {
                    Debug.LogError($"No AgentActions found on Agent ID: {id}");
                }
            });
        }
        else
        {
            Debug.LogError($"Agent ID {id} is out of range.");
        }
    }
}
