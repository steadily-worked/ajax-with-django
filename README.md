# Ajax에 관하여

## 현재 상황
- CORS 오류를 해결하지 못해서 표류하는 중
- Django 서버를 켜고 나서 로컬에서 index.html을 실행하고, 비동기 통신을 통해 버튼을 눌러서 list.html의 내용을 가져오는 것을 목표로 하고 있음


<b>CORS에러가 무엇인가?</b>(하기하는 내용은 <a href="https://evan-moon.github.io/2020/05/21/about-cors/#cors%EC%97%90-%EB%8C%80%ED%95%9C-%EA%B8%B0%EB%B3%B8%EC%A0%81%EC%9D%B8-%EB%82%B4%EC%9A%A9">이 글</a>을 내가 보기 쉽게 정리한 것이다.)
- CORS는, ```Cross-Origin Resource Sharing```의 줄임말. 한국어로 해석해보면 "교차 출처 리소스 공유" 정도로 말할 수 있다. 교차 출처는 곧 다른 출처로 이해하면 된다.

<b>출처(Origin)란 무엇인가?</b>
- https://www.evan-moon.gitgub.io/users?sort=asc&page=1#foo 에서<br>
https:// : Protocol<br>
www.evan-moon.com : Host<br>
/users : Path<br>
?sort=asc&page=1 : Query String<br>
#foo : Fragment<br>의 여러가지 요소로 구성되어 있다.

출처란 이러한 것들을 모두 합친 것을 의미한다. 서버의 위치를 찾아가기 위해 필요한 가장 기본적인 것들을 합쳐놓은 것.

```js
console.log(location.origin);
```
을 개발자 도구 콘솔에서 찍어보면, 손쉽게 어플리케이션이 실행되고 있는 출처를 알아낼 수 있다.

<b>SOP(Same-Origin Policy)</b>

웹 생태계에는 다른 출처로의 리소스 요청을 제한하는 것에 대해 CORS와 SOP의 두 가지 정책이 있다.
SOP는, 단어 뜻 그대로 "같은 출처에서만 리소스를 공유할 수 있다." 라는 규칙을 가진 정책이다.
허나, 다른 출처에서 리소스를 가져와서 쓰는 것은 매우 흔한 일이기 때문에 <b>CORS 정책을 지킨 리소스 요청에 한해</b> 출처가 다르더라도 허용하기로 했다.

우리가 다른 출처로 리소스를 요청한다면 SOP 정책을 위반한 것이 되고, 거기다가 SOP의 예외 조항인 CORS 정책까지 지켜지지 않는다면, 다른 출처의 리소스를 아예 사용할 수 없게 되는 것이다.

즉, 이렇게 다른 출처의 리소스를 사용하는 것을 제한하는 행위는, 하나의 정책만으로 결정된 사항이 아니라는 의미가 되며, SOP에서 확인할 수 있는 예외 사항과 CORS를 사용할 수 있는 케이스들이 맞물리지 않을 경우에는 리소스 요청을 아예 할 수 없는 케이스도 존재할 수 있다.

개발자 입장에선 답답한 오류지만, 이렇게 막아둔 것에는 다 이유가 있기 마련이다.

이렇게 출처가 다른 두 개의 어플리케이션이 자유롭게 소통할 수 있게 된다는 건 꽤나 위험한 환경이다.

현재 브라우저의 개발자 도구만 열더라도 DOM이 어떻게 작성돼 있는지, 어떤 서버와 통신하는지, 리소스의 출처는 어디인지와 같은 각종 정보들을 아무 제한 없이 열람할 수 있다. 이러한 이유 때문에 클라이언트 어플리케이션은 사용자의 공격에 매우 매우 취약하다.

최근엔 자바스크립트 코드를 난독화 하여 외부에서 읽기 어렵게 한다고 하지만, 그렇지 않은 사이트들도 많고 그런 경우는 개발자 도구에서 Script에 대한 소스코드를 너무 쉽게 볼 수 있다.

이런 상황 속에서 다른 출처의 어플리케이션이 서로 통신하는 것에 대해 아무런 제약도 존재하지 않는다면, 악의를 가진 사용자가 소스코드를 쓱 구경한 후 특정 방법을 사용해서 본인의 어플리케이션에서 코드가 실행된 것처럼 꾸며서 사용자의 정보를 탈취하기가 너무 쉬워진다.

이제, 정확히 어떤 경우에 출처가 같다고 판단하고, 어떤 경우에 출처가 다르다고 판단하는 것인지에 대해 알아보자.

<b>같은 출처와 다른 출처의 구분</b>

두 개의 출처가 서로 같다고 판단하는 로직 자체는 굉장히 간단하다. 두 URL의 구성 요소 중 ```Scheme```, ```Host```, ```Port``` 이 세가지만 동일하면 된다.

