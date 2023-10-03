import os
from ..utils import converter


class Templates:
    def __init__(self, filepath):
        self._filepath = filepath
        
    def service_template(self):
        return f"""\
#This is a generated service template
from flask import Blueprint
from pydantic import BaseModel

class {converter.to_camel_case_with_capitalize(os.path.basename(self._filepath))}Service(Services):
    
    def _validate(args):
        pass
    
    def _logics(self, req) -> (BaseModel, int):
        pass

    def retrieve(self, req: BaseModel) -> (BaseModel, int):
        pass
        
class {converter.to_camel_case_with_capitalize(os.path.basename(self._filepath))}Controller(Controllers, {converter.to_camel_case_with_capitalize(os.path.basename(self._filepath))}Service):

    def __init__(self, blueprint: Blueprint, endpoint: str, methods: List[str]):
        super().__init__(blueprint, endpoint, methods)

    def controller(self):
        try:
            return super().done()
        except FundamentalException as e:
            return super().catcher(err_response, e)
"""