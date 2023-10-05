O que há neste pacote?
============

Este pacote tem ferramentas para extender as funcionalidades de API's rest escritas em Django e Django Rest Framework.

Middlewares
------------

### Envelope ###

Este middleware dá a capacidade de incluir um envelope na respostas da API:

Ex:

Requisição: https://[.....]/?**envelope=true**

Resposta:

~~~json
{
    "code": 200,
    "message": "OK",
    "data": {
        "id": "11e87365528a11659bdd005056a83b77",
        "numero_loja": 2,
        "endereco": "RUA OTAVIO ROCHA, 152",
        "cidade": "PORTO ALEGRE",
        "estado": "RS",
        "cep": 90020150,
        "telefone": "(51) 3901-6053"
    }
}
~~~

Requisição: https://[.....]/?**envelope=false**

Resposta:
~~~json
{
    "id": "11e87365528a11659bdd005056a83b77",
    "numero_loja": 2,
    "endereco": "RUA OTAVIO ROCHA, 152",
    "cidade": "PORTO ALEGRE",
    "estado": "RS",
    "cep": 90020150,
    "telefone": "(51) 3901-6053"
}
~~~

Obs.: Por default, o recurso de envelope fica desabilitado (igual a envelope=false).

### Log ###

Este middleware habilita uma personalização dos logs para envio para o Graylog, ferramenta de registro de logs.

Segue um exemplo de configuração:

~~~python
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'settings_filter': {
            '()': 'apicredito.core.logfilter.SettingsFilter',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'graypy': {
            'level': 'INFO',
            'class': 'graypy.GELFHandler', # configurações do Graylog
            'host': '192.168.0.45',
            'port': 12201,
            'level_names': True,
            'extra_fields': True
        }
    },
    'loggers': {       
        'apilog': {
            'level': 'INFO',
            'handlers': ['graypy'],
            'filters': ['settings_filter']
        }
    }
}
~~~

Para habilitar os middlewares, coloque na seção MIDDLEWARE do `settings.py` da sua API Django:

~~~python
MIDDLEWARE = [
    [...]
    'lins_restapi.http.EnvelopeMiddleware',
    'lins_restapi.http.LoggingMiddleware',
]
~~~

Paginação
------------

Este pacote estende a biblioteca de paginação do Django, padronizando e integrando com os demais middlewares do pacote.
Ele adiciona headers nas respostas da API, contendo o total de registros, o número de registros retornados na página e qual a pagina atual. 
Se envelope=true, também retorna como um campo do envelope.

Conceitos:

- total ou X-Total: Total de registros da requisição;
- page ou X-Page: Página atual/requisitada;
- per_page ou X-Per-Page: Número de registros por página;

Ex.:

Requisição:

https://[...]?**per_page**=2&**page**=5&envelope=true

Resposta:

~~~python
{
    "code": 200,
    "message": "OK",
    "total": 43,
    "page": 5,
    "per_page": 2,
    "data": [
        {
            "id": "11e87365528a5bff9bdd005056a83b77",
            "numero_loja": 10,
            "endereco": "RUA JULIO DE CASTILHOS, 2030",
            "cidade": "CAXIAS DO SUL",
            "estado": "RS",
            "cep": 95010002,
            "telefone": "(54) 3223-1685"
        },
        {
            "id": "11e87365528a62609bdd005056a83b77",
            "numero_loja": 11,
            "endereco": "AV. NAÇÕES UNIDAS, 2001",
            "cidade": "NOVO HAMBURGO",
            "estado": "RS",
            "cep": 93320020,
            "telefone": "(51) 3594.5948"
        }
    ]
}
~~~

Headers:

~~~python
X-Page →5
X-Per-Page →2
X-Total →43
~~~

Obs.: Se houver cors, como o `django-cors-headers`, é necessário adicionar os headers de paginação como exceção:

~~~python
CORS_EXPOSE_HEADERS = [
    'X-Page',
    'X-Per-Page',
    'X-Total'
]
~~~

Outros recursos
------------

- Sobrescrita de classes do Swagger Generator afim de tratar o protocolo https;