```https://steadily-worked.github.io:80``` 이라는 출처를 예로 들면, ```https://``` 라는 스킴에 ```steadily-worked.github.io``` 호스트를 가지고 ```:80```번 포트를 사용하고 있다는 것만 같다면 나머지는 전부 다르더라도 같은 출처로 인정이 된다는 것이다.

<b>https://steadily-worked.github.io</b>/about : 스킴, 호스트, 포트가 동일하므로 같은 출처.
<b>https://steadily-worked.github.io</b>/about?q=안뇽 : 스킴, 호스트, 포트가 동일하므로 같은 출처.
http:// -> 스킴이 다르므로 다른 출처.

여기서 중요한 사실 한 가지는, 이렇게 출처를 비교하는 로직이 서버에 구현된 스펙이 아니라 <b>브라우저에 구현되어 있는 스펙</b>이라는 것이다.

만약 우리가 CORS 정책을 위반하는 리소스 요청을 하더라도 해당 서버가 같은 출처에서 보낸 요청만 받겠다는 로직을 갖고 있는 경우가 아니라면 서버는 정상적으로 응답을 하고, 이후 브라우저가 이 응답을 분석해서 CORS 정책 위반이라고 판단되면 그 응답을 사용하지 않고 그냥 버리는 순서인 것이다. 서버는 CORS를 위반하더라도 정상적으로 응답을 해주고, 응답의 파기 여부는 브라우저가 결정한다.

즉 CORS는 브라우저의 구현 스펙에 포함되는 정책이기 때문에, 브라우저를 통하지 않고 서버 간 통신을 할 때는 이 정책이 적용되지 않는다. 또한 CORS 정책을 위반하는 리소스 요청 때문에 에러가 발생했다고 해도 서버 쪽 로그에는 정상적으로 응답을 했다는 로그만 남기 때문에, CORS가 돌아가는 방식을 정확히 모르면 에러 트레이싱에 난항을 겪을 수도 있다.

<b>CORS는 어떻게 동작하는가?</b>

본격적으로 어떤 방법을 통해 서로 다른 출처를 가진 리소스를 안전하게 사용할 수 있는지 알아보도록 하자.

기본적으로 웹 클라이언트 어플리케이션이 다른 출처의 리소스를 요청할 때는 HTTP 프로토콜을 사용하여 요청을 보내게 되는데, 이때 브라우저는 요청 헤더에 Origin이라는 필드에 요청을 보내는 출처를 함께 담아 보낸다.

```http
Origin: https://steadily-worked.github.io
```

이후 서버가 이 요청에 대한 응답을 할 때 응답 헤더에 ```Access-Control-Allow-Origin``` 이라는 값에 "이 리소스를 접근하는 것이 허용된 출처"를 내려주고, 이후 이 응답을 받은 브라우저는 자신이 보냈던 요청의 ```Origin```과 서버가 보내준 응답의 ```Access-Control-Allow-Origin```을 비교해본 후 이 응답이 유효한 응답인지 아닌지를 결정한다.

기본적인 흐름은 이렇게 간단하지만, 사실 CORS가 동작하는 방식은 한 가지가 아니라 세 가지의 시나리오에 따라 변경되기 때문에 본인의 요청이 어떤 시나리오에 해당되는지 잘 파악한다면 CORS 정책 위반으로 인한 에러를 고치는 것이 한결 쉬울 것이다.

<b>Preflight Request</b>

```프리플라이트(Preflight)``` 방식은 일반적으로 우리가 웹 어플리케이션을 개발할 때 가장 자주 마주치는 시나리오이다. 이 시나리오에 해당하는 상황일 때 브라우저는 요청을 한 번에 보내지 않고 예비 요청과 본 요청으로 나눠서 서버로 전송한다. 

이 때에 브라우저가 본 요청을 보내기 전에 보내는 예비 요청을 Preflight라고 부르는 것이며, 이 예비 요청에는 HTTP 메소드 중 ```OPTIONS``` 메소드가 사용된다. 예비 요청의 역할은 본 요청을 보내기 전에 브라우저 스스로 이 요청을 보내는 것이 안전한지 확인하는 것이다.

우리가 자바스크립트의 ```fetch``` API를 사용하여 브라우저에게 리소스를 받아오라는 명령을 내리면 브라우저는 서버에게 예비 요청을 먼저 보내고, 서버는 이 예비 요청에 대한 응답으로 현재 자신이 어떤 것들을 허용하고, 어떤 것들을 금지하고 있는 지에 대한 정보를 응답 헤더에 담아서 브라우저에게 다시 보내주게 된다.

이후 브라우저는, 자신이 보낸 예비 요청과 서버가 응답에 담아준 허용 정책을 비교한 후, 이 요청을 보내는 것이 안전하다고 판단되면 같은 엔드포인트로 다시 본 요청을 보내게 된다. 이후 서버가 이 본 요청에 대한 응답을 하면 브라우저는 최종적으로 이 응답 데이터를 자바스크립트에게 넘겨준다.

