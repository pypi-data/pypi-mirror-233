from random import randint

from api_compose.servers.api_server_two.views.base import BaseView



class StatefulOneView(BaseView):
    NUMBER = None

    def search(self):
        if self.__class__.NUMBER is not None:
            resp = {'message': 'Number Available', 'number': self.__class__.NUMBER}
            return self.dict_to_xml(resp) if self.is_xml() else resp, 200
        else:
            resp = {'message': 'Number Unavailable'}
            return self.dict_to_xml(resp) if self.is_xml() else resp, 404

    def post(self, body):
        self.__class__.NUMBER = body.get('number')
        resp = {'message': 'Number is set'}
        return self.dict_to_xml(resp) if self.is_xml() else resp, 200

    def delete(self):
        self.__class__.NUMBER = None
        resp = {'message': 'Number is deleted'}
        return self.dict_to_xml(resp) if self.is_xml() else resp, 200


class StatefulTwoView(BaseView):
    NUMBER = randint(1, 1000)

    def search(self):
        resp = {'message': 'Number is retrieved', 'number': self.__class__.NUMBER}
        return self.dict_to_xml(resp) if self.is_xml() else resp, 200

    def post(self, body):
        guess: int = body.get('number')
        if type(guess) == int and guess == self.__class__.NUMBER:
            resp = {'message': f'Your guess is correct!'}
            return self.dict_to_xml(resp) if self.is_xml() else resp, 200
        else:
            resp = {'message': f'Your guess is wrong. Try again!'}
            return self.dict_to_xml(resp) if self.is_xml() else resp, 400
