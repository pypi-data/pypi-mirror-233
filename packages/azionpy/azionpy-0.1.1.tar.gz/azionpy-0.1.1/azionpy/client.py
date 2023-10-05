import httpx

from azionpy.api_auth import ApiAuth
from azionpy.exceptions.azion_exceptions import InternalError
from azionpy.models import decode_json, Domain, Certificate


class Azion:
    """Classe principal para interagir com a API da Azion.

    Para começar a usar este cliente, é necessário informar o personal token
    gerado dentro do painel da Azion.

    Após isso, você poderá utilizar os recursos do cliente.

    Parameters:
        token (str): Um personal token gerado dentro do painel da Azion.

    Returns:
        Azion(Azion): instância da classe

    Examples:

        from azionpy import Azion
        client = Azion(
            token='xxxxxxxxmypersonaltokenxxxxxx'
        )

    """
    def __init__(self, token: str):
        self.apiauth = ApiAuth(token)
        self.base_url = 'https://api.azionapi.net/'
        self.headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token ' + self.apiauth.get_token(),
        }
        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=15
        )

    def __create_domain_from_api(self, data):
        return Domain(**data)

    def __create_certificate_from_api(self, data):
        return Certificate(**data)

    def get_all_domains(self):
        """Função que retorna todos os domínios da conta

        Returns:
            data (list(Domain)): lista de domínios

        Examples:

            domains = client.get_all_domains()
            for domain in domains:
                print(domain.name)
        """
        response = []
        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token ' + self.apiauth.get_token(),
        }

        with self.client as client:
            try:
                page = 1
                while True:
                    req = client.get(
                        f'/domains?page={page}'
                    )
                    req.raise_for_status()
                    x = decode_json(req, 200)
                    response.extend(
                        self.__create_domain_from_api(data) for data in x['results']
                    )
                    page = page + 1
                    if page > x['total_pages']:
                        break
            except httpx.HTTPError as e:
                raise InternalError(e)
        return response

    def get_all_certificates(self):
        """Função que retorna todos os certificados digitais da conta

        Returns:
            data (list(Certificate)): lista de certificados

        Examples:

            certificates = client.get_all_certificates()
            for cert in certificates:
                print(cert.name)
        """
        response = []
        with self.client as client:
            try:
                page = 1
                while True:
                    req = client.get(
                        f'/digital_certificates?page={page}'
                    )
                    req.raise_for_status()
                    x = decode_json(req, 200)
                    response.extend(
                        self.__create_certificate_from_api(data) for data in x['results']
                    )
                    page = page + 1
                    if page > x['total_pages']:
                        break
            except httpx.HTTPError as e:
                raise InternalError(e)
        return response

    def create_domain(self, data):
        """
        Função que cria um novo domínio na conta.

        Args:
            data (dict): Os dados do domínio a ser criado.

        Returns:
            Domain (Domain): Uma instância da classe Domain representando o domínio criado.

        Raises:
            InternalError: Se ocorrer um erro HTTP ao criar o domínio.

        Examples:

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

        """
        headers = self.headers
        headers['Content-Type'] = 'application/json'

        try:
            with self.client as client:
                req = client.post(
                    '/domains',
                    headers=headers,
                    json=data
                )
                x = decode_json(req, 201)
                return Domain(**x.get('results'))
        except httpx.HTTPError as e:
            raise InternalError(e)
