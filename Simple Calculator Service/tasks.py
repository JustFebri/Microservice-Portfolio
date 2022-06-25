from cgitb import text
from itertools import count
from unittest import result
from celery import Celery
from time import sleep

from sqlalchemy import false, true

app = Celery('tasks', broker='amqp://localhost', backend='db+sqlite:///db.sqlite3')

def isPrime(n):
    if n <= 1 :
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

@app.task
def prime(n):
    sleep(5)
    counter = 0
    number = 0
    while(n!=counter):
        number+=1
        if isPrime(number):
            counter+=1
    result = {
        "result": number
    }
    return result

@app.task
def prime_palindrom(n):
    sleep(5)
    number = 0
    counter = 0
    while counter != n:
        number += 1
        if isPrime(number):
            if str(number) == str(number)[::-1]:
                counter+=1
    result = {
        "result": number
    }
    return result