import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

from tasks import prime, prime_palindrom


class GatewayService:
    name = 'gateway'

    hotel_rpc = RpcProxy('room_service')

    @http('GET', '/api/prime/<int:n>')
    def prime(self, request, n):
        result = prime.delay(n)
        return json.dumps(result.get())
    
    @http('GET', '/api/palindrome/<int:n>')
    def palindrome(self, request, n):
        result = prime_palindrom.delay(n)
        return json.dumps(result.get())
    
# celery -A tasks worker -l info -P gevent