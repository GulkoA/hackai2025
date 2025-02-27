using UnityEngine;

public class NetworkDebugger : MonoBehaviour
{
    public void SendDebug()
    {
        UnityEngine.Debug.Log("Sending new message via DEBUG.");
        NetworkManager.Instance.SendAction("this is a test");
    }
}
