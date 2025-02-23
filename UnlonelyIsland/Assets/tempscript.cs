using UnityEngine;

public class tempscript : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // Get the object's position
        Vector3 origin = transform.position;

        // Define the direction of the ray (downward)
        Vector3 direction = Vector3.down;

        // Create a RaycastHit variable to store information about what was hit
        RaycastHit hit;

        // Perform the raycast, if it hits something within a specified distance
        float maxDistance = 100.0f;
        if (Physics.Raycast(origin, direction, out hit, maxDistance))
        {
            // Output the name of the object the ray hit
            Debug.Log("Hit object: " + hit.collider.name);

            // Output the position where the ray hit the object
            Debug.Log("Hit position: " + hit.point.ToString());
        }

    }
}
