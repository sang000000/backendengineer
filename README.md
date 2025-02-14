
- Middleware란 무엇인가?(withDecorators)
    - Django에서 요청과 응답 사이에서 특정 기능을 수행하는 필터 역할을 하는 컴포넌트이다.
    - 보안, 인증, 요청 로깅, CORS 처리 등 다양한 기능을 구현할 수 있다.

- Decorator란?
    - Decorator는 Python에서 함수를 감싸는 기능을 제공하는 함수로 뷰 함수에 권한을 추가하거나, 요청을 필터링하는 용도로 자주 사용한다.
    - @login_requried 등을 사용하면 로그인한 사용자만 접근할 수 있도록 제한 할 수 있다.

- Django란?
    - Python 기반 웹 프레임워크로, 웹 애플리케이션을 빠르고 효율적으로 개발할 수 있도록 도와준다.
    - MTV (Model-Template-View) 아키텍처를 기반으로 동작한다.
    - ORM(Object Relational Mapping)을 지원하여, SQL을 직접 작성하지 않고도 데이터베이스를 다룰 수 있다.

- JWT란 무엇인가?
    - JWT는 사용자 인증 및 정보 교환을 위한 토큰 기반 인증 방식이다.
    - 일반적인 세션 인증 방식과 달리 서버에 세션 정보를 저장하지 않는다.
    - JWT는 토큰을 클라이언트에 저장하고 요청마다 이를 서버에 전달하여 인증하는 방식이다.
    - JWT는 로그인 시 Access Token과 Refresh Token을 발급하며, 로그아웃 시 Refresh Token을 블랙리스트 처리하여 무효화한다.

