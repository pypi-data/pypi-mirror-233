# Azionpy

Este pacote foi criado com o intuito de facilitar a comunicação com a API
da Azion e permitir a criação e gerenciamentos dos recursos de uma forma 
pythonica.

Em desenvolvimento.

[Acesse a documentação aqui.](https://azionpy.freire.live/)

## Instalação

```bash
pip install azionpy
```

## Uso

Instâncie a classe Azion passando o personal token como parâmetro 
e utilize os métodos de acordo com o recurso.

```python
from azionpy import Azion

client = Azion(
    token='xxxxxxxxmypersonaltokenxxxxxx'
)
```

### Domains

#### Buscar todos:
```python
domains = client.get_all_domains()

for domain in domains:
    print(domain.name)
```

#### Criar um:
```python
data = {
    'name': 'my-domain',
    'cnames': ['www.my-domain.com'],
    'cname_access_only': 'true',
    'digital_certificate_id': 123,
    'edge_application_id': 123,
    'edge_firewall_id': 123,
    'is_active': 'true',
}

domain = client.create_domain(
    data=data
)
```


### Digital Certificates

#### Buscar todos:

```python
certs = client.get_all_certificates()

for cert in certs:
    print(cert.name)
```