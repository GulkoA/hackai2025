using UnityEngine;
using TMPro;

public class SpeechBubbleController : MonoBehaviour
{
    public TextMeshProUGUI dialogueText;
    public Transform target;

    void Update()
    {
        // Make the speech bubble face the camera
        transform.LookAt(Camera.main.transform);

        // Position the speech bubble above the target
        Vector3 screenPosition = Camera.main.WorldToScreenPoint(target.position);
        transform.position = screenPosition + new Vector3(0, 1, 0); // Adjust the offset as needed
    }

    public void SetDialogue(string dialogue)
    {
        dialogueText.text = dialogue;

    }
}
