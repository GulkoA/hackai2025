using UnityEngine;

public class AgentInventory : MonoBehaviour
{
    public int NumFish { get; set; }
    public int NumTomatoes { get; set; }
    public int NumMeals { get; set; }
    public int NumGold { get; set; }


    public int Vitals { get; set; }
    public int Stamina {  get; set; }

    public string Occupation { get; set; }
    public string Location { get; set; }
    public int[] Agents {  get; set; }
    public bool[] ActionIndex { get; set; }
    // 1: fishing
    // 2: farming
    // 3: cooking

    private void Start()
    {
        ActionIndex = new bool[3];
    }
}
