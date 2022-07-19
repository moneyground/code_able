# 파이썬 내장 수학 관련 함수

# abs(x) 	x의 절댓값을 반환
# sum(iterable)  iterable의 모든 값을 더하여 반환
# max(x1, x2, ... , xn) 	x1, x2, ... , xn 사이에서 가장 큰 수를 반환
# min(x1, x2, ... , xn) 	x1, x2, ... , xn 사이에서 가장 작은 수를 반환
# pow(x, y) 	x의 y제곱을 반환
# round(x), round(x, n) 	x를 반올림하여 반환 / x의 n번째까지 반올림한 수를 반환

# 조건/매개변수 구현 함수

# map(함수, 리스트)  리스트의 원소들을 하나씩 꺼내어 함수에 적용시켜 그 결과값들을 모아 새로운 리스트를 생성
# filter(함수, 리스트) 리스트의 원소들을 함수에 적용시켰을 때 결과가 참인 값들만 모아 새로운 리스트를 생성


#random모듈

# random.random()  0부터 1 사이의 난수 생성
# random.randrange(x,y)  x이상 y이하의 난수 생성
# random.choice(iterable) iterable의 원소 중 무작위로 한 개의 원소 추출
# random.shuffle(iterable)  iterable의 원소를 뒤죽박죽 섞어줍니다.


# math모듈                  https://issac-min.tistory.com/67

# -----수론 및 표현함수-----
# math.ceil(x) 	x를 올림하여 정수값을 반환한다.
# math.floor(x) 	x를 내림하여 정수값을 반환한다.
# math.fabs(x) 	x의 절댓값을 반환한다.
# math.trunc(x)   x의 소수점을 자른 후 정수값을 반환합니다.
# math.copysign(x, y) 	x값의 절댓값에 y의 부호를 갖는 유리수를 반환한다.
# math.comb(n, k) 	nCk과 같은 조합 값을 반환한다. (n개의 수에서 k개를 선택)
# math.perm(n, k) 	nPk와 같은 순열 값을 반환한다. (n개의 수에서 k를 꺼내 순서대로 나열)
# math.factorial(x) 	x의 팩토리얼을 반환합니다. (1*2*3*...*x)
# math.fmod(x, y) 	x에 y를 나눈 후 나머지를 제공한다. (부동소수점 연산에 사용)
# math.frexp(x) 	x를 (m * 2 ** e) 형태로 반환합니다.
# math.ldexp(x, i) 	x * 2 ** i 값을 반환합니다.
# math.fsum(iterable) 	이터러블(iterable)에 있는 값의 정확한 부동 소수점 합을 반환합니다.
# math.prod(iterable) 	이터러블(iterable)의 모든 수의 곱을 반환합니다. (빈 경우 1을 반환)
# math.gcd(integers) 	여러개의 정수를 받아 최대 공약수를 반환합니다.
# math.lcm(integers) 	여러개의 정수를 받아 최소 공약수를 반환합니다.
# math.isclose(a, b) 	a의 실수 연산이 b와 같은지 확인하고 bool 값을 반환합니다.
# math.isfinite(x) 	x값이 무한하거나 Nan(Not a number) 일경우 True 값을 반환합니다.
# math.isinf(x) 	x가 양 또는 음의 무한대이면 True, 반대일 경우 False를 반환합니다.
# math.isnan(x) 	x가 Nan(Not a number)일경우 True, 반대일 경우 False를 반환합니다.
# math.isqrt(n) 	n의 음이 아닌 정수 제곱근을 반환합니다.
# math.modf(x) 	x의 (소수, 정수)부분으로 반환합니다. 정수부분은 float로 반환됩니다

# -----지수와 로그함수-----
# math.exp(x) 	자연상수인 e의 x 거듭제곱을 반환합니다.   	e^x
# math.expm1(x) 	자연상수인 e의 x 거듭제곱에서 1을 뺀값을 반환합니다. 	e^x - 1
# math.log(x) 	진수가 x인 자연로그를 반환합니다. 	ln(x)
# math.log(x,base) 	밑을 base, 진수를 x로 가지는 log를 반환합니다. 	log(x) / log(base)
# math.log1p(x) 	밑이 e(자연상수)인 x+1의 자연로그를 반환합니다.  	ln(1+x)
# math.log2(x) 	밑이 2인 로그를 반환합니다. 	log(x) / log(2)
# math.log10(x) 	밑이 10인 상용로그를 반환합니다. 	log(x) / log(10)
# math.pow(x, y) 	x의 y 거듭제곱을 반환합니다. 	x^y
# math.sqrt(x) 	x의 제곱근을 반환합니다. 	x^(1/2)

# -----삼각함수-----
# math.sin(x) 	x 라디안의 사인값을 반환합니다. 	sin(x)
# math.cos(x) 	x 라디안의 코사인값을 반환합니다. 	cos(x)
# math.tan(x) 	x 라디안의 탄젠트값을 반환합니다. 	tan(x)
# math.asin(x) 	x의 아크 사인을 라디안 값으로 반환합니다. 	asin(x)
# math.acos(x) 	x의 아크 코사인을 라디안 값으로 반환합니다. 	acos(x)
# math.atan(x) 	x의 아크 탄젠트를 라디안 값으로 반환합니다. 	atan(x)
# math.atan2(x) 	y/x의 아크 탄젠트를 라디안 값으로 반환합니다. 	atan(y/x)
# math.dist(p, q) 	두 점 p와 q 사이의 유클리드 거리를 반환합니다.(p와 q는 이터러블) 	root((p2-p1)^2+(q2 - q1)^2)
# math.hypot(x, y) 	가로 x 세로 y인 각직삼각형의 빗면의 유클리드 거리를 반환합니다. 	root(x^2 + y^2)

# -----각도변환함수-----
# math.degrees(x) 	라디안인 x를 도(degree)로 반환합니다. 	180/pi * x
# math.radians(x) 	도(degree)인 x를 라디안으로 반환합니다. 	pi/180 * x

# -----쌍곡선함수-----
# math.asinh(x) 	x의 역 쌍곡 사인값을 반환합니다. 	ln(x+root(x^2 + 1))
# math.acosh(x) 	x의 역 쌍곡 코사인값을 반환합니다. 	ln(x+root(x^2 - 1))
# math.atanh(x) 	x의 역 쌍곡 탄젠트값을 반환합니다. 	1/2 * ln((1+x)/(1-x))
# math.sinh(x) 	x의 쌍곡 사인값을 반환합니다. 	(e^x - e^(-x))/2
# math.cosh(x) 	x의 쌍곡 코사인값을 반환합니다. 	(e^x + e^(-x))/2
# math.tanh(x) 	x의 쌍곡 탄젠트값을 반환합니다. 	(e^2x - 1)/(e^2x +1)