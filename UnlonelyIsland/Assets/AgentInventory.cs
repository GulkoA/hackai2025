using UnityEngine;
using System;

public class AgentInventory : MonoBehaviour
{
    // Event to publish JSON data to all subscribers
    public static event Action<string> OnJsonPublished;

    public int NumFish { get; set; }
    public int NumTomatoes { get; set; }
    public int NumMeals { get; set; }
    public int NumGold { get; set; }

    public int Vitals { get; set; }
    public int Stamina { get; set; }

    public string Occupation { get; set; }
    public string Location { get; set; }
    public int[] Agents { get; set; }
    public bool[] ActionIndex { get; set; }
    // 1: fishing
    // 2: farming
    // 3: cooking

    private void Start()
    {
        ActionIndex = new bool[3];
    }

    public string packageJson()
    {
        // Use an anonymous object or a serializable class to package the data
        var jsonObject = new
        {
            NumFish = this.NumFish,
            NumTomatoes = this.NumTomatoes,
            NumMeals = this.NumMeals,
            NumGold = this.NumGold,
            Vitals = this.Vitals,
            Stamina = this.Stamina,
            Occupation = this.Occupation,
            Location = this.Location,
            Agents = this.Agents,
            ActionIndex = this.ActionIndex
        };

        // Convert the object to JSON string
        string jsonString = JsonUtility.ToJson(jsonObject, true);
        Debug.Log($"Packaged JSON: {jsonString}");

        // Publish the JSON to all subscribers
        OnJsonPublished?.Invoke(jsonString);

        return jsonString;
    }
}
