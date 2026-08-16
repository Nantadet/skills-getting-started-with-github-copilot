@app.delete("/activities/{activity_name}/participants/{email}")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""

    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is registered
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=404,
            detail="Student is not registered for this activity"
        )

    # Remove student
    activity["participants"].remove(email)

    return {
        "message": f"Unregistered {email} from {activity_name}"
    }