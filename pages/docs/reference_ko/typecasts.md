---
type: doc
layout: reference
category: "Syntax"
title: "타입 검사와 형변환: 'is'와 'as'"
---

# 타입 검사와 형변환: 'is'와 'as'

## `is`와 `!is` 연산자

`is` 연산자를 사용하면 런타임에 객체가 특정 타입을 따르는지 검사할 수 있다. `!is` 연산자는 반대를 검사한다:

``` kotlin
if (obj is String) {
    print(obj.length)
}

if (obj !is String) { // !(obj is String)와 동일
    print("Not a String")
}
else {
    print(obj.length)
}
```

## 스마트 형변환

코틀린에서는 많은 경우 명시적인 형변환 연산이 필요 없다. 왜냐면 컴파일러가 불변 값에 대해
`is`-검사와 [명시적 형변환](#unsafe-cast-operator)을 추적해서
자동으로 필요한 곳에 (안전한) 형변환을 넣어주기 때문이다:

``` kotlin
fun demo(x: Any) {
    if (x is String) {
        print(x.length) // x를 자동으로 String으로 형변환
    }
}
```

!is 검사를 통해 리턴할 경우 컴파일러는 형변환을 안전하게 할 수 있다는 것을 알고, 자동으로 형변환을 추가한다:

``` kotlin
    if (x !is String) return
    print(x.length) // x를 자동으로 String으로 형변환
```

또한 `&&`와 `||`의 오른쪽에도 자동 형변환을 추가한다:

``` kotlin
    // `||`의 오른쪽에서 x를 자동으로 String으로 형변환
    if (x !is String || x.length == 0) return

    // `&&`의 오른쪽에서 x를 자동으로 String으로 형변환
    if (x is String && x.length > 0) {
        print(x.length) // x를 자등으로 String으로 형변환
    }
```

이런 _스마트 형변환_은 [*when*{: .keyword }-식](control-flow.html#when-expression)과
[*while*{: .keyword }-루프](control-flow.html#while-loops)에서도 동작한다:

``` kotlin
when (x) {
    is Int -> print(x + 1)
    is String -> print(x.length + 1)
    is IntArray -> print(x.sum())
}
```

변수 검사와 사용 사이에 변수가 바뀌지 않는다는 것을 컴파일러가 확신할 수 없으면
스마트 형변환이 동작하지 않는다.
구체적으로 다음 규칙에 따라 스마트 형변환을 적용한다:

  * *val*{: .keyword } 로컬 변수 - 항상 적용
  * *val*{: .keyword } 프로퍼티 - 프로퍼티가 private이거나 internal이거나 프로퍼티를 선언한 같은 모듈에서 검사를 한 경우에 적용.
    커스텀 getter를 가진 프로퍼티나 open 프로퍼티에는 스마트 변환이 적용되지 않음
  * *var*{: .keyword } 로컬 변수 - 변수 검사와 사용 사이에 수정이 없고 변수를 캡처한 람다가 변수를 수정하지 않으면 적용  
  * *var*{: .keyword } 프로퍼티- 적용하지 않음 (왜냐면 다른 코드가 언제든 변수를 수정할 수 있음).


## "Unsafe" 형변환 연산자

보통 형변환 연산자는 형변환이 불가능하면 익셉션을 발생한다. 따라서 이를 *불안전*하다고 한다.
코틀린에서 불안전 형변환은 중위 연산자인 *as*{: .keyword }로 수행한다([연산자 우선순위](grammar.html#precedence)를 보자):

``` kotlin
val x: String = y as String
```

x는 [nullable](null-safety.html)이 아니기 때문에 *null*{: .keyword }을 `String`으로 형변환할 수 없다.
예를 들어, `y`가 null이면 위 코드는 익셉션을 던진다.
자바의 변환 세만틱에 맞추려면, 다음과 같이 변환 연산자의 오른쪽에 nullable 타입이 와야 한다:

``` kotlin
val x: String? = y as String?
```

## "안전한" (nullable) 형변환 연산자

익셉션이 발생하는 것을 피하려면 *안전한* 형변환 연산자인 *as?*{: .keyword }를 사용할 수 있다.
이 연산자는 실패시 *null*{: .keyword }을 리턴한다.

``` kotlin
val x: String? = y as? String
```
*as?*{: .keyword }의 오른쪽이 null이 아닌 `String` 타입이지만 형변환 결과는 nullable이다.