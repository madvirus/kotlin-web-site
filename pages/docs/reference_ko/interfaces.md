---
type: doc
layout: reference_ko
category: "Syntax"
title: "인터페이스"
---

# 인터페이스

코틀린의 인터페이스는 자바 8 인터페이스와 매우 유사하다.
추상 메서드를 선언할 수 있고 또한 메서드 구현을 포함할 수 있다.
추상 클래스와의 차이점은 인터페이스는 상태를 가질 수 없다는 것이다.
인터페이스가 프로퍼티를 가질 수 있지만
프로퍼티는 추상이거나 또는 접근자 구현을 제공해야 한다.

인터페이스는 *interface*{: .keyword } 키워드로 정의한다.

``` kotlin
interface MyInterface {
    fun bar()
    fun foo() {
      // optional body
    }
}
```

## 인터페이스 구현

클래스나 오브젝트는 한 개 이상의 인터페이스를 구현할 수 있다.

``` kotlin
class Child : MyInterface {
    override fun bar() {
        // body
    }
}
```

## 인터페이스의 프로퍼티

인터페이스에 프로퍼티를 선언할 수 있다. 인터페이스에 선언한 프로퍼티는 추상이거나
또는 접근자를 위한 구현을 제공할 수 있다.
인터페이스의 프로퍼티는 지원(backing) 필드를 가질 수 없으므로,
인터페이스에 선언한 프로퍼티에서 지원 필드를 참조할 수 없다.

``` kotlin
interface MyInterface {
    val prop: Int // 추상

    val propertyWithImplementation: String
        get() = "foo"

    fun foo() {
        print(prop)
    }
}

class Child : MyInterface {
    override val prop: Int = 29
}
```

## 오버라이딩 충돌 해결

상위 타입 목록에 여러 타입을 지정하면, 같은 메서드에 대한 구현을 두 개 이상 상속받을 수 있다.
다음은 예이다.

``` kotlin
interface A {
    fun foo() { print("A") }
    fun bar()
}

interface B {
    fun foo() { print("B") }
    fun bar() { print("bar") }
}

class C : A {
    override fun bar() { print("bar") }
}

class D : A, B {
    override fun foo() {
        super<A>.foo()
        super<B>.foo()
    }

    override fun bar() {
        super<B>.bar()
    }
}
```

인터페이스 *A*와 *B*는 둘다 *foo()*와 *bar()* 함수를 선언하고 있다.
둘 다 *foo()* 함수를 구현하고 있고 *bar()*는 *B*만 구현하고 있다.
(*A*에서 *bar()*에 abstract를 붙이지 않았는데 그 이유는 인터페이스의 메서드는 몸체가 없으면 기본으로 추상이기 때문이다.)
*A*를 상속받은 콘크리트 클래스인 *C*는 당연히 *bar()*를 오버라이딩해서 구현을 제공해야 한다.

하지만 *A*와 *B*를 상속한 *D*는 두 인터페이스에서 상속한 모든 메서드를 구현해야 하며
*D*가 어떻게 메서드를 구현할지 지정해야 한다.
이 규칙은 한 개 구현을 상속한 메서드(*bar()*)나 여러 구현을 상속한 메서드(*foo()*)에
모두 적용된다.
