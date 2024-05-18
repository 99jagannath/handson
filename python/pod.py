pods = ['admin-server-0','cec-server-0','clamav-0','refinery-server-0'] 
CEC_MANAGEDSERVER_PATTERN = 'cec_server_'
CEC_MANAGEDPOD_PATTERN = 'cec-server-'
for pd in pods:
    print(pd.replace(CEC_MANAGEDPOD_PATTERN, CEC_MANAGEDSERVER_PATTERN))