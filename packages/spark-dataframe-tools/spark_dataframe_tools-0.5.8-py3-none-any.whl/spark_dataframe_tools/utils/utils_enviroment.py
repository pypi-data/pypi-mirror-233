def requests_environ_artifactory():
    import os

    os.environ["ARTIFACTORY_LOCAL"] = "artifactory.globaldevtools.bbva.com"
    os.environ["ARTIFACTORY_SANDBOX"] = "artifactory-gdt.central-02.nextgen.igrupobbva"

    os.environ["ARTIFACTORY_DATIO_WORK"] = "gl-datio-da-generic-dev-local"
    os.environ["ARTIFACTORY_DATIO_LIVE"] = "gl-datio-da-generic-local"
