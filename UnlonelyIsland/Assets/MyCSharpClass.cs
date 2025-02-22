using UnityEditor.Scripting.Python;
using UnityEditor;
using UnityEngine;

public class Menu_Item_Hello_Class : MonoBehaviour
{
    // [MenuItem("MyPythonScripts/Ensure Naming")]
    // static void RunEnsureNaming()
    void Start()
    {
        PythonRunner.RunFile($"{Application.dataPath}/ensure_naming.py");
    }
}
