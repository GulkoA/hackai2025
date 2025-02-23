using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class NetworkManager : MonoBehaviour
{
    private Process pythonServerProcess;
    private TcpClient client;
    private NetworkStream stream;

    void Start()
    {
        StartPythonServer();
        ConnectToServer();
    }

    void StartPythonServer()
    {
        try
        {
            pythonServerProcess = new Process();
            pythonServerProcess.StartInfo.FileName = "python";
            pythonServerProcess.StartInfo.Arguments = Application.dataPath + "/Scripts/network.py"; // Update path accordingly
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

            // Example: Send a message to the server
            SendMessage("Hello from Unity");
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

            // Example: Read response from the server
            byte[] responseData = new byte[1024];
            int bytes = stream.Read(responseData, 0, responseData.Length);
            UnityEngine.Debug.Log("Received: " + Encoding.ASCII.GetString(responseData, 0, bytes));
        }
    }

    void OnApplicationQuit()
    {
        stream?.Close();
        client?.Close();

        if (pythonServerProcess != null && !pythonServerProcess.HasExited)
        {
            pythonServerProcess.Kill();
        }
    }
}
