import africastalking
from app.config import settings


class SMSService:
    """Service for sending SMS via Africa's Talking"""
    
    def __init__(self):
        africastalking.initialize(
            username=settings.africastalking_username,
            api_key=settings.africastalking_api_key
        )
        self.sms = africastalking.SMS
    
    def send_sms(self, message: str, phone_number: str) -> dict:
        """Send SMS to a phone number"""
        try:
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            response = self.sms.send(
                message,
                [phone_number]
            )
            return response
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return {'error': str(e)}


sms_service = SMSService()