이 플로우는 브라우저의 개발자 도구 콘솔에서도 간단하게 재현해볼 수 있는데, 필자의 블로그 환경에서 필자의 티스토리 블로그의 RSS 파일 리소스에 요청을 보내면 브라우저가 본 요청을 보내기 전에 ```OPTIONS``` 메소드를 사용하여 예비 요청을 보내는 것을 확인할 수 있다.

```js
const headers = new Headers({
  'Content-Type': 'text/xml',
});
fetch('https://evan-moon.tistory.com/rss', { headers });
```
```http
OPTIONS https://evan-moon.tistory.com/rss

Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,ko;q=0.8,ja;q=0.7,la;q=0.6
Access-Control-Request-Headers: content-type
Access-Control-Request-Method: GET
Connection: keep-alive
Host: evanmoon.tistory.com
Origin: https://evan-moon.github.io
Referer: https://evan-moon.github.io/2020/05/21/about-cors/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
```

실제로 브라우저가 보낸 요청을 보면, 단순히 ```Origin```에 대한 정보 뿐만 아니라 자신이 예비 요청 이후에 보낼 본 요청에 대한 다른 정보들도 함께 포함되어 있는 것을 볼 수 있다.

이 예비 요청에서 브라우저는 ```Access-Control-Request-Headers```를 사용하여 자신이 본 요청에서 ```Content-Type``` 헤더를 사용할 것을 알려주거나, ```Access-Control-Request-Method```를 사용하여 이후 ```GET``` 메소드를 사용할 것을 서버에게 미리 알려주고 있는 것이다.

이렇게 티스토리 서버에 예비 요청을 보내면, 이제 티스토리 서버가 이 예비 요청에 대한 응답을 보내준다.

```http
OPTIONS https://evanmoon.tistory.com/rss 200 OK

Access-Control-Allow-Origin: https://evanmoon.tistory.com
Content-Encoding: gzip
Content-Length: 699
Content-Type: text/xml; charset=utf-8
Date: Sun, 24 May 2020 11:52:33 GMT
P3P: CP='ALL DSP COR MON LAW OUR LEG DEL'
Server: Apache
Vary: Accept-Encoding
X-UA-Compatible: IE=Edge
```

여기서 우리가 눈여겨 봐야 할 것은 서버가 보내준 응답 헤더에 포함된 ```Access-Control-Allow-Origin: https://evanmoon.tistory.com``` 라는 값이다.

티스토리 서버는 이 리소스에 접근이 가능한 출처는 오직 ```https://evanmoon.tistory.com``` 뿐이라고 브라우저에게 얘기해준 것이고, 필자가 이 요청을 보낸 출처는 ```https://evan-moon.github.io``` 이므로 서버가 허용해준 출처와는 다른 출처이다.

결국 브라우저는 이 요청이 CORS 정책을 위반했다고 판단하고 다음과 같은 에러를 뱉게 되는 것이다.

```
🚨 Access to fetch at ‘https://evanmoon.tistory.com/rss’ from origin ‘https://evan-moon.github.io’ has been blocked by CORS policy: Response to preflight request doesn’t pass access control check: The ‘Access-Control-Allow-Origin’ header has a value ‘http://evanmoon.tistory.com’ that is not equal to the supplied origin. Have the server send the header with a valid value, or, if an opaque response serves your needs, set the request’s mode to ‘no-cors’ to fetch the resource with CORS disabled.
```

이때 예비 요청에 대한 응답에서 에러가 발생하지 않고 정상적으로 ```200```이 떨어졌는데, 콘솔 창에는 빨갛게 에러가 표시되기 때문에 많은 사람들이 헷갈려한다. CORS 정책 위반으로 인한 에러는 예비 요청의 성공 여부와 별 상관이 없다. 브라우저가 CORS 정책 위반 여부를 판단하는 시점은 예비 요청에 대한 응답을 받은 이후이기 때문이다.

물론 예비 요청 자체가 실패해도 똑같이 CORS 정책 위반으로 처리될 수도 있지만, 중요한 것은 예비 요청의 성공/실패 여부가 아니라 "응답 헤더에 유효한 ```Access-Control-ALlow-Origin``` 값이 존재하는가"이다. 만약 예비 요청이 실패해서 ```200```이 아닌 상태 코드가 내려오더라도 헤더에 저 값이 제대로 들어가있다면 CORS 정책 위반이 아니라는 의미이다.

대부분의 경우 이렇게 예비 요청, 본 요청을 나누어 보내는 프라플라이트 방식을 사용하기는 하지만, 모든 상황에서 이렇게 두 번씩 요청을 보내는 것은 아니다. 조금 까다로운 조건이긴 하지만 어떤 경우에는 예비 요청 없이 본 요청만으로 CORS 정책 위반 여부를 검사하기도 한다.
