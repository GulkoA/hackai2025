using UnityEngine;

public class NetworkDebugger : MonoBehaviour
{
    public void SendDebug()
    {
        UnityEngine.Debug.Log("Sending new message via DEBUG.");
        NetworkManager.Instance.SendAction("{\"id\": 0, \"command\": \"prompt_agent_action\", \"parameters\": {\"ctx\": {\"AgentID\": -1, \"NumFish\": 0, \"NumTomatoes\": 0, \"NumMeals\": 0, \"NumGold\": 0, \"Vitals\": 5, \"Stamina\": 5, \"Occupation\": \"\", \"Location\": \"\", \"Agents\": [], \"ActionIndex\": []}}}");
    }
}
