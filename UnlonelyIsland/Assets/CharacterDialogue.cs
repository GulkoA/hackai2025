using UnityEngine;

public class CharacterDialogue : MonoBehaviour
{
    public GameObject speechBubblePrefab;
    private SpeechBubbleController speechBubbleController;

    void Start()
    {
        // Instantiate the speech bubble and set the target
        GameObject speechBubble = Instantiate(speechBubblePrefab, transform.position, Quaternion.identity);
        speechBubble.transform.SetParent(this.transform, false);
        speechBubbleController = speechBubble.GetComponent<SpeechBubbleController>();
        speechBubbleController.target = transform;
    }

    public void UpdateDialogue(string speech)
    {
            speechBubbleController.SetDialogue(speech);
    }
}