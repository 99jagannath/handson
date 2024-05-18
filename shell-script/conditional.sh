#! /bin/bash
# indentation is not here but space between letter is matter.
count=0

if [ ${count} ]
then 
    echo "value equals to 10"
elif (( $count > 10 ))
then 
    echo "value greater than 10"
else
    echo "value less than 10"
fi

function is_valid_url() {
    local PROPERTIES_URL=$1
    echo $PROPERTIES_URL
    regex='https?://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
    if [[ ${PROPERTIES_URL} =~ ${regex} ]]; then
        return 0
    else
        return 1
    fi
}
CONTROL_PLANE_PROPERTIES_URL="https://us-ashburn-1.oraclecloud.com/p/hs-2fVnlwuevq1skIu7tu9NXrCj2Yk_56LEekygDbjP6IRmB6SyAOBkS3115BGRE/n/cecdevaccount/b/jagannath-test/o/data_plane.properties"
CONTROL_PLANE_PROPERTIES_OPTS=""
if is_valid_url ${CONTROL_PLANE_PROPERTIES_URL} && [[ -n "${CONTROL_PLANE_PROPERTIES_URL}" ]]; then
    CONTROL_PLANE_PROPERTIES_OPTS="-p ${CONTROL_PLANE_PROPERTIES_URL}"
else
    CONTROL_PLANE_PROPERTIES_OPTS="Not a url"
fi

echo $CONTROL_PLANE_PROPERTIES_OPTS
