import sys
import os
import oci
import optparse
import traceback
import logging


class LogAnManager:

    def __init__(self, options, lalogger):
        self.options = options
        self.logger = lalogger
        self.host_compartment_id = options.host_tenancy_logging_compartment_ocid
        self.host_tenancy_ocid = options.host_tenancy_ocid
        self.host_namespace = options.host_tenancy_namespace
        self.init_clients()

    def init_clients(self):
        config = oci.config.from_file()
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
            self.logger.info('SUCCESS: saved search [%s] replicated successfully' % (create_management_saved_search_response.data.display_name))
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
            self.logger.info('SUCCESS: dashboard [%s] replicated successfully' % (create_management_dashboard_response.data.display_name))
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
                    return True
        return False

    def update_saved_search_details(self, replicated_saved_searchs, dashboard):
        recent_traced_time_updated = None
        updated_tiles = []
        for tile in dashboard.tiles:
            if 'ocid1' not in tile.saved_search_id:
                updated_tiles.append(tile)
                continue
            for replicated_saved_search in replicated_saved_searchs:
                if tile.display_name == replicated_saved_search.display_name:
                    if recent_traced_time_updated == None:
                        recent_traced_time_updated = replicated_saved_search.time_updated
                        tile.saved_search_id = replicated_saved_search.id
                    elif recent_traced_time_updated < replicated_saved_search.time_updated:
                        recent_traced_time_updated = replicated_saved_search.time_updated
                        tile.saved_search_id = replicated_saved_search.id
            updated_tiles.append(tile)
        dashboard.tiles = updated_tiles
        return dashboard

    def replicate_saved_search_cross_region(self, home_region, region_list):
        self.logger.info('==================================================================')
        self.logger.info('       Cross region replication of saved searches started         ')
        self.logger.info('==================================================================')
        self.management_dashboard_client.base_client.set_region(home_region)
        list_exit_code, saved_search_list = self.list_saved_searches(home_region)
        if list_exit_code != 0:
            raise Exception('Failed to fetch saved search list from home region [%s]' % (home_region))
        if len(saved_search_list) == 0:
            self.logger.info('No save searches are present in the compartment')
            return
        for region in region_list:
            self.logger.info('Saved search replication started for region [%s]' % (region))
            self.management_dashboard_client.base_client.set_region(region)
            replicated_saved_search_exit_code, replicated_saved_searches = self.list_saved_searches(region)
            if replicated_saved_search_exit_code != 0:
                continue
            replication_count = 0
            for saved_search in saved_search_list:
                if not self.is_already_replicated(saved_search, replicated_saved_searches):
                    create_exit_code = self.create_saved_search_in_region(saved_search)
                    if create_exit_code == 0:
                        replication_count += 1
            self.logger.info('Total number of replication for region [%s] : [%s]' % (region, replication_count))
    
    def replicate_dashboard_cross_region(self, home_region, region_list):
        self.logger.info('==================================================================')
        self.logger.info('         Cross region replication of dashboards started           ')
        self.logger.info('==================================================================')
        self.management_dashboard_client.base_client.set_region(home_region)
        list_exit_code, dashboards_list = self.list_dashboards(home_region)
        if list_exit_code != 0:
            raise Exception('Failed to fetch dashboard list from home region [%s]' % (home_region))
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
            replication_count = 0
            for dashboard in dashboard_details:
                if not self.is_already_replicated(dashboard, replicated_dashboards):
                    if len(dashboard.saved_searches) > 0:
                        dashboard = self.update_saved_search_details(replicated_saved_searchs, dashboard)
                    create_exit_code = self.create_dashboard_in_region(dashboard)
                    if create_exit_code == 0:
                        replication_count += 1
            self.logger.info('Total number of replication for region [%s] : [%s]' % (region, replication_count))

    def cross_region_replication(self, replication_type):
        exit_code = 0 
        try:
            region_exit_code, home_region, region_list = self.get_regions()
            if region_exit_code == 1:
                raise Exception('Failed to fetch regions list')
                
            if replication_type == 'all' or replication_type == 'dashboard':
                self.replicate_saved_search_cross_region(home_region, region_list)
                self.replicate_dashboard_cross_region(home_region, region_list)
            elif replication_type == 'saved_search':
                self.replicate_saved_search_cross_region(home_region, region_list)
            else:
                self.logger.error('ERROR: Please provide valid replication type')
                exit_code = 1

            if exit_code == 0:
                self.logger.info('SUCCESS: Cross region replication completed successfully')
        except Exception as ex:
            self.logger.error('ERROR: Failed to perform cross region replication [%s]' % (ex))
            exit_code = 1
        return exit_code


def init(arg_list=[]):
    class MyParser(optparse.OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    example_usage = '''
     # To replicate saved searches cross regions
     python logan-manager.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # To replicate dashboards cross regions
     python logan-manager.py --replicate --type dashboard  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # To replicate both saved searches and  dashboards cross regions
     python logan-manager.py --replicate  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
    '''
    parser = MyParser(version='%prog 1.0.0', epilog=example_usage)
    parser.add_option('--operation_type', action='store', dest='operation_type', type='string',
                      default='logan-manager', help='Execution Operation Type')
    parser.add_option('--replicate', action='store_true', dest='replicate', default=False, 
                      help='replicate saved searches and dashboards into cross regions')
    parser.add_option('-t', '--type', action='store', dest='type', type='string', default='all',
                      help='Type of replication EX: saved search or dashboard')
    parser.add_option('--compartment_ocid', action='store', dest='host_tenancy_logging_compartment_ocid', type='string', default='None',
                      help='host tenancy logging compartment ocid')
    parser.add_option('--tenancy_ocid', action='store', dest='host_tenancy_ocid', type='string', default='None',
                      help='host tenancy ocid')
    parser.add_option('--tenancy_namespace', action='store', dest='host_tenancy_namespace', type='string', default='None',
                      help='host tenancy namespace')

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



def main(arg_list=[]):
    exit_code = 0
    options, args, parser = init(arg_list)
    if not options.replicate:
        parser.print_help()
        exit_code = 1
        return exit_code


    try:
        DEFAULT_LOG_DIR_BASE = '/scratch/ops/logs'
        logs_dir = os.path.join(DEFAULT_LOG_DIR_BASE)
        create_dirs(logs_dir)
        logger = get_logger(options.operation_type, logs_dir)
        manager = LogAnManager(options, logger)
        if options.replicate:
            exit_code = manager.cross_region_replication(options.type)
            
        if exit_code == 0:
            logger.info('Log Analytics configuration completed successfully.')
        else:
            logger.error('Log Analytics configuration Failed to complete.')
    except Exception as ex:
        exit_code = 1
        traceback.print_exc()
    return exit_code


if __name__ in ['main', '__main__']:
    sys.exit(main())
