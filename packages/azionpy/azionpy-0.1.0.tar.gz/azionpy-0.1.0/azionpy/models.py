from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Domain(BaseModel):
    """
    Representa um domínio na aplicação.

    Args:
        id (int): O ID único do domínio.
        name (str): O nome do domínio.
        cnames (List[str]): Uma lista de CNAMEs associados ao domínio.
        cname_access_only (bool): Indica se o acesso é permitido apenas via CNAME.
        digital_certificate_id (Optional[int]): O ID do certificado digital associado, se houver.
        edge_application_id (int): O ID da aplicação Edge associada ao domínio.
        is_active (bool): Indica se o domínio está ativo.
        domain_name (str): O nome do domínio.
        environment (str): O ambiente do domínio.
        edge_firewall_id (Optional[int]): O ID do firewall Edge associado, se houver.

    Returns:
        Domain (Domain): Uma instância da classe Domain com os atributos especificados.
    """
    id: int
    name: str
    cnames: List[str]
    cname_access_only: bool
    digital_certificate_id: Optional[int]
    edge_application_id: int
    is_active: bool
    domain_name: str
    environment: str
    edge_firewall_id: Optional[int]


class Certificate(BaseModel):
    """
    Representa um certificado digital na aplicação.

    Args:
        id (int): O ID único do certificado.
        name (str): O nome do certificado.
        issuer (Optional[str]): O emissor do certificado, se especificado.
        subject_name (Optional[List[str]]): A lista de nomes de assunto do certificado, se especificado.
        validity (Optional[datetime]): A data de validade do certificado, se especificada.
        status (str): O status atual do certificado.
        certificate_type (str): O tipo de certificado.

    Returns:
        Certificate (Certificate): Uma instância da classe Certificate com os atributos especificados.

    """
    id: int
    name: str
    issuer: Optional[str]
    subject_name: Optional[List[str]]
    validity: Optional[datetime]
    status: str
    certificate_type: str


def decode_json(response, excepted_status_code):
    from azionpy.exceptions.azion_exceptions import handle_error

    if response is None:
        return None

    status_code = response.status_code
    if status_code != excepted_status_code:
        if status_code >= 400:
            raise handle_error(response)

    return response.json()
