using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using NUnit.Framework;
using UnityEngine;

public class NetworkManager : MonoBehaviour
{
    public static NetworkManager Instance { get; private set; }
    private Process pythonServerProcess;
    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;

    void Start()
    {
        StartPythonServer();
        ConnectToServer();
    }

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

    void StartPythonServer()
    {
        try
        {
            pythonServerProcess = new Process();
            pythonServerProcess.StartInfo.FileName = "python"; // Update with the full path to your Python executable
            pythonServerProcess.StartInfo.Arguments = Application.streamingAssetsPath + "/Scripts/network.py"; // Update path accordingly
            pythonServerProcess.StartInfo.UseShellExecute = false;
            pythonServerProcess.StartInfo.RedirectStandardOutput = true;
            pythonServerProcess.StartInfo.RedirectStandardError = true;
            pythonServerProcess.StartInfo.CreateNoWindow = true;
            pythonServerProcess.OutputDataReceived += (sender, args) => UnityEngine.Debug.Log("Python Server: " + args.Data);
            pythonServerProcess.ErrorDataReceived += (sender, args) => UnityEngine.Debug.LogError("Python Server Error: " + args.Data);
            pythonServerProcess.Start();
            pythonServerProcess.BeginOutputReadLine();
            pythonServerProcess.BeginErrorReadLine();
            UnityEngine.Debug.Log("Python server started");
        }
        catch (Exception e)
        {
            UnityEngine.Debug.LogError($"Failed to start Python server: {e.Message}");
            Application.Quit();
        }
    }

    void ConnectToServer()
    {
        try
        {
            Thread.Sleep(2000); // Increase the delay to ensure the server has started
            client = new TcpClient("localhost", 12345);
            stream = client.GetStream();
            UnityEngine.Debug.Log("Connected to server");

            // Start a separate thread to handle incoming messages from the server
            receiveThread = new Thread(ReceiveMessages);
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }
        catch (Exception e)
        {
            UnityEngine.Debug.LogError($"Connection error: {e.Message}");
        }
    }

    // Use the new keyword to hide the inherited member
    public new void SendMessage(string message)
    {
        if (stream != null)
        {
            byte[] data = Encoding.ASCII.GetBytes(message);
            stream.Write(data, 0, data.Length);
            UnityEngine.Debug.Log("Message sent: " + message);
        }
    }
    public void SendAction(string context) {
        if (stream != null)
        {
            byte[] data = Encoding.ASCII.GetBytes(context);
            stream.Write(data, 0, data.Length);
            UnityEngine.Debug.Log("Context sent: " + context);
        }
    }

    void ReceiveMessages()
    {
        try
        {
            byte[] buffer = new byte[1024];
            while (client.Connected)
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead > 0)
                {
                    string message = Encoding.ASCII.GetString(buffer, 0, bytesRead);

                    try
                    {
                        // Attempt to parse the JSON message
                        Data data = JsonUtility.FromJson<Data>(message);

                        // Use the parsed data
                        AgentManager.Instance.DistributeToAgent(data.id, data.command, data.parameters); // Assuming you want to pass the id

                        UnityEngine.Debug.Log($"Received: {message}");
                        UnityEngine.Debug.Log($"ID: {data.id}, Destination: {data.command}");
                    }
                    catch (Exception jsonEx)
                    {
                        // If parsing fails, just output the message
                        UnityEngine.Debug.Log($"Received non-JSON message: {message}");
                    }
                }
            }
        }
        catch (Exception e)
        {
            UnityEngine.Debug.LogError($"Receive error: {e.Message}");
        }
    }


    void OnApplicationQuit()
    {
        stream?.Close();
        client?.Close();
        receiveThread?.Abort();

        if (pythonServerProcess != null && !pythonServerProcess.HasExited)
        {
            pythonServerProcess.Kill();
        }
    }
}

[Serializable]
public class Data
{
    public int id;
    public string command;
    public string parameters;
}
