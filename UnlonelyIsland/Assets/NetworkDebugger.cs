using UnityEngine;

public class NetworkDebugger : MonoBehaviour
{
    public void SendDebug()
    {
        UnityEngine.Debug.Log("Sending new message via DEBUG.");
        NetworkManager.Instance.SendAction("{\"id\": 0, \"command\": \"prompt_agent_action\", \"parameters\": { \"ctx\": { \"inventory\": { \"fish\": 10, \"tomatoes\": 0, \"meals\": 0, \"gold\": 0 }, \"vitals\": { \"hunger\": 1, \"stamina\": 5 }, \"location\": \"market\", \"agents_nearby\": [], \"actions_available\": [] } } }");
    }
}
