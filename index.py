import re
import json
from readme_wrapper import ReadmeClient

def convert_parameters(curl_string):
	endpoint = re.search(r'curl[\S\s]*?http[\S]+', curl_string).group()
	regex = re.compile(r'(?<=\')[^\=\']+=[^\']+')
	parameters = regex.findall(curl_string)
	json_dict = {}
	for parameter in parameters:
		key_valor = parameter.split('=')
		json_dict[key_valor[0]] = key_valor[1]
	pretty_printed_json = json.dumps(json_dict, indent=4, sort_keys=True)
	formatted_curl = endpoint + " -H 'content-type: application/json' \n -d '" + pretty_printed_json + "'"
	return formatted_curl

with open('config.json', 'r') as file:
	readme_configs = json.load(file).get('readme')
	client = ReadmeClient(readme_configs, 'pagarme', 'v1');

pages = [
"/docs/overview-principal",
"/docs/getting-started",
"/docs/dashboard-pagarme",
"/docs/api-key-e-encryption-key",
"/docs/versionamento",
"/docs/bibliotecas-pagarme",
"/docs/overview-transacao",
"/docs/obtendo-os-dados-do-cartao",
"/docs/realizando-uma-transacao-de-cartao-de-credito",
"/docs/realizando-uma-transacao-de-boleto-bancario",
"/docs/usando-metadata",
"/docs/estornando-uma-transacao",
"/docs/overview-checkout",
"/docs/inserindo-o-formulario",
"/docs/overview-marketplace",
"/docs/criacao-conta-bancaria",
"/docs/criando-um-recebedor-1",
"/docs/split-rules",
"/docs/overview-recorrencia",
"/docs/quickstart",
"/docs/criando-um-plano",
"/docs/criando-uma-assinatura",
"/docs/fluxo-de-cobranca",
"/docs/overview-gerenciamento-de-saldo",
"/docs/composicao-do-saldo",
"/docs/saque",
"/docs/overview-antecipacao",
"/docs/criando-uma-antecipacao",
"/docs/consultando-antecipacoes",
"/docs/cancelando-uma-antecipacao",
"/docs/overview-postback-url",
"/docs/gerenciando-postbacks",
"/docs/armazenando-um-cartao",
"/docs/card-hash",
"/docs/overview-mpos",
"/docs/integrando-com-ios",
"/docs/integrando-com-android",
"/docs/integrando-com-windows",
"/docs/tabela-de-erros",
"/docs/instalando-modulo-magento",
"/docs/configurando-o-modulo-magento",
"/docs/instalando-plugin-pagarme-woocommerce",
"/docs/configurando-o-plugin-pagarme-woocommerce",
"/docs/instalando-modulo-prestashop",
"/docs/instalando-modulo-opencart",
"/docs/configurando-o-modulo-opencart",
"/docs/sdk-ios",
"/docs/sdk-android",
"/docs/sdk-windowsnet",
"/docs/referencia-completa-da-api",
]

response = client.get_page('/docs/criando-um-plano')
body = response.json().get('body')

# regex = re.compile(r'(?<=\[block:code\])[\S\s]*?(?=\[/block\])')

def replace_lambda(match):
	string_match = match.group()
	codes = json.loads(string_match).get('codes')
	curl_code = filter(lambda item: 
		item.get('language') == 'curl', 
		codes
	)
	curl_code[0]['code'] = convert_parameters(codes[0].get('code'))
	return json.dumps({ 'codes': codes}, indent=4)

replaced_body = re.sub(r'(?<=\[block:code\])[\S\s]*?(?=\[/block\])', replace_lambda, body)
print(replaced_body)