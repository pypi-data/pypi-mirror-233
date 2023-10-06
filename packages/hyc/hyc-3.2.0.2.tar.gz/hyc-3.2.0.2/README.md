# hyc库食用指南

## 简介

__名称：hyc库__
[![It's a LOGO](https://i.postimg.cc/NfWmLkMc/logo-for-HYC.png)](https://postimg.cc/VdWdVMnG)

__版本号：3.2.0.2版本__
>新增了当分数为右操作数时的乘方运算

__本次更新时间：2023年10月3日__

_[点击我跳转到GitHub界面哦~](https://github.com/fourlight/hyc)_

---
## 更新记录

### 3.2.0.2版本
>* 增加了当Fraction()对象为指数时的乘方运算
> ```python
> from hyc.fraction import *
> a = Fraction(4,1)
> print(16**a)
> 
> """
> 控制台
> 2
> """
> ```


### 3.2.0版本

>* 修复了一些bug
> 
>_所有被修复的问题_
>* 修复了当`1<=Fraction()对象<2`时`__repr__()`函数无返回值的问题
>* 修复了介绍中不准确的描述
>* 增加了分数计算的 __整除__
>* 分数可以和整数 __直接运算__，不需要再用`convert()`函数转换，且分数 __位置随意__
>```python
>"3.1.0版本"
>from hyc.fraction import *
>from hyc import *
>
># 表示2分之1加5
>a = Fraction(2,1)
>b = convert(5, Fraction)
>print(a+b)
>
>
>""""
>控制台
>5又2分之1
>"""
>```
>```python
>"3.2.0β1测试版"
>from hyc.fraction import *
>
># 表示2分之1加5
>a = Fraction(2,1)
>print(a+5)
>
>
>"""
>控制台
>5又2分之1
>"""
>```
>* 增加了比较运算符功能，使分数之间可以进行比较
>```python
>from hyc.fraction import *
> 
>a = Fraction(2,1)
>b = Fraction(3,1)
>print(a<b, a<=b, a==b, a>b, a>=b, a!=b)
>
>"""
>控制台
>False False False True True True
>"""
>```
>* `__str__()`函数支持带分数



### 3.1.0版本

>* 增加了分数计算的 __乘方计算__
>* 增加了`fraction`模块的`convert()`函数，可让整数和小数直接化为`Fraction`类型， __直接和分数进行运算__

### 3.0.0版本

>* 3.0.0正式版正式上线Pypi，相比于3.0.0β1测试版修复了一些`fraction`模块的bug以及进行了一些调整
>
>_调整内容_
>* 规范了介绍的一些问题
>* 规范了Fraction()类参数的命名
>
>_所有被修复的问题_
>* 修复了`float()`转换和`int()`转换错误的问题
>* 由于出现了bug，移除了`__float__()`的`rounding` __（四舍五入位数）__ 参数，`__float()__`改为自动四舍五入到百分位
---
## 下载方式

### 下载正式版（3.2.1版本）

```
pip install hyc
```
---
## 导入方式

### 1.

```python
from hyc import *
```

### 2.

```python
from hyc import num
```

### 3.

```python
from hyc.num import *
```
---
## hyc库内部结构

```
hyc
├─fraction
│  ├─common_denominator()
│  ├─convert()
│  └─Fraction()类
│      ├─opposide()
│      ├─red_fr()
│      ├─simp_fr()
│      ├─__add__()和__radd__()加法
│      ├─__float__()（分数化小数并保留位数）
│      ├─__init__()
│      ├─__int__()（fraction对象化整数）
│      ├─__mul__()和__rmul__()乘法
│      ├─__repr__()
│      ├─__sub__()和__rsub__()减法
│      ├─__turediv__()和__rturediv__()除法
│      ├─__floordiv__()和__rfloordiv__()整除
│      ├─__pow__()和__rpow__()乘方
│      └─__le__() __lt__() __eq__() __ne__() __gt__() __ge__()比较运算符
└─num
    ├─factor()
    ├─pri_num()
    ├─per_num()
    ├─even_num()
    ├─lcm()
    ├─hcf()
    ├─pri_fac()
    └─comprime()
```
---
## 使用方式

_通过调用函数或类完成您想要达成的效果_

### `num`模块

#### 1.`factor()`

该函数是用来寻找一个数的所有因数的，请在括号内填入一个数字，该函数就可以找出括号内数字的所有参数

##### 示例

```python
from hyc.num import *

print(factor(9))
```
"

"-"台
[1, 3, 9]
"""`

#### 2.`per_num()`

该函数是用来判断一个数是否为完全数的，请在括号内填入一个数字，该函数返回True或False

##### 示例

```python
from hyc.num import *

print(per_num(9), per_num(27))


"""
控制台
False True
"""
```

#### 3.`pri_num()

该函数是用来判断一个数是否为质数的，请在括号内填入一个数字，该函数返回True或False

##### 示例

```python
from hyc.num import *

print(pri_num(9), pri_num(2))


"""
控制台
False True
"""
```

#### 4.`even_num()`

该函数是用来判断一个数是否为偶数的，请在括号内填入一个数字，该函数返回True或False

##### 示例

```python
from hyc.num import *

print(per_num(9), per_num(28))

"""
控制台
False True
"""
```

#### 5.`lcm()`

该函数是用来寻找几个数的最小公倍数的，请在括号内填入一个包含两个或以上数字的列表，请勿填入字符串、浮点数

##### 示例

```python
from hyc.num import *

print(lcm([5, 9]))

"""
控制台
45                    
"""
```

#### 6.`hcf()`

该函数是用来寻找几个数的公因数和最大公因数的，请在括号内填入一个包含两个或以上数字的列表，请勿填入字符串、浮点数；该函数会返回两个值，前一个值为两个数所有的公因数列表，后一个值为两个数的最大公因数

##### 示例

```python
from hyc.num import *

print(hcf([5, 15]))

"""
控制台
[1, 5], 5
"""
```

#### 7.`pri_fac()`

该函数是用来分解一个数的质因数的，请在括号内填入一个数字，该函数返回‘括号内的数 = 质因数1 * 质因数2 * ...’字符串

##### 示例

```python
from hyc.num import *

print(pri_fac(5))

"""
控制台
150 = 2*3*5*5              
"""
```

#### 8.`coprime()`

该函数是用来该函数是用来判断几个数是否为互质数的，请在括号内填入一个包含两个及以上数字的列表，该函数返回True或False

##### 示例

```python
from hyc.num import *

print(coprime([9, 12]), coprime([2, 3]))

"""
控制台
False True
"""
```

### `fraction`模块

_请注意：在hyc库里，分数请先用`name=Fraction(分子,分母)`转换实例化Fraction()类后再使用_

#### 9.`den_di()`

该函数是用来通分的，请在函数内填入一个分数列表，该函数可以将分数列表中的所有分数化为同分母分数

##### 示例

```python
from hyc.fraction import *

a = Fraction(5, 2)  # 代表五分之二
b = Fraction(9, 1)  # 代表九分之一
print(den_di([a, b]))

"""
控制台
[45分之18, 45分之5]
"""
```

#### 10.`convert()`

该函数可以直接将整数和小数化为`Fraction`类型

##### 示例

```python
from hyc import *

a = convert(9.5)
b = convert(8,)
print(a, b, a + b)

"""
控制台
9又2分之1 1分之8 17又2分之1
"""
```

#### 11.`Fraction`类

`Fraction`类是`fraction`模块中最主要的部分，它会创建一个分数对象，如`a=Fraction(2, 5)`就可以创建`五分之二`这个分数；__也支持带分数__，比如`a=Fraction(1, 6, num=5)`
就可以创建`五又六分之一`这个分数，其中的`num`表示带分数的 __整数部分__

其中的`__int__()`函数和`__float__()`基本原理相同，都是将分数化为整数（或小数）

##### 示例

```python
from hyc.fraction import *

a = Fraction(2, 4)
print(int(a))  # 将4分之2化为整数

"""
控制台
1
"""
```

>这段代码，就是将4分之2化为整数，因为4分之2等于0.5，0.5四舍五入等于1，因此返回1
`__float__()`函数与`__int__()`函数的不同点在于`__float__()`函数是直接将对象化为小数，而不是保留到个位

#### 示例

```python
a = Fraction(1, 8)
print(float(a))


"""
控制台
0.125
"""
```

>8分之1等于0.125，因此返回0.125 除了`__int__()`和`__float__()`函数，还有`__repr__()`函数，用于控制对象的名称，比如`Fraction(2, 1)`就是`2分之1`；也支持带分数，如`Fraction(9, 5, num=3)`
为`3又9分之5`，`Fraction(9, 32)`也为`3又9分之5`

剩下的`red_fr()`，`simp_fr()`和`opposide()`函数除了调用方式是

```
a = Fraction(分母,分子)
a.函数()
```

其余用法与[2.2.0版本](https://pypi.org/project/hyc/2.2.0) 相同

剩下的就是加减乘除四则运算了，__可以直接运算__

##### 示例

```python
from hyc.fraction import *

a = Fraction(1, 5)
b = Fraction(1, 4)
c = Fraction(1, 3)
print(a + b + c)

"""
控制台
60分之47
"""
```

当然，示例中的`+`可以替换成`-`，`*`和`/`，但暂时不支持`//`

不仅如此，还有 __乘方运算__

##### 示例

```python
from hyc.fraction import *

a = Fraction(1, 2)
print(a ** 2, 4 ** a)

"""
控制台
4分之1 2
"""
```

__混合运算__ 也被支持

##### 示例

```python
from hyc.fraction import *

a = Fraction(1, 3)
b = Fraction(1, 6)
c = Fraction(2, 3)
print(a + b * c)

"""
控制台
9分之4
"""
```

也可以做出整数或小数与分数运算的效果

##### 示例

```python
from hyc.fraction import *

a = Fraction(1, 5)
print(a+5)

"""
控制台
5又2分之1
"""

```

分数、整数和小数之间还可以进行比较

##### 示例

```python
from hyc.fraction import *

a = Fraction(2, 9)
b = Fraction(1, 9)
print(a < b, a <= b, a == b, a != b, a >b, a >= b, a < 1, a < 1.1)

"""
控制台
False False False True True True False False
"""
```

但值得注意的是，只能`分数<整数（小数）`，不能`整数（小数）>分数` __（比较运算符前必须是分数）__

---
## 分数计算小程序

_如果您觉得hyc库的分数计算太过于麻烦，~~贴心~~的作者准备了一个相对简便的分数计算小软件，源代码[请点击这里](http://github.com/fourlight/fra_cal)_

---
## 感谢您的使用，希望对您有所帮助