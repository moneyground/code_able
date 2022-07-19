

# 소인수분해 함수 (반환 자료형 : 리스트)
def factorization(x): 
    d=2
    result=[]
    while d<=x:
        if x%d==0:
            result.append(d)
            x=x/d
        else:
            d+=1
    return result


# 약수 도출 함수 (반환 자료형 : 리스트)
def yaksoo(num):
    loop=num**0.5
    result=[]
    
    if loop==int(loop):
        result.append(int(loop))
    else:
        pass
    
    i=1
    while i<loop:
        if num%i==0:
            result.append(i)
            result.append(int(num/i))
        i+=1

        result.sort()
    return result


# 약수의 갯수 도출 함수 (반환 자료형: 정수)
def yaksoo_num(num):
    loop=num**0.5
    # for square number
    if loop==int(loop):
        count=1
    else:
        count=0
    
    i=1
    while i<loop:
        if num%i==0:
            count+=2
        i+=1
    return count



# x이하의 소수의 합 반환 함수 (반환 자료형: 정수)
from sympy import isprime

def prime_under_x(x,y):
    if isprime(x):
        y=y+x

    if x>1:
        return prime_under_x(x-1,y)
    else:
        return y


# 숫자를 조각내 리스트로 변환
n=12345
n_list = list(map(int, str(n)))


# 재귀 함수 제한 해제
import sys
limit_number = 15000
sys.setrecursionlimit(limit_number)