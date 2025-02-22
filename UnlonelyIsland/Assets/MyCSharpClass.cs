// using UnityEngine;
// using UnityEditor.Scripting.Python;

// public class MyCSharpClass : MonoBehaviour
// {
//     // Make this method public (does not need to be static)
//     public void PrintMessage()
//     {
//         Debug.Log("Message from Python: ");
//     }

//     // void Start()
//     // {
//     //     // Call the Python script
//     //     PythonRunner.RunFile("Assets/hello.py");
//     // }
// }


using UnityEngine;
using UnityEditor;
using UnityEditor.Scripting.Python;
using System.IO;

public class Menu_Item_Hello_Class : MonoBehaviour
{
    void Start()
    {
        // Path to the Python script
        string scriptPath = "Assets/hello.py";

        // Run the Python script
        PythonRunner.RunFile(scriptPath);

        // Path to the temporary result file
        string resultFilePath = "output.txt";

        // Wait for the file to be written
        if (File.Exists(resultFilePath))
        {
            // Read the result from the file
            string result = File.ReadAllText(resultFilePath);
            Debug.Log("Python output: " + result);
        }
        else
        {
            Debug.LogError("Result file not found. Ensure the Python script runs correctly.");
        }
    }
    public void MyCSharpMethod() {
        Debug.Log("Hello!");
    }
}
