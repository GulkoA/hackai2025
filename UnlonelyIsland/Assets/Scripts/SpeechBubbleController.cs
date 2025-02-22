using UnityEngine;
using TMPro;

public class SpeechBubbleController : MonoBehaviour
{
    public TextMeshProUGUI dialogueText;
    public Transform target;

    void Update()
    {
        transform.LookAt(Camera.main.transform);

        Vector3 worldPosition = target.position + new Vector3(0, 2.0f, 0); // Adjust the y-offset as needed
        Vector3 screenPosition = Camera.main.WorldToScreenPoint(worldPosition);

        transform.position = Camera.main.ScreenToWorldPoint(new Vector3(screenPosition.x, screenPosition.y, screenPosition.z));
    }

    public void SetDialogue(string dialogue)
    {
        dialogueText.text = dialogue;
    }
}
    