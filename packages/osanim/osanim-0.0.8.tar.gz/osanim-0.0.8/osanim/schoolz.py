__all__ = ['Schoolz']

from osanim.base import _BaseAPI

class Schoolz(_BaseAPI):
    """
    Schoolz API.
    
    Business Utility Library
    """

    def __init__(self, token: str):
        super(Schoolz, self).__init__(token=token)
        
        
    ############################# Students #############################
    def add_student(self, first_name:str, last_name:str, student_class, **kwargs):
        """
        This operation is used to add a new student.
        
        Args:
            first_name:
            last_name:
            student_classes:
        Returns:
            status:
            transaction_id:
            message:
            error:

        """
        
        self._uri = 'schoolz/v1/students'
        payload = {'first_name': first_name, 'last_name': last_name, 'student_class': student_class, 'phone':kwargs.get('phone', '')}
        headers = None
        return self._api_call(method='POST', payload=payload, headers=headers)

    ########################## End of Students #########################
    
    