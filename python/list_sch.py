#!/usr/bin/python

import oci



signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()


service_connector_client = oci.sch.ServiceConnectorClient(config={}, signer=signer)



def list_service_connector(display_name, compartment_id ):
    connector_list = []
    try:
        list_service_connector_response = service_connector_client.list_service_connectors(
                compartment_id=compartment_id,
                lifecycle_state="ACTIVE",
                display_name=display_name
            )
        print("Service connectors listed successfully")
        connector_list = list_service_connector_response.data.items
        print(connector_list)
    except Exception as e:
        raise
    return connector_list

list_service_connector("sch1","ocid1.compartment.oc1..aaaaaaaaeqga6zmp4bfadayjl4nmj2nzoytz5v7pj6jtrbvng36ra2ygaoia")