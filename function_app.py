import azure.functions as func
import logging
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
KeyVaultName = "test-rag-index"
KVUri = f"https://{KeyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

secretName = "AZURE-OPENAI-KEY"
retrieved_secret = client.get_secret(secretName)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             f"This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.{retrieved_secret}",
             status_code=200
        )