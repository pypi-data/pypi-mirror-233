from typing import Dict

import connexion
from dicttoxml import dicttoxml


class BaseView():

    def is_xml(self) -> bool:
        media_type = connexion.request.headers.get('Accept')

        if media_type.strip() == 'application/xml':
            return True
        else:
            return False

    def dict_to_xml(self, dict_: Dict) -> str:
        return dicttoxml(dict_, return_bytes=False)
