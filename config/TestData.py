import requests.auth

class TestData:
    # CHROME_EXECUTABLE = "/usr/local/bin/chromedriver"
    # FIREFOX_EXECUTABLE = "/usr/local/bin/geckodriver"
    # EDGE_EXECUTABLE = "/usr/local/bin/msedgedriver"

    # Enrollment Workflow Url
    KEYCLOAK_URL = "https://stage-sso.plansource.com/auth/realms/stage-benefits/protocol/openid-connect/token"
    ENROLLMENT_SERVICE_URL = "https://98c0bbb9-587a-4181-b1fc-b208059524c0.trayapp.io"
    HCM_SERVICE_KEYCLOAK_URL = "https://stage-sso.plansource.com/auth/realms/stage-hcm/protocol/openid-connect/token"
    HCM_SERVICE_UPDATE_EVENT_URL = "https://stage-hcm.plansource.com/api/v1/source/paylocity/org_code/1PS001/subscriber"
    HCM_SERVICE_CREATE_EVENT_URL = "https://stage-hcm.plansource.com/api/v1/source/paylocity/org_code/"
    HCM_SERVICE_TERMINATE_EVENT_URL = "https://stage-hcm.plansource.com/api/v1/source/paylocity/org_code/1PS001/subscriber"

    HCM_SERVICE_PROD_KEYCLOAK_URL = "https://sso.plansource.com/auth/realms/hcm/protocol/openid-connect/token"
    HCM_SERVICE_PROD_CREATE_EVENT_URL = "https://hcm.plansource.com/api/v1/source/paylocity/org_code/"
    HCM_SERVICE_PROD_UPDATE_EVENT_URL = "https://hcm.plansource.com/api/v1/source/paylocity/org_code/"
    HCM_SERVICE_PROD_EVENT_LOG_INDEX = "https://hcm.plansource.com/api/event_logs"
    HCM_SERVICE_PROD_EVENT_LOG_DETAILS = "https://hcm.plansource.com/api/event_logs/"
    HCM_SERVICE_PROD_TERMINATE_EVENT_URL = "https://hcm.plansource.com/api/v1/source/paylocity/org_code/"

    # Prudential Enrollment Workflow Url
    PRUDENTIAL_ENROLLMENT_URL = "https://6da1d2c8-5107-41cc-9c8e-e91611579717.trayapp.io"

    # Prudential Mapping mocked workflow url
    PRUDENTIAL_MAPPING_URL = "https://d4af0e7b-14c1-4387-93b7-0f9b69d78264.trayapp.io"

    # HCM Service Production Credentials

    HCM_service_prod_client_id = "hcm_service"
    HCM_service_prod_client_secret = "oYNFPeYZ3Wwr4CzxH7IJ04gnVEcEG00X"
    HCM_service_prod_client_auth = requests.auth.HTTPBasicAuth(HCM_service_prod_client_id, HCM_service_prod_client_secret)
    HCM_service_prod_auth_url = HCM_SERVICE_PROD_KEYCLOAK_URL
    HCM_service_prod_query_params = {"grant_type": "client_credentials"}

    # HCM Service URL
    URL_PARTNER_DEV = 'https://stage-hcm.plansource.com'
    URL_PROD = 'https://hcm.plansource.com/'

    GUARDIAN_PROD_URL = 'https://api.guardianlife.com'
    GUARDIAN_QA_URL = 'https://api.uat.guardianlife.com/'
    GUARDIAN_AUTH_HEADER = {'Content-Type': 'application/json', 'Authorization': 'Basic YXpoN3Q3aVlrQUpyU2ZaQk4xOTA4TUxaZWZVUlpnOTE6YnRXQnNrRHI4REFHVXZnVQ=='}






