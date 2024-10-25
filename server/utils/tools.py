class CustomException(Exception):
    def __init__(self,status_code:int,error_detail:str,response:dict):
        self.error_detail=error_detail
        self.response=response
        self.status_code=status_code