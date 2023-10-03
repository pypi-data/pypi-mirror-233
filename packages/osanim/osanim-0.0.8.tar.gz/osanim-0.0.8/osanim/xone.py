__all__ = ['XOne']

from osanim.base import _BaseAPI

class XOne(_BaseAPI):
    """
    XOne API.
    
    Business Utility Library
    """

    def __init__(self, token: str):
        super(XOne, self).__init__(token=token)
        
        
    ############################# Messaging #############################
    def send_sms(self, msisdn:str, message:str, **kwargs):
        """
        This operation is used to send sms messages.
        
        Args:
            msisdn:
            message:
            reference_id:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'xone/v1/messaging/send_sms'
        payload = {'msisdn': msisdn, 'message': message, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    def send_whatsapp(self, msisdn:str, message:str, **kwargs):
        """
        This operation is used to send whatsapp messages.
        
        Args:
            msisdn:
            message:
            reference_id:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'xone/v1/messaging/send_whatsapp'
        payload = {'msisdn': msisdn, 'message': message, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)
    
    def send_email(self, email:str, subject:str, message:str, **kwargs):
        """
        This operation is used to send email messages.
        
        Args:
            email:
            subject:
            message:
            reference_id:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'xone/v1/messaging/send_email'
        payload = {'email': email, 'subject':subject, 'message': message, 'reference_id': kwargs.get('reference_id', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    def send_mobile_notification(self, device_token:str, subject:str, message:str, **kwargs):
        """
        This operation is used to send email messages.
        
        Args:
            email:
            subject:
            message:
            reference_id:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'xone/v1/messaging/send_mobile_notification'
        payload = {'device_token': device_token, 'subject':subject, 'message': message, 'reference_id': kwargs.get('reference_id', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    def send_message(self, msg_type:str, destination:str, subject:str, message:str, **kwargs):
        """
        This operation is used to send email messages.
        
        Args:
            email:
            subject:
            message:
            reference_id:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'xone/v1/messaging/send_message'
        payload = {'msg_type': msg_type, 'destination':destination, 'subject':subject, 'message': message, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    ########################## End of Messaging #########################
    
    
    ############################# Payments #############################
    def get_mobile_telcos_supported(self, **kwargs):
        """
        This operation is used to get supported mobile telcos.
        
        Args:
            country:
        Returns:
            status:
            telcose:
            error:

        """
        
        self._uri = f'xone/v1/payments/get_mobile_telcos_supported?country={kwargs.get("country", "")}'
        return self._api_call()
    
    def send_mobile_payment(self, msisdn:str, amount:str, telco:str, **kwargs):
        """
        This operation is used to send mobile payment to a user using an msisdn.
        
        Args:
            msisdn:
            amount:
            telco:
            reference_id:
        Returns:
            status:
            transaction_id:
            amount:
            telco:
            error:

        """
        
        self._uri = 'xone/v1/payments/send_mobile_payment'
        payload = {'msisdn': msisdn, 'amount': amount, 'telco':telco, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)
    
    def receive_mobile_payment(self, msisdn:str, amount:str, telco:str, **kwargs):
        """
        This operation is used to receive mobile payment from a user using an msisdn.
        
        Args:
            msisdn:
            amount:
            telco:
            reference_id:
        Returns:
            status:
            transaction_id:
            amount:
            telco:
            error:

        """
        
        self._uri = 'xone/v1/payments/receive_mobile_payment'
        payload = {'msisdn': msisdn, 'amount': amount, 'telco':telco, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    def send_bank_payment(self, accmount_number:str, amount:str, swift_code:str, **kwargs):
        """
        This operation is used to send bank payment to a user using an bank account number.
        
        Args:
            accmount_number:
            amount:
            bank_code:
            swift_code:
            reference_id:
        Returns:
            status:
            transaction_id:
            amount:
            bank_code:
            swift_code:
            error:

        """
        
        self._uri = 'xone/v1/payments/send_bank_payment'
        payload = {'accmount_number': accmount_number, 'amount': amount, 'swift_code':swift_code, 'reference_id': kwargs.get('reference_id', ''), 'country':kwargs.get('country', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)
    
    def initiate_card_checkout(self, **kwargs):
        """
        This operation is used to initiate a bank checkout.
        
        Args:
            
            
        Returns:
            status:
            transaction_id:

        """
        
        self._uri = 'xone/v1/payments/initiate_card_checkout'
        payload = {'amount': kwargs.get('amount', ''), 'reference_id': kwargs.get('reference_id', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)
    
    ########################## End of Payments #########################
    
    