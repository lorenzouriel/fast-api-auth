## O que é um JWT
O JWT é um padrão (RFC 7519) que define uma maneira compacta e autônoma de transmitir informações entre as partes de maneira segura. Essas informações são transmitidas como um objeto JSON que é digitalmente assinado usando um segredo (com o algoritmo HMAC) ou um par de chaves pública/privada usando RSA, ou ECDSA.

Um JWT consiste em três partes:

1. **Header:** O cabeçalho do JWT consiste tipicamente em dois componentes: o tipo de token, que é JWT neste caso, e o algoritmo de assinatura, como HMAC SHA256 ou RSA. Essas informações são codificadas em Base64Url e formam a primeira parte do JWT.
```py
{
   "alg": "HS256",
   "typ": "JWT"
}
```

2. **Payload:** O payload de um JWT é onde as reivindicações (em inglês claims) são armazenadas. As reivindicações são informações que queremos transmitir e que são relevantes para a interação entre o cliente e o servidor. As reivindicações são codificadas em Base64Url e formam a segunda parte do JWT.
```py
{
  "sub": "teste@test.com",
  "exp": 1690258153
}
```

3. **Signature:** A assinatura é utilizada para verificar que o remetente do JWT é quem afirma ser e para garantir que a mensagem não foi alterada ao longo do caminho. Para criar a assinatura, você precisa codificar o cabeçalho, o payload, e um segredo utilizando o algoritmo especificado no cabeçalho. A assinatura é a terceira parte do JWT. Uma assinatura de JWT pode ser criada como se segue:
```py
HMACSHA256(
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
 nosso-segredo
)
```

Essas três partes são separadas por pontos (.) e juntas formam um token JWT.

Formando a estrutura: `HEADER.PAYLOAD.SIGNATURE` que formam um token parecido com:
```py
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.Nx0P_ornVwJBH_LLLVrlJoh6RmJeXR-Nr7YJ_mlGY04
```

É importante ressaltar que, apesar de a informação em um JWT estar codificada, ela não está criptografada. Isso significa que qualquer pessoa com acesso ao token pode decodificar e ler as informações nele. No entanto, sem o segredo usado para assinar o token, eles não podem alterar as informações ou forjar um novo token. Portanto, não devemos incluir informações sensíveis ou confidenciais no payload do JWT.

### Claims
As Claims do JWT são as informações que serão adicionadas ao token via payload. Como:
```
{
    "sub": "teste@test.com",
    "exp": 1690258153
}
```

Onde as chaves deste exemplo:
- sub: identifica o "assunto" (subject), basicamente uma forma de identificar o cliente. Pode ser um id, um uuid, email, ...
- exp: tempo de expiração do token. O backend vai usar esse dado para validar se o token ainda é válido ou existe a necessidade de uma atualização do token.

Em nossos exemplos iremos usar somente essas duas claims, mais existem muitas outras. [Você pode ver a lista completa das claims aqui caso queira aprender mais.](https://www.iana.org/assignments/jwt/jwt.xhtml)

## Como funciona o JWT
Em uma aplicação web, o processo de autenticação geralmente funciona da seguinte maneira:
1. O usuário envia suas credenciais (e-mail e senha) para o servidor em um endpoint de geração de token (/token por exemplo);
2. O servidor verifica as credenciais e, se estiverem corretas, gera um token JWT e o envia de volta ao cliente;
3. Nas solicitações subsequentes, o cliente deve incluir esse token no cabeçalho de autorização de suas solicitações. Como, por exemplo: Authorization: Bearer <token>;
4. Quando o servidor recebe uma solicitação com um token JWT, ele pode verificar a assinatura e se o token é válido e não expirou, ele processa a solicitação.
- ![img](/docs/jwt.png)

