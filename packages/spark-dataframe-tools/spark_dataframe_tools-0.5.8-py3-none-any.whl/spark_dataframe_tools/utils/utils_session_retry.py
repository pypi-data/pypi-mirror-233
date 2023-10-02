MAX_RETRY = 2
MAX_RETRY_FOR_SESSION = 2
BACK_OFF_FACTOR = 0.3
TIME_BETWEEN_RETRIES = 1000
ERROR_CODES = (500, 502, 504)


def requests_retry_session(retries=MAX_RETRY_FOR_SESSION,
                           back_off_factor=BACK_OFF_FACTOR,
                           status_force_list=ERROR_CODES,
                           session=None):
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    session = session
    retry = Retry(total=retries,
                  read=retries,
                  connect=retries,
                  backoff_factor=back_off_factor,
                  status_forcelist=status_force_list)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def request_path_schema_artifactory(table_name=None,
                                    env="work",
                                    phase="master",
                                    code_country="pe",
                                    is_uuaa_tag=False,
                                    is_sandbox=False,
                                    token_artifactory=None):
    import os
    import json
    from io import BytesIO
    import requests
    import sys
    from spark_dataframe_tools.utils.utils_enviroment import requests_environ_artifactory

    is_windows = sys.platform.startswith('win')
    env_list = ["work", "live"]
    env_phase = ["master", "raw"]

    if table_name in ("", None):
        raise Exception(f'required variable table_name')
    if str(env) not in env_list:
        raise Exception(f'required variable env', env_list)
    if str(phase) not in env_phase:
        raise Exception(f'required variable phase', env_phase)
    if code_country in ("", None):
        raise Exception(f'required variable code_country')
    if token_artifactory in ("", None):
        raise Exception(f'required variable token_artifactory')

    requests_environ_artifactory()
    s = requests_retry_session(session=requests.Session())

    uuaa_name = str(table_name.split("_")[1]).lower()
    uuaa_tag_name = "".join(table_name.split("_")[2:])
    uuaa_tag_table_name = table_name
    if is_uuaa_tag:
        uuaa_tag_table_name = uuaa_tag_name

    if str(env).lower() == "work":
        artifactory_datio_env = os.getenv("ARTIFACTORY_DATIO_WORK")
    else:
        artifactory_datio_env = os.getenv("ARTIFACTORY_DATIO_LIVE")
    artifactory_gdt_phase = f"{artifactory_datio_env}/schemas/{code_country}/{uuaa_name}/{phase}"
    artifactory_gdt_output_schema = f"{artifactory_gdt_phase}/{uuaa_tag_table_name}/latest/{uuaa_tag_table_name}.output.schema"

    if is_sandbox:
        artifactory_url = os.getenv("ARTIFACTORY_SANDBOX")
        artifactory_gdt = f"http://{artifactory_url}/artifactory"
    else:
        headers = {
            'Content-Type': 'application/json',
            'X-JFrog-Art-Api': f'{token_artifactory}',
            'Authorization': f'{token_artifactory}'
        }
        s.headers.update(headers)
        artifactory_url = os.getenv("ARTIFACTORY_LOCAL")
        artifactory_gdt = f"http://{artifactory_url}/artifactory"
    artifactory_path_complete = f"{artifactory_gdt}/{artifactory_gdt_output_schema}"
    if is_windows:
        artifactory_path_complete = artifactory_path_complete.replace("\\", "/")

    path = s.get(artifactory_path_complete)
    if path.status_code == 200:
        artifactory_json = json.load(BytesIO(path.content))
        return artifactory_json
    else:
        print("Path Artifactory =>", artifactory_path_complete)
        print("Not Found")
        return None
