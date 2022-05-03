# <kbd>module</kbd> `pyfraction`

이 모듈은 파이썬 내장 `fractions.Fraction` 클래스의 재구현 및 확장입니다.

---

## Installation & Usage

```python
import pyfraction
```
또는 
```python
from pyfraction import PyFraction
```
유닛테스트(`pyfractiontest.py`)에서 사용방법을 참조할 수 있습니다.

---

## <kbd>function</kbd> `is_fraction_form`

```python
is_fraction_form(form: str)
```

입력 인자가 분수 형태인지 확인합니다. 


---

## <kbd>function</kbd> `is_numeric_form`

```python
is_numeric_form(form: str)
```

입력 인자가 숫자 형태인지 확인합니다. 


---

## <kbd>class</kbd> `PyFraction`
분수 클래스 

이 클래스는 파이썬 built-in `fractions.Fraction` 클래스를 재구현 및 확장한 것입니다. 

### <kbd>method</kbd> `__init__`

```python
__init__(numerator: object, denominator: object = None) → None
```

이 클래스의 인스턴스를 생성합니다. 



**Args:**
 
 - `numerator` (`object`):  분자. 지원타입: `int`, `float`, `decimal.Decimal`, `numbers.Rational`, `str`, `PyFraction` 
 - `denominator` (`object`, optional): 분모. `None`이 아닐 경우 분자와 호환되는 타입입니다. 기본값은 `None`. 



**Raises:**
 
 - `TypeError`:  변환 가능한 타입 또는 형식이 아닐 경우 
 - `ZeroDivisionError`:  분모가 영(0)으로 주어진 경우 


---

#### <kbd>property</kbd> denominator

분자 

---

#### <kbd>property</kbd> members

(분자:`int`, 분모:`int`) 형태의 `tuple` 객체를 반환합니다. 

---

#### <kbd>property</kbd> numerator

분모 



---

### <kbd>classmethod</kbd> `from_builtin`

```python
from_builtin(fraction: Fraction) → PyFraction
```

`fraction.Fraction` 객체로부터 이 클래스의 인스턴스를 생성합니다. 

---

### <kbd>classmethod</kbd> `from_number`

```python
from_number(number: int | float | Decimal | Rational) → PyFraction
```

`int`, `float`, `decimal.Decimal`, `numbers.Rational` 값으로부터 이 클래스의 인스턴스를 생성합니다. 

---

### <kbd>classmethod</kbd> `from_other`

```python
from_other(fraction: 'PyFraction') → PyFraction
```

이 클래스의 인스턴스로부터 이 클래스의 인스턴스를 생성합니다. 

---

### <kbd>classmethod</kbd> `from_str`

```python
from_str(num_str: str) → PyFraction
```

`str` 객체로부터 이 클래스의 인스턴스를 생성합니다. 

---

### <kbd>method</kbd> `get_Egyptian_expression`

```python
get_Egyptian_expression() → list['PyFraction']
```

이집트식 분수 표기법(단위 분수의 합)으로 변환합니다. 

---

### <kbd>method</kbd> `get_reciprocal`

```python
get_reciprocal() → PyFraction
```

역수를 반환합니다. 

---

### <kbd>method</kbd> `get_whole_number`

```python
get_whole_number() → int
```

(가)분수의 정수부를 반환합니다. 

---

### <kbd>method</kbd> `is_improper`

```python
is_improper() → bool
```

가분수(improper fraction)인지 확인합니다. 

---

### <kbd>method</kbd> `is_integer`

```python
is_integer() → bool
```

분수의 값이 정수인지 확인합니다. 

---

### <kbd>method</kbd> `is_proper`

```python
is_proper() → bool
```

진분수(proper fraction)인지 확인합니다. 

---

### <kbd>method</kbd> `limit_denominator`

```python
limit_denominator(max_denominator: int = 1000000)
```

분모가 최대 `max_denominator`인 현재 인스턴스에 가장 가까운 인스턴스를 반환합니다. 이 메서드는 특히 순환 소수를 변환하는데 유용합니다: 

---

### <kbd>method</kbd> `to_builtin`

```python
to_builtin() → Fraction
```

이 클래스의 인스턴스에 해당하는 `fraction.Fraction` 객체를 반환합니다. 

---

### <kbd>method</kbd> `to_decimal`

```python
to_decimal() → Decimal
```

`decimal.Decimal` 값으로 변환합니다. 

---

## Project Info

### Version

+ Version: 1.0.2022.0503

### Dev Tools

+ Python 3.10
+ Visual Studio Code 1.66

### Environment

+ Test Environment

   + Microsoft Windows 10 Pro (x64)

+ Dependencies / 3rd-party package(s)

  + None

## License

+ MIT License

