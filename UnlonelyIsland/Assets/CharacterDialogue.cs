using UnityEngine;

public class CharacterDialogue : MonoBehaviour
{
    public GameObject speechBubblePrefab;
    private SpeechBubbleController speechBubbleController;

    void Start()
    {
        // Instantiate the speech bubble and set the target
        GameObject speechBubble = Instantiate(speechBubblePrefab, transform.position, Quaternion.identity);
        speechBubble.transform.parent = this.gameObject.transform;
        speechBubbleController = speechBubble.GetComponent<SpeechBubbleController>();
        speechBubbleController.target = transform;
    }

    void Update()
    {
        // Example: Show dialogue when the player presses the space key
        if (Input.GetKeyDown(KeyCode.Space))
        {
            speechBubbleController.SetDialogue("Hello, this is a speech bubble!");
        }
    }
}