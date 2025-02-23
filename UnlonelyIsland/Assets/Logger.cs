using System;
using System.IO;
using UnityEngine;

public class Logger : MonoBehaviour
{
    private static string logFilePath;

    void Awake()
    {
        logFilePath = Application.persistentDataPath + "/game_log.txt";
        Application.logMessageReceived += HandleLog;
    }

    void OnDestroy()
    {
        Application.logMessageReceived -= HandleLog;
    }

    private void HandleLog(string logString, string stackTrace, LogType type)
    {
        string logMessage = $"{DateTime.Now}: {type} - {logString}\n{stackTrace}\n";
        File.AppendAllText(logFilePath, logMessage);
    }
}