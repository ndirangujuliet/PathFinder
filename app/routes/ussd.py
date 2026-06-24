from fastapi import APIRouter, BackgroundTasks, Request
from app.models import USSDRequest, USSDResponse, session_state
from app.services.gemini_service import gemini_service
from app.services.sms_service import sms_service


router = APIRouter()


async def process_grades_and_send_sms(phone_number: str, grades: str):
    """Background task to process grades and send SMS"""
    try:
        # Generate recommendations using Gemini
        recommendations = await gemini_service.generate_recommendations(grades)
        
        # Send SMS with recommendations
        sms_service.send_sms(recommendations, phone_number)
        
        print(f"SMS sent to {phone_number}: {recommendations}")
    except Exception as e:
        print(f"Error in background task: {e}")


@router.post("/webhook/ussd")
async def ussd_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle USSD requests from Africa's Talking"""
    form_data = await request.form()
    
    ussd_request = USSDRequest(
        sessionId=form_data.get("sessionId"),
        phoneNumber=form_data.get("phoneNumber"),
        networkCode=form_data.get("networkCode"),
        serviceCode=form_data.get("serviceCode"),
        text=form_data.get("text", "")
    )
    
    session_id = ussd_request.sessionId
    phone_number = ussd_request.phoneNumber
    text = ussd_request.text
    
    # Parse the text input (Africa's Talking sends concatenated inputs)
    inputs = text.split("*") if text else []
    
    # Check if this is the first request
    if not inputs or inputs == [""]:
        session_state.set(session_id, "step", "grades")
        return USSDResponse(
            response="CON Welcome to Pathfinder! Please enter your KCSE grades (e.g., A, B+, B, C+):",
            action="CON"
        )
    
    # Check current step
    current_step = session_state.get(session_id, "step", "grades")
    
    if current_step == "grades":
        # User has entered their grades
        grades = inputs[-1] if inputs else ""
        
        if grades:
            # Trigger background task to process grades
            background_tasks.add_task(
                process_grades_and_send_sms,
                phone_number,
                grades
            )
            
            # Clean up session
            session_state.delete(session_id)
            
            # Return END response
            return USSDResponse(
                response="END Thank you! Pathfinder is analyzing your grades. You will receive an SMS with your course recommendations shortly.",
                action="END"
            )
        else:
            return USSDResponse(
                response="CON Please enter your KCSE grades to proceed:",
                action="CON"
            )
    
    # Default response
    return USSDResponse(
        response="END An error occurred. Please try again.",
        action="END"
    )
