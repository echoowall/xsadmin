from django.test import TestCase

# Create your tests here.
import re
from datetime import datetime

def test():
    '''
    restr = re.compile(r'^([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([0-9a-zA-Z]+)\|([\d]+)$')

    match = restr.search('ai9jhklfai9ioj2as890dfh|90fualksdjfo89uq2kef|290fujaklsdf099u12fklja|19871892341')
    print(match)

    if not match:
        print('not match')
    else:
        print(match.group(0))
        print(match.group(1))
        print(match.group(2))
        print(match.group(3))
        print(match.group(4))

    now = datetime.now()
    print(now,type(now),now.timestamp())
    #print(type(int('14889431481488914889431481488943148148894314843148')))
    date1 = datetime.fromtimestamp(0)
    print(date1)
    date_delay = now - date1
    print(date_delay,type(date_delay),date_delay.seconds)
    '''

    from decimal import Decimal

    a = Decimal('1.00')
    print(int(a*0))
    print(a.to_integral)


if __name__ == '__main__':
    test()