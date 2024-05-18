import sys
import os
import oci
import optparse
import traceback
import logging

# Storing the default values 
DEFAULT_HOST_TENANCY_LOGGING_COMPARTMENT_OCID ='ocid1.compartment.oc1..aaaaaaaantn45vqhpifew6eq2nzc5znuw5xiswhmvrox5c2wsxfogh73jzkq'
DEFAULT_HOST_TENANCY_OCID ='ocid1.tenancy.oc1..aaaaaaaalwaai64ek45opq4daacc6bpertigw7gqdkht2cga35ob3wl2jaaq'
DEFAULT_NAMESPACE = 'oce0003'
DEFAULT_LOG_DIR_BASE = '/tmp/ops/logs'
LOG_SOURCE_ZIP_FILE = 'log_source.zip'

class Replication:

    def __init__(self, options, lalogger):
        self.options = options
        self.logger = lalogger
        self.host_compartment_id = options.host_tenancy_logging_compartment_ocid
        self.host_tenancy_ocid = options.host_tenancy_ocid
        self.host_namespace = options.host_tenancy_namespace
        self.failed_saved_search_list = []
        self.failed_dashboard_list = []
        self.init_clients()

    def init_clients(self):
        config = oci.config.from_file()
        self.log_analytics_client = oci.log_analytics.LogAnalyticsClient(config)
        self.management_dashboard_client = oci.management_dashboard.DashxApisClient(config)
        self.identity_client = oci.identity.IdentityClient(config)

    
    def get_regions(self):
        exit_code = 0
        home_region = None
        region_list = []
        try:
            list_region_subscriptions_response = self.identity_client.list_region_subscriptions(
                tenancy_id=self.host_tenancy_ocid
            )
            for region in list_region_subscriptions_response.data:
                if region.is_home_region:
                    home_region = region.region_name
                else:
                    region_list.append(region.region_name)
            self.logger.info('SUCCESS: Region list fetched successfully.')
        except Exception as ex:
            self.logger.error('ERROR: Failed to fetch regions list [%s]' % (ex))
            exit_code = 1
        return exit_code, home_region, region_list

    def check_logan_for_region(self, region):
        is_enabled = False
        try:
            list_namespaces  = self.log_analytics_client.list_namespaces(
                compartment_id=self.host_tenancy_ocid
            ).data.items
            is_enabled = list_namespaces[0].is_onboarded
        except Exception as ex:
            self.logger.error('ERROR : Failed to check logan enabled for region [%s], %s' % (region, ex))
        return is_enabled
        

    def list_saved_searches(self, region):
        exit_code = 0
        saved_search_list = []
        try:
            saved_search_list = self.management_dashboard_client.list_management_saved_searches(
                compartment_id=self.host_compartment_id
            ).data.items
        except Exception as ex:
            exit_code = 1
            self.logger.error('ERROR: Failed to fetch saved searches from region [%s] , [%s]' % (region, ex))
        return exit_code, saved_search_list
    
    def list_dashboards(self, region):
        exit_code = 0 
        dashboards_list = []
        try:
            dashboards_list = self.management_dashboard_client.list_management_dashboards(
                compartment_id=self.host_compartment_id
            ).data.items
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to fetch dashboards from region [%s], [%s]' % (region, ex))
        return exit_code, dashboards_list

    def list_log_sources(self, region):
        exit_code = 0 
        sources_list = []
        try:
            sources_list = self.log_analytics_client.list_sources(
                namespace_name=self.host_namespace,
                compartment_id=self.host_compartment_id,
                is_system="CUSTOM"
            ).data.items
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to fetch log sources from region [%s], [%s]' % (region, ex))
        return exit_code, sources_list 

    def export_log_source(self, region, log_source_name_list):
        exit_code = 0 
        try:
            export_custom_content_response = self.log_analytics_client.export_custom_content(
                namespace_name=self.host_namespace,
                export_custom_content_details=oci.log_analytics.models.ExportContent(
                    source_names=log_source_name_list
                    )
                )
            with open(LOG_SOURCE_ZIP_FILE, 'wb') as zipFile:
                zipFile.write(export_custom_content_response.data.content)
            self.logger.info('SUCCESS: Log sources successfully exported from region [%s]' % region)
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to export log sources from region [%s], [%s]' % (region, ex))
        return exit_code

    def import_log_source(self, region, log_source_name_list):
        exit_code = 0 
        try:
            with open(LOG_SOURCE_ZIP_FILE, 'rb') as f:
                data = f.read()
                import_custom_content_response = self.log_analytics_client.import_custom_content(
                    namespace_name=self.host_namespace,
                    import_custom_content_file_body=data,
                    is_overwrite=True)
            self.logger.info('SUCCESS: Log sources %s successfully imported to region [%s]' % (log_source_name_list, region))
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to import log sources to region [%s], [%s]' % (region, ex))
        return exit_code  

    def get_dashboard_details(self, dashboards):
        dashboard_details = [] 
        for dashboard in dashboards:
            try:
                details = self.management_dashboard_client.get_management_dashboard(
                    management_dashboard_id=dashboard.dashboard_id
                )
                dashboard_details.append(details.data)
            except Exception as ex:
                self.logger.error('ERROR: Failed to fetch details of dashboard [%s], [%s]' % (dashboard.display_name, ex))
        return dashboard_details
    
    def create_saved_search_in_region(self, saved_search):
        exit_code = 0
        try:
            create_management_saved_search_response = self.management_dashboard_client.create_management_saved_search(
                create_management_saved_search_details=oci.management_dashboard.models.CreateManagementSavedSearchDetails(
                    display_name=saved_search.display_name,
                    provider_id=saved_search.provider_id,
                    provider_version=saved_search.provider_version,
                    provider_name=saved_search.provider_name,
                    compartment_id=saved_search.compartment_id,
                    id=saved_search.id,
                    is_oob_saved_search=saved_search.is_oob_saved_search,
                    description=saved_search.description,
                    nls=saved_search.nls,
                    type=saved_search.type,
                    ui_config=saved_search.ui_config,
                    data_config=saved_search.data_config,
                    screen_image=saved_search.screen_image,
                    metadata_version=saved_search.metadata_version,
                    widget_template=saved_search.widget_template,
                    widget_vm=saved_search.widget_vm,
                    parameters_config=saved_search.parameters_config,
                    freeform_tags=saved_search.freeform_tags,
                    defined_tags=saved_search.defined_tags)
            )
            self.logger.info('SUCCESS: saved search [%s] replicated successfully' % create_management_saved_search_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to replicate [%s], [%s]' % (saved_search.display_name, ex))
            exit_code = 1
        return exit_code


    def create_dashboard_in_region(self, dashboard):
        exit_code = 0
        try:
            create_management_dashboard_response = self.management_dashboard_client.create_management_dashboard(
                create_management_dashboard_details=oci.management_dashboard.models.CreateManagementDashboardDetails(
                    provider_id=dashboard.provider_id,
                    provider_name=dashboard.provider_name,
                    provider_version=dashboard.provider_version,
                    tiles=dashboard.tiles,
                    display_name=dashboard.display_name,
                    description=dashboard.description,
                    compartment_id=dashboard.compartment_id,
                    is_oob_dashboard=dashboard.is_oob_dashboard,
                    is_show_in_home=dashboard.is_show_in_home,
                    metadata_version=dashboard.metadata_version,
                    is_show_description=dashboard.is_show_description,
                    screen_image=dashboard.screen_image,
                    nls=dashboard.nls,
                    ui_config=dashboard.ui_config,
                    data_config=dashboard.data_config,
                    type=dashboard.type,
                    is_favorite=dashboard.is_favorite,
                    parameters_config=dashboard.parameters_config,
                    drilldown_config=dashboard.drilldown_config,
                    freeform_tags=dashboard.freeform_tags,
                    defined_tags=dashboard.defined_tags)
            )
            self.logger.info('SUCCESS: dashboard [%s] replicated successfully' % create_management_dashboard_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to replicate [%s], [%s]' % (dashboard.display_name, ex))
            exit_code = 1
        return exit_code

    def is_already_replicated(self, saved_item, old_saved_items):
        for old_item in old_saved_items:
            if old_item.display_name == saved_item.display_name and old_item.compartment_id == saved_item.compartment_id:
                current_saved_item_time_updated = saved_item.time_updated
                old_saved_item_time_created = old_item.time_created
                if old_saved_item_time_created >= current_saved_item_time_updated:
                    self.logger.info('saved_item [%s] is already replicated' % saved_item.display_name)
                    return True, saved_item
                else:
                    saved_item.id = old_item.id
                    break
        return False, saved_item

    def update_saved_search_details(self, replicated_saved_searches, dashboard):
        recent_traced_time_updated = None
        updated_tiles = []
        for tile in dashboard.tiles:
            if 'ocid1' not in tile.saved_search_id:
                updated_tiles.append(tile)
                continue
            for replicated_saved_search in replicated_saved_searches:
                if tile.display_name == replicated_saved_search.display_name:
                    if recent_traced_time_updated is None:
                        recent_traced_time_updated = replicated_saved_search.time_updated
                        tile.saved_search_id = replicated_saved_search.id
                    elif recent_traced_time_updated < replicated_saved_search.time_updated:
                        recent_traced_time_updated = replicated_saved_search.time_updated
                        tile.saved_search_id = replicated_saved_search.id
            updated_tiles.append(tile)
        dashboard.tiles = updated_tiles
        return dashboard

    def replicate_saved_search_cross_region(self, base_region, region_list):
        self.logger.info('==================================================================')
        self.logger.info('       Cross region replication of saved searches started         ')
        self.logger.info('==================================================================')
        self.management_dashboard_client.base_client.set_region(base_region)
        list_exit_code, saved_search_list = self.list_saved_searches(base_region)
        self.logger.info(len(saved_search_list))
        if list_exit_code != 0:
            raise Exception('Failed to fetch saved search list from home region [%s]' % (base_region))
        if len(saved_search_list) == 0:
            self.logger.info('No save searches are present in the compartment')
            return
        for region in region_list:
            self.logger.info('Saved search replication started for region [%s]' % (region))
            self.management_dashboard_client.base_client.set_region(region)
            replicated_saved_search_exit_code, replicated_saved_searches = self.list_saved_searches(region)
            if replicated_saved_search_exit_code != 0:
                continue
            self.logger.info(len(replicated_saved_searches))
            replication_count = 0
            for saved_search in saved_search_list:
                is_replicated, updated_saved_search = self.is_already_replicated(saved_search, replicated_saved_searches)
                if not is_replicated:
                    create_exit_code = self.create_saved_search_in_region(updated_saved_search)
                    if create_exit_code == 0:
                        replication_count += 1
                    else:
                        self.failed_saved_search_list.append(saved_search.display_name)
            self.logger.info('Total number of replication for region [%s] : [%s]' % (region, replication_count))
    
    def replicate_dashboard_cross_region(self, base_region, region_list):
        self.logger.info('==================================================================')
        self.logger.info('         Cross region replication of dashboards started           ')
        self.logger.info('==================================================================')
        self.management_dashboard_client.base_client.set_region(base_region)
        list_exit_code, dashboards_list = self.list_dashboards(base_region)
        if list_exit_code != 0:
            raise Exception('Failed to fetch dashboard list from home region [%s]' % (base_region))
        if len(dashboards_list) == 0:
            self.logger.info('No dashboards are present in the compartment')
            return
        dashboard_details = self.get_dashboard_details(dashboards_list)
        for region in region_list:            
            self.logger.info('Dashboard replication started for region [%s]' % (region))
            self.management_dashboard_client.base_client.set_region(region)
            replicated_dashboards_exit_code, replicated_dashboards = self.list_dashboards(region)
            if replicated_dashboards_exit_code != 0:
                continue
            replicated_saved_search_exit_code, replicated_saved_searchs = self.list_saved_searches(region)
            if replicated_saved_search_exit_code != 0:
                continue
            replication_count = 0
            for dashboard in dashboard_details:
                if not self.is_already_replicated(dashboard, replicated_dashboards):
                    if len(dashboard.saved_searches) > 0:
                        dashboard = self.update_saved_search_details(replicated_saved_searchs, dashboard)
                    create_exit_code = self.create_dashboard_in_region(dashboard)
                    if create_exit_code == 0:
                        replication_count += 1
                    else:
                        self.failed_dashboard_list.append(dashboard.display_name)
            self.logger.info('Total number of replication for region [%s] : [%s]' % (region, replication_count))

    def replicate_log_source_cross_region(self, base_region, region_list):
        self.logger.info('==================================================================')
        self.logger.info('         Cross region replication of Log source started           ')
        self.logger.info('==================================================================')
        self.log_analytics_client.base_client.set_region(base_region)
        list_exit_code, log_source_list = self.list_log_sources(base_region)
        if list_exit_code != 0:
            raise Exception('Failed to list Log sources from base region [%s]' % base_region)
        log_source_name_list =[]
        for log_source in log_source_list:
            log_source_name_list.append(log_source.display_name)
        export_exit_code = self.export_log_source(base_region, log_source_name_list)
        if export_exit_code != 0:
            raise Exception('Failed to export Log source from region [%s]' % base_region)        
        for region in region_list:
            self.log_analytics_client.base_client.set_region(region)
            if not self.check_logan_for_region(region):
                self.logger.info('Region [%s] is not enabled for Log analytics' % region)
                continue
            self.logger.info('Log source replication started for region [%s]' % region)              
            self.import_log_source(region, log_source_name_list)

    def cross_region_replication(self, options):
        exit_code = 0 
        try:
            region_exit_code, base_region, region_list = self.get_regions()
            if options.base_region is not None:
                region_list.append(base_region)
                base_region = options.base_region
                region_list.remove(base_region)
            region_list = ['us-phoenix-1']
            if region_exit_code == 1:
                raise Exception('Failed to fetch regions list')
            if options.replication_type == 'dashboard':
                self.replicate_saved_search_cross_region(base_region, region_list)
                self.replicate_dashboard_cross_region(base_region, region_list)
            elif options.replication_type == 'saved_search':
                self.replicate_saved_search_cross_region(base_region, region_list)
            elif options.replication_type == 'log-source':
                self.replicate_log_source_cross_region(base_region, region_list)
            else:
                self.logger.error('ERROR: Please provide valid replication type')
                exit_code = 1

            if len(self.failed_saved_search_list) > 0:
                self.logger.error('Saved searches failed to replicate %s' % self.failed_saved_search_list)

            if len(self.failed_dashboard_list) > 0:
                self.logger.error('Dashboards failed to replicate %s' % self.failed_dashboard_list)           
        except Exception as ex:
            self.logger.error('ERROR: Failed to perform cross region replication [%s]' % (ex))
            exit_code = 1
        finally:
            clean_up(LOG_SOURCE_ZIP_FILE)
        return exit_code


def init(arg_list=[]):
    class MyParser(optparse.OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    example_usage = '''
     # if want to replicate from default home region us-ashburn-1
     # To replicate saved searches cross regions
     python saved_item_replication.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # To replicate dashboards cross regions
     python saved_item_replication.py --replicate --type dashboard  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # if want to replicate from base region other than default home region us-ashburn-1
     # To replicate saved searches cross regions
     python saved_item_replication.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
     # To replicate dashboards cross regions
     python saved_item_replication.py --replicate --type dashboard  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
     # To replicate log sources cross regions
     python saved_item_replication.py --replicate --type log-source --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
    '''
    parser = MyParser(version='%prog 1.0.0', epilog=example_usage)
    parser.add_option('--operation_type', action='store', dest='operation_type', type='string',
                      default='saved_item_replication', help='Execution Operation Type')
    parser.add_option('--replicate', action='store_true', dest='replicate', default=False, 
                      help='replicate saved searches and dashboards into cross regions')
    parser.add_option('-t', '--type', action='store', dest='replication_type', type='string', default=None,
                      help='Type of replication EX: saved search or dashboard')
    parser.add_option('--compartment_ocid', action='store', dest='host_tenancy_logging_compartment_ocid', type='string', default= DEFAULT_HOST_TENANCY_LOGGING_COMPARTMENT_OCID,
                      help='host tenancy logging compartment ocid. The default value is OCETelemetry compartment ocid')
    parser.add_option('--tenancy_ocid', action='store', dest='host_tenancy_ocid', type='string', default=DEFAULT_HOST_TENANCY_OCID,
                      help='host tenancy ocid.The default value is oce0003 tenancy  ocid')
    parser.add_option('--tenancy_namespace', action='store', dest='host_tenancy_namespace', type='string', default=DEFAULT_NAMESPACE,
                      help='host tenancy namespace. The default namespace value is oce0003')
    parser.add_option('--base-region', action="store", dest="base_region", type="string", default=None,
                      help='The region from which saved items replicated to other regions')

    if arg_list:
        options, args = parser.parse_args(arg_list)
    else:
        options, args = parser.parse_args()
    return options, args, parser

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

def clean_up(path):
    if os.path.exists(path):
        os.remove(path)      

def main(arg_list=[]):
    exit_code = 0
    options, args, parser = init(arg_list)
    if not options.replicate:
        parser.print_help()
        exit_code = 1
        return exit_code


    try:
        logs_dir = os.path.join(DEFAULT_LOG_DIR_BASE)
        create_dirs(logs_dir)
        logger = get_logger(options.operation_type, logs_dir)
        manager = Replication(options, logger)
        if options.replicate:
            exit_code = manager.cross_region_replication(options)
            
        if exit_code == 0:
            logger.info('Log Analytics saved item replication completed successfully.')
        else:
            logger.error('Log Analytics saved item replication Failed to complete.')
    except Exception as ex:
        exit_code = 1
        traceback.print_exc()
    return exit_code


if __name__ in ['main', '__main__']:
    sys.exit(main())
