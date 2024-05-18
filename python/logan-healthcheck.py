import sys
import os
import oci
import optparse
import traceback
import logging
from datetime import datetime, timedelta, timezone

# Storing the default values 
DEFAULT_HOST_TENANCY_LOGGING_COMPARTMENT_OCID ='ocid1.compartment.oc1..aaaaaaaantn45vqhpifew6eq2nzc5znuw5xiswhmvrox5c2wsxfogh73jzkq'
DEFAULT_HOST_TENANCY_OCID ='ocid1.tenancy.oc1..aaaaaaaalwaai64ek45opq4daacc6bpertigw7gqdkht2cga35ob3wl2jaaq'
DEFAULT_NAMESPACE = 'oce0003'
DEFAULT_LOG_DIR_BASE = '/tmp/ops/logs'
TS_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"



class LoganHealthCheck:

    def __init__(self, options, lalogger):
        self.options = options
        self.logger = lalogger
        self.host_compartment_id = options.host_tenancy_logging_compartment_ocid
        self.host_tenancy_ocid = options.host_tenancy_ocid
        self.host_namespace = options.host_tenancy_namespace
        self.init_clients()

    def init_clients(self):
        # config = oci.config.from_file()
        # self.log_analytics_client = oci.log_analytics.LogAnalyticsClient(config)
        self.signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        self.logan_client = oci.log_analytics.LogAnalyticsClient(config={}, signer=self.signer)

    # Function to excute query
    def excecute_query(self, list_ns_resp, query_string, ts_start, ts_end):
        exit_code = 0
        log_count = 0
        try:
            if len(list_ns_resp.items) > 0 and list_ns_resp.items[0].is_onboarded:
                query_response = self.logan_client.query(namespace_name=DEFAULT_NAMESPACE,
                                                        query_details=oci.log_analytics.models.QueryDetails(
                                                            compartment_id=DEFAULT_HOST_TENANCY_OCID,
                                                            query_string=query_string,
                                                            sub_system="LOG",
                                                            time_filter=oci.log_analytics.models.TimeRange(
                                                                time_start=ts_start,
                                                                time_end=ts_end,
                                                                time_zone=timezone.utc
                                                            ),
                                                            query_timeout_in_seconds=300,
                                                            compartment_id_in_subtree=True
                                                        )
                                )
                log_count = query_response.data
        except Exception as err:
            exit_code = 1
            self.logger.error("Failed to query log count [%s]" % err)
        return exit_code, log_count

    # Function to generate query string
    def generate_query_string(self, log_source, pod_name):
        query_string = "'Log Source' = '%s' | link 'Status' | stats count('Status') as 'Count'" % log_source
        query_string = query_string + " and 'Log Group' = '%s'" % pod_name
        return query_string

    def health_check(self):
        log_source_list = ['OCE FMW WLS Server Access Logs']
        pod_name = 'oradocsphx1'
        ts_end = datetime.utcnow()
        ts_start = self.ts_end - timedelta(minutes=self.options.duration)
        for log_source in log_source_list:
            query_string = self.generate_query_string(log_source, pod_name)
            self.logan_client.base_client.set_region(self.options.region)
            list_ns_resp =  self.logan_client.list_namespaces(
                                compartment_id=DEFAULT_HOST_TENANCY_OCID
                            ).data
            log_count = self.excecute_query(list_ns_resp, query_string, ts_start, ts_end)

def get_pid():
    return os.getpid()

def get_logger(name, logs_dir):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(threadName)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(os.path.join(logs_dir, '%s-%s.log' % (name.lower(), get_pid())))
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(threadName)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_ts(ts):
    return datetime.strptime(ts, TS_FORMAT).replace(tzinfo=timezone.utc)

def init(arg_list=[]):
    class MyParser(optparse.OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    example_usage = '''
     # if want to replicate from default home region us-ashburn-1
     # To replicate saved searches cross regions
     python manage_saved_item.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
    '''
    parser = MyParser(version='%prog 1.0.0', epilog=example_usage)
    parser.add_option('--operation_type', action='store', dest='operation_type', type='string',
                      default='logan_healthcheck', help='Execution Operation Type')
    parser.add_option('--health_check', action='store_stue', dest='health_check',
                      default=False , help='Run health check')
    parser.add_option('--duration', action='store', dest='operation_type', type=int,
                      default=60, help='Log duration')

    if arg_list:
        options, args = parser.parse_args(arg_list)
    else:
        options, args = parser.parse_args()
    return options, args, parser      

def main(arg_list=[]):
    exit_code = 0
    missing_args = False
    options, args, parser = init(arg_list)
    if not options.health_check:
        parser.print_help()
        exit_code = 1
        return exit_code

    
    
    if missing_args:
        parser.print_help()
        exit_code = 1
        return exit_code


    try:
        logs_dir = os.path.join(DEFAULT_LOG_DIR_BASE)
        create_dirs(logs_dir)
        logger = get_logger(options.operation_type, logs_dir)
        manager = LoganHealthCheck(options, logger)
        
        if options.health_check:
            manager.health_check()

        if exit_code == 0:
            logger.info('Log Analytics health check operation completed successfully.')
        else:
            logger.error('Log Analytics health check operation Failed to complete.')
    except Exception as ex:
        exit_code = 1
        traceback.print_exc()
    return exit_code


if __name__ in ['main', '__main__']:
    sys.exit(main())
