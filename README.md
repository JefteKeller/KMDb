# KMDb

>---
>
> Esta aplicação é um sistema de avaliação/crítica de filmes.
>
>---

Nossa plataforma KMDb possibilita  ter um ou mais admins que ficarão responsáveis pelo cadastro dos filmes, um ou mais críticos/revisores que podem escrever avaliações para os filmes cadastrados e usuários "comuns" que podem escrever comentários sobre os filmes.

## Sobre Usuários

>---
>
> Admin - será responsável por criar e deletar os filmes na plataforma.
>
>
> Crítico - não poderão criar ou deletar filmes, mas sim criar > as avaliações para eles.
>
> Usuários - podem somente adicionar quantos comentários quiserem aos filmes.
>
>---

## Sobre Críticas

---

Os usuários do tipo "críticos" são os responsáveis por criar reviews para os filmes cadastrados na plataforma. Cada crítico só poderá fazer uma crítica por filme. Caso necessário, poderão editá-las, mas nunca criar mais de uma.

O número de estrelas dadas em uma review deve estar faixa de 1 a 10. 

## Rotas

---

### Rota Base para todas as solicitações

``` Shell
http://127.0.0.1:8000/api/
```


## Para criar diferentes usuários altere essas propriedades

---

>---
>
> Usuário - terá ambos os campos is_staff e is_superuser com o valor False. <br>
>Crítico - terá os campos is_staff == True e is_superuser == False. <br>
>Admin - terá ambos os campos is_staff e is_superuser com o valor True. 
>
>---

### Exemplo de Criação de um Usuário Comum

 ``` JSON
// REQUEST
{
  "username": "user",
  "password": "1234",
  "first_name": "John",
  "last_name": "Wick",
  "is_superuser": false,
  "is_staff": false
}
 ```

 ``` JSON
 // RESPONSE STATUS -> HTTP 201 CREATED
{
  "id": 1,
  "username": "user",
  "first_name": "John",
  "last_name": "Wick",
  "is_superuser": false,
  "is_staff": false,
}
```

### Rota de Login

``` JSON
POST /login/
```


``` JSON
// REQUEST
{
  "username": "critic",
  "password": "1234"
}
```

``` JSON
// RESPONSE STATUS -> HTTP 200 OK
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}

Esse token deverá ser adicionado no Header dos Requests de acordo com o nível de Permissão necessário.
```

### Rota de Criação de Filmes

``` JSON
POST /movies/
```


``` JSON
// REQUEST
// Header -> Authorization: Token <token-do-admin>
{
  "title": "O Poderoso Chefão",
  "duration": "175m",
  "genres": [
    {"name": "Crime"},
    {"name": "Drama"}
    ],
  "launch": "1972-09-10",
  "classification": 14,
  "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado."
}
```


### Rota de Listagem de Filmes

``` JSON
GET /movies/
```


### Rota de Listagem de Filmes com Filtro

``` JSON
GET /movies/
```

``` JSON
{
  "title": "liberdade" // Campo de Filtro Aceito
}
```


### Rota de Busca de Filme pelo ID

``` JSON
GET /movies/<int: movie_id>/
```


### Rota de Deleção de um Filme

``` JSON
DELETE  /movies/<int:movie_id>/
```

>Somente um usuário do tipo `Admin` pode deletar filmes.



### Rota de Criação de Review

``` JSON
POST  /movies/<int:movie_id>/review
```

>Somente um usuário do tipo `Critico` pode deletar filmes.



### Rota de Alteração de Review

``` JSON
PUT  /movies/<int:movie_id>/review
```



### Rota de Criaçao de Comentários

``` JSON
POST  /movies/<int:movie_id>/comments
```


``` JSON
// REQUEST
// Header -> Authorization: Token <token-do-user>
{
  "comment": "Lindo filme. Com certeza assistam.",
}
```

>Somente um usuário `Comum` pode enviar comentários.



### Rota de Alteração de Comentários

``` JSON
PUT  /movies/<int:movie_id>/comments
```


``` JSON
// REQUEST
// Header -> Authorization: Token <token-do-user>
{
  "comment_id": 1,
  "comment": "Lindo, nos faz refletir sobre a vida, os anos, envelhecer. Vale a pena assistir"
}
```

