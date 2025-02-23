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
    public void DistributeToAgent(string data, int id)
    {
        if (id < agentArray.Length)
        {
            AgentActions aa = agentArray[id].GetComponent<AgentActions>();
            if (aa is not null)
            {
                aa.InterpretData(data);
            }
        }
    }
}
