import sys
import os
import oci
import optparse
import traceback
import logging
import json
import subprocess

# Storing the default values 
DEFAULT_HOST_TENANCY_LOGGING_COMPARTMENT_OCID ='ocid1.compartment.oc1..aaaaaaaantn45vqhpifew6eq2nzc5znuw5xiswhmvrox5c2wsxfogh73jzkq'
DEFAULT_HOST_TENANCY_OCID ='ocid1.tenancy.oc1..aaaaaaaalwaai64ek45opq4daacc6bpertigw7gqdkht2cga35ob3wl2jaaq'
DEFAULT_NAMESPACE = 'oce0003'
DEFAULT_LOG_DIR_BASE = '/tmp/ops/logs'
LOG_SOURCE_ZIP_FILE = 'log_source.zip'
SAVED_SEARCH_FOLDER = 'saved_search'
DASHBOARD_fOLDER = 'dashboard'
EXPORT_DASHBOARD_FILE = 'dashboards.json'

class SavedItemManager:

    def __init__(self, options, lalogger):
        self.options = options
        self.logger = lalogger
        self.host_compartment_id = options.host_tenancy_logging_compartment_ocid
        self.host_tenancy_ocid = options.host_tenancy_ocid
        self.host_namespace = options.host_tenancy_namespace
        self.saved_item_bucket = options.bucket_name
        self.failed_saved_search_list = []
        self.failed_dashboard_list = []
        self.init_clients()

    def init_clients(self):
        config = oci.config.from_file()
        self.log_analytics_client = oci.log_analytics.LogAnalyticsClient(config)
        self.management_dashboard_client = oci.management_dashboard.DashxApisClient(config)
        self.identity_client = oci.identity.IdentityClient(config)
        self.object_storage_client = oci.object_storage.ObjectStorageClient(config)

    
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

    def put_object_in_object_storage(self, object_name, object_content):
        exit_code = 0
        try:
            put_object_response = self.object_storage_client.put_object(
                namespace_name=self.host_namespace,
                bucket_name=self.saved_item_bucket,
                object_name=object_name,
                put_object_body=object_content
            )
            self.logger.info("saved item [%s] successfully uploaded" % object_name)
        except Exception as ex:
            self.logger.error('Failed to Put object in object storage [%s]' % ex)
            exit_code = 1
        return exit_code
    
    def get_object_from_object_storage(self, object_name, version_id=None):
        saved_item = {}
        exit_code = 0
        try:
            get_object_response = self.object_storage_client.get_object(
                namespace_name=self.host_namespace,
                bucket_name=self.saved_item_bucket,
                object_name=object_name,
                version_id=version_id,
            )
            saved_item.update(json.loads(get_object_response.data.content.decode('utf-8')))
        except Exception as ex:
            self.logger.error('Failed to get object from object storage [%s]' % ex)
            exit_code = 1
        return exit_code, saved_item

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

    def convert_management_type_obj_to_dict(self, obj):
        saved_item = {}
        saved_item.update(json.loads(str(obj)))
        return saved_item

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

    def export_dashboards(self, dashboard_id_map, region):
        exit_code = 0
        try:
            export_dashboard_response = self.management_dashboard_client.export_dashboard(
                                            export_dashboard_id=json.loads(dashboard_id_map)
                                        )
            with open(EXPORT_DASHBOARD_FILE, 'wb') as jsonFile:
                jsonFile.write(export_dashboard_response.data.content)
            self.logger.info('SUCCESS: Dashboards successfully exported from region [%s]' % region)
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to export dashboards from region [%s], [%s]' % (region, ex))
        return exit_code

    def import_dashboards(self, region):
        exit_code = 0 
        try:
            cmd = "oci management-dashboard --region %s dashboard import --dashboards file://%s" % (region, EXPORT_DASHBOARD_FILE)
            output, error, pexit_code = execute_command(cmd, self.logger)
            print(output, error, pexit_code)
            self.logger.info('SUCCESS: dashboards successfully imported to region [%s]' %  region)
        except Exception as ex:
            exit_code  = 1
            self.logger.error('ERROR: Failed to import dashboard to region [%s], [%s]' % (region, ex))
        return exit_code 

    def collect_dashboard_ids(self, dashboard_list):
        dashboard_id_list = []
        for dashboard in dashboard_list:
            dashboard_id_list.append(dashboard.id)
        dashboard_id_map ={}
        dashboard_id_map['dashboardIds'] = dashboard_id_list
        return dashboard_id_map


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
                    display_name=saved_search['display_name'],
                    provider_id=saved_search['provider_id'],
                    provider_version=saved_search['provider_version'],
                    provider_name=saved_search['provider_name'],
                    compartment_id=saved_search['compartment_id'],
                    is_oob_saved_search=saved_search['is_oob_saved_search'],
                    description=saved_search['description'],
                    nls=saved_search['nls'],
                    type=saved_search['type'],
                    ui_config=saved_search['ui_config'],
                    data_config=saved_search['data_config'],
                    screen_image=saved_search['screen_image'],
                    metadata_version=saved_search['metadata_version'],
                    widget_template=saved_search['widget_template'],
                    widget_vm=saved_search['widget_vm'],
                    parameters_config=saved_search['parameters_config'],
                    freeform_tags=saved_search['freeform_tags'],
                    defined_tags=saved_search['defined_tags'])
            )
            self.logger.info('SUCCESS: saved search [%s] create successfully' % create_management_saved_search_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to create [%s], [%s]' % (saved_search.display_name, ex))
            exit_code = 1
        return exit_code


    def create_dashboard_in_region(self, dashboard):
        exit_code = 0
        if len(dashboard['tiles']) > 0:
            dashboard['tiles'] = self.create_tiles(dashboard['tiles'])
        try:
            create_management_dashboard_response = self.management_dashboard_client.create_management_dashboard(
                create_management_dashboard_details=oci.management_dashboard.models.CreateManagementDashboardDetails(
                    provider_id=dashboard['provider_id'],
                    provider_name=dashboard['provider_name'],
                    provider_version=dashboard['provider_version'],
                    tiles=dashboard['tiles'],
                    display_name=dashboard['display_name'],
                    description=dashboard['description'],
                    compartment_id=dashboard['compartment_id'],
                    is_oob_dashboard=dashboard['is_oob_dashboard'],
                    is_show_in_home=dashboard['is_show_in_home'],
                    metadata_version=dashboard['metadata_version'],
                    is_show_description=dashboard['is_show_description'],
                    screen_image=dashboard['screen_image'],
                    nls=dashboard['nls'],
                    ui_config=dashboard['ui_config'],
                    data_config=dashboard['data_config'],
                    type=dashboard['type'],
                    is_favorite=dashboard['is_favorite'],
                    parameters_config=dashboard['parameters_config'],
                    drilldown_config=dashboard['drilldown_config'],
                    freeform_tags=dashboard['freeform_tags'],
                    defined_tags=dashboard['defined_tags'])
            )
            self.logger.info('SUCCESS: dashboard [%s] created successfully' % create_management_dashboard_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to create [%s], [%s]' % (dashboard.display_name, ex))
            exit_code = 1
        return exit_code

    def create_tiles(self, dict_tiles):
        obj_tiles = []
        for tile in dict_tiles:
            obj = oci.management_dashboard.models.ManagementDashboardTileDetails(
                display_name=tile["display_name"],
                saved_search_id=tile["saved_search_id"],
                row=tile["row"],
                column=tile["column"],
                height=tile["height"],
                width=tile["width"],
                nls=tile["nls"],
                ui_config=tile["ui_config"],
                data_config=tile["data_config"],
                state='DEFAULT',
                drilldown_config=tile["drilldown_config"],
                parameters_map=tile["drilldown_config"]
            )
            obj_tiles.append(obj)
        return obj_tiles

    def update_saved_search_in_region(self, saved_search):
        exit_code = 0
        try:
            update_management_saved_search_response = self.management_dashboard_client.update_management_saved_search(
                management_saved_search_id=saved_search['id'],
                update_management_saved_search_details=oci.management_dashboard.models.UpdateManagementSavedSearchDetails(
                    display_name=saved_search['display_name'],
                    provider_id=saved_search['provider_id'],
                    provider_version=saved_search['provider_version'],
                    provider_name=saved_search['provider_name'],
                    compartment_id=saved_search['compartment_id'],
                    is_oob_saved_search=saved_search['is_oob_saved_search'],
                    description=saved_search['description'],
                    nls=saved_search['nls'],
                    type=saved_search['type'],
                    ui_config=saved_search['ui_config'],
                    data_config=saved_search['data_config'],
                    screen_image=saved_search['screen_image'],
                    metadata_version=saved_search['metadata_version'],
                    widget_template=saved_search['widget_template'],
                    widget_vm=saved_search['widget_vm'],
                    parameters_config=saved_search['parameters_config'],
                    freeform_tags=saved_search['freeform_tags'],
                    defined_tags=saved_search['defined_tags'])
            )
            self.logger.info('SUCCESS: saved search [%s] updated successfully' % update_management_saved_search_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to update [%s], [%s]' % (saved_search.display_name, ex))
            exit_code = 1
        return exit_code


    def update_dashboard_in_region(self, dashboard):
        exit_code = 0
        if len(dashboard['tiles']) > 0:
            dashboard['tiles'] = self.create_tiles(dashboard['tiles'])
        try:
            update_management_dashboard_response = self.management_dashboard_client.update_management_dashboard(
                management_dashboard_id=dashboard['id'],
                update_management_dashboard_details=oci.management_dashboard.models.UpdateManagementDashboardDetails(
                    provider_id=dashboard['provider_id'],
                    provider_name=dashboard['provider_name'],
                    provider_version=dashboard['provider_version'],
                    tiles=dashboard['tiles'],
                    display_name=dashboard['display_name'],
                    description=dashboard['description'],
                    compartment_id=dashboard['compartment_id'],
                    is_oob_dashboard=dashboard['is_oob_dashboard'],
                    is_show_in_home=dashboard['is_show_in_home'],
                    metadata_version=dashboard['metadata_version'],
                    is_show_description=dashboard['is_show_description'],
                    screen_image=dashboard['screen_image'],
                    nls=dashboard['nls'],
                    ui_config=dashboard['ui_config'],
                    data_config=dashboard['data_config'],
                    type=dashboard['type'],
                    is_favorite=dashboard['is_favorite'],
                    parameters_config=dashboard['parameters_config'],
                    drilldown_config=dashboard['drilldown_config'],
                    freeform_tags=dashboard['freeform_tags'],
                    defined_tags=dashboard['defined_tags'])
            )
            self.logger.info('SUCCESS: dashboard [%s] updated successfully' % update_management_dashboard_response.data.display_name)
        except Exception as ex:
            self.logger.error('ERROR: Failed to update [%s], [%s]' % (dashboard.display_name, ex))
            exit_code = 1
        return exit_code

    def is_already_replicated(self, saved_item, old_saved_items, saved_item_type):
        for old_item in old_saved_items:
            if old_item.display_name == saved_item.display_name and old_item.compartment_id == saved_item.compartment_id:
                current_saved_item_time_updated = saved_item.time_updated
                old_saved_item_time_updated = old_item.time_updated
                if old_saved_item_time_updated >= current_saved_item_time_updated:
                    self.logger.info('saved_item [%s] is already replicated' % saved_item.display_name)
                else:
                    saved_item_dict = self.convert_management_type_obj_to_dict(saved_item)
                    saved_item_dict['id'] = old_item.id 
                    if saved_item_type == 'saved_search':
                        exit_code = self.update_saved_search_in_region(saved_item_dict)
                        if exit_code != 0:
                            self.failed_saved_search_list(saved_item_dict['display_name'])
                    if saved_item_type == 'dashboard':
                        exit_code = self.update_dashboard_in_region(saved_item_dict)
                        if exit_code != 0:
                            self.failed_dashboard_list(saved_item_dict['display_name'])
                return True  
        return False

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
            replication_count = 0
            for saved_search in saved_search_list:                                          
                if not self.is_already_replicated(saved_search, replicated_saved_searches, 'saved_search'):
                    saved_search_dict = self.convert_management_type_obj_to_dict(saved_search)
                    create_exit_code = self.create_saved_search_in_region(saved_search_dict)
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
        dashboard_id_map = self.collect_dashboard_ids(dashboards_list)
        self.export_dashboards(dashboard_id_map, base_region)
        for region in region_list:
            self.import_dashboards(region)

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

    def backup_saved_search(self, base_region):
        self.logger.info('======================================================')
        self.logger.info('         Backup store of saved searches started           ')
        self.logger.info('======================================================')
        self.management_dashboard_client.base_client.set_region(base_region)
        list_exit_code, saved_search_list = self.list_saved_searches(base_region)
        if list_exit_code != 0:
            raise Exception('Failed to fetch saved search list from home region [%s]' % base_region)
        if len(saved_search_list) == 0:
            self.logger.info('No save searches are present in the compartment')
            return
        for saved_search in saved_search_list:
            object_name = saved_search.display_name
            object_location = '/%s/%s' % (SAVED_SEARCH_FOLDER,object_name)
            upload_exit_code = self.put_object_in_object_storage(object_location, str(saved_search))
            if upload_exit_code != 0:
                self.failed_saved_search_list(saved_search.display_name)

    def backup_dashboard(self, base_region):
        self.logger.info('======================================================')
        self.logger.info('         Backup store of dashboards started           ')
        self.logger.info('======================================================')
        self.management_dashboard_client.base_client.set_region(base_region)
        list_exit_code, dashboards_list = self.list_dashboards(base_region)
        if list_exit_code != 0:
            raise Exception('Failed to fetch dashboard list from home region [%s]' % base_region)
        if len(dashboards_list) == 0:
            self.logger.info('No dashboards are present in the compartment')
            return
        dashboard_details = self.get_dashboard_details(dashboards_list)   
        for dashboard in dashboard_details:
            object_name = dashboard.display_name
            object_location = '/%s/%s' % (DASHBOARD_fOLDER, object_name)
            upload_exit_code = self.put_object_in_object_storage(object_location, str(dashboard))
            if upload_exit_code != 0:
                self.failed_dashboard_list.append(dashboard.display_name)
        
    def restore_dashboard(self, base_region):
        dashboard_obj = '/%s/%s' % (DASHBOARD_fOLDER, self.options.object_name)
        dashboard_version = self.options.object_version
        get_object_exit_code , dashboard = self.get_object_from_object_storage(dashboard_obj, dashboard_version)
        if get_object_exit_code != 0:
            raise Exception('Failed to get dashboard object [%s]' % dashboard_obj)
        dashboard_version = self.options.object_version if self.options.object_version is not None else 'latest'
        dashboard['display_name'] = '%s-%s' % (dashboard['display_name'], dashboard_version)
        self.management_dashboard_client.base_client.set_region(base_region)
        restore_exit_code = self.create_dashboard_in_region(dashboard)
        if restore_exit_code != 0:
            raise Exception('Failed to restore dashboard [%s] in home region [%s]' % (self.options.object_name ,base_region)) 

    def restore_saved_search(self, base_region):
        saved_search_obj = '/%s/%s' % (SAVED_SEARCH_FOLDER,self.options.object_name)
        saved_search_version = self.options.object_version 
        get_object_exit_code , saved_search = self.get_object_from_object_storage(saved_search_obj, saved_search_version)
        if get_object_exit_code != 0:
            raise Exception('Failed to get saved search [%s]' % saved_search_obj)
        saved_search_version = self.options.object_version if self.options.object_version is not None else 'latest'
        saved_search['display_name'] = '%s-%s' % (saved_search['display_name'], saved_search_version)
        self.management_dashboard_client.base_client.set_region(base_region)
        restore_exit_code = self.create_saved_search_in_region(saved_search)
        if restore_exit_code != 0:
            raise Exception('Failed to restore saved search [%s] in home region [%s]' % (self.options.object_name ,base_region))

    def cross_region_replication(self):
        exit_code = 0 
        try:
            region_exit_code, base_region, region_list = self.get_regions()
            if self.options.base_region is not None:
                region_list.append(base_region)
                base_region = self.options.base_region
                region_list.remove(base_region)
            region_list = ['us-phoenix-1']
            if region_exit_code == 1:
                raise Exception('Failed to fetch regions list')
            if self.options.type == 'dashboard':
                # self.replicate_saved_search_cross_region(base_region, region_list)
                self.replicate_dashboard_cross_region(base_region, region_list)
            elif self.options.type == 'saved_search':
                self.replicate_saved_search_cross_region(base_region, region_list)
            elif self.options.type == 'log-source':
                self.replicate_log_source_cross_region(base_region, region_list)
            else:
                self.logger.error('ERROR: Please provide valid replication type')
                exit_code = 1

            if len(self.failed_saved_search_list) > 0:
                self.logger.error('Saved searches failed to replicate %s' % self.failed_saved_search_list)

            if len(self.failed_dashboard_list) > 0:
                self.logger.error('Dashboards failed to replicate %s' % self.failed_dashboard_list)           
        except Exception as ex:
            self.logger.error('ERROR: Failed to perform cross region replication [%s]' % ex)
            exit_code = 1
        finally:
            clean_up(LOG_SOURCE_ZIP_FILE)
        return exit_code

    def backup_saved_item(self):
        exit_code = 0
        try:
            region_exit_code, base_region, region_list = self.get_regions()
            if region_exit_code == 1:
                raise Exception('Failed to fetch regions list')
            if self.options.type == 'dashboard':
                self.backup_saved_search(base_region)
                self.backup_dashboard(base_region)
            elif self.options.type == 'saved_search':
                self.backup_saved_search(base_region)
            else:
                self.logger.error('ERROR: Please provide valid backup type')
                exit_code = 1

            if len(self.failed_saved_search_list) > 0:
                self.logger.error('Saved searches failed to backup %s' % self.failed_saved_search_list)

            if len(self.failed_dashboard_list) > 0:
                self.logger.error('Dashboards failed to backup %s' % self.failed_dashboard_list)
        except Exception as ex:
            self.logger.error('ERROR: Failed to store the backup in object storage [%s]' % ex)
            exit_code = 1
        return exit_code

    def restore_saved_item(self):
        exit_code = 0
        try:
            region_exit_code, base_region, region_list = self.get_regions()
            if region_exit_code == 1:
                raise Exception('Failed to fetch regions list')
            if self.options.type == 'dashboard':
                self.restore_dashboard(base_region)
            elif self.options.type == 'saved_search':
                self.restore_saved_search(base_region)
            else:
                self.logger.error('ERROR: Please provide valid restore type')
                exit_code = 1
        except Exception as ex:
            self.logger.error('ERROR: Failed to restore the backup from object storage [%s]' % ex)
            exit_code = 1
        return exit_code

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

def execute_command(cmd, shell=True, in_params=None, env=None, timeout=None):
    error = None
    output = None
    exit_code = -1

    if env is not None:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=shell, env=env, encoding='utf8')
    else:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=shell, encoding='utf8')
    output, error = process.communicate(in_params, timeout=timeout)
    exit_code = process.returncode
    return output, error, exit_code

def init(arg_list=[]):
    class MyParser(optparse.OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    example_usage = '''
     # if want to replicate from default home region us-ashburn-1
     # To replicate saved searches cross regions
     python manage_saved_item.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # To replicate dashboards cross regions
     python manage_saved_item.py --replicate --type dashboard  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace>
     # if want to replicate from base region other than default home region us-ashburn-1
     # To replicate saved searches cross regions
     python manage_saved_item.py --replicate --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
     # To replicate dashboards cross regions
     python manage_saved_item.py --replicate --type dashboard  --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
     # To replicate log sources cross regions
     python manage_saved_item.py --replicate --type log-source --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> --base-region <base_region>
     # To store backup of the saved search
     python manage_saved_item.py --backup --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> -b <bucket_name>
     # To store backup of the dashboard
     python manage_saved_item.py --backup --type dashboard --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> -b <bucket_name>
     # To restore saved search from object storage , if we don't provide the version id it will restore the latest saved search.
     python manage_saved_item.py --restore --type saved_search --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> -b <bucket_name> -o <saved_search_name> -v <saved_search_version>
     # To restore dashboard from object storage , if we don't provide the version id it will restore the latest dashboard.
     python manage_saved_item.py --restore --type dashboard --compartment_ocid <compartment_ocid> --tenancy_ocid <tenancy_ocid> --tenancy_namespace <tenancy_namespace> -b <bucket_name> -o <dashboard_name> -v <dashboard_version>
    '''
    parser = MyParser(version='%prog 1.0.0', epilog=example_usage)
    parser.add_option('--operation_type', action='store', dest='operation_type', type='string',
                      default='manage_saved_item', help='Execution Operation Type')
    parser.add_option('--replicate', action='store_true', dest='replicate', default=False, 
                      help='replicate saved searches and dashboards into cross regions')
    parser.add_option('-t', '--type', action='store', dest='type', type='string', default=None,
                      help='Type of saved item EX: saved search or dashboard or log source')
    parser.add_option('--compartment_ocid', action='store', dest='host_tenancy_logging_compartment_ocid', type='string', default= DEFAULT_HOST_TENANCY_LOGGING_COMPARTMENT_OCID,
                      help='host tenancy logging compartment ocid. The default value is OCETelemetry compartment ocid')
    parser.add_option('--tenancy_ocid', action='store', dest='host_tenancy_ocid', type='string', default=DEFAULT_HOST_TENANCY_OCID,
                      help='host tenancy ocid.The default value is oce0003 tenancy  ocid')
    parser.add_option('--tenancy_namespace', action='store', dest='host_tenancy_namespace', type='string', default=DEFAULT_NAMESPACE,
                      help='host tenancy namespace. The default namespace value is oce0003')
    parser.add_option('--base-region', action="store", dest="base_region", type="string", default=None,
                      help='The region from which saved items replicated to other regions')
    parser.add_option('--backup', action='store_true', dest='backup', default=False,
                      help='store the backup of saved item in the object storage')
    parser.add_option('--restore', action='store_true', dest='restore', default=False,
                      help='restore saved item from object storage')
    parser.add_option('-b', '--bucket-name', action='store', default=None, dest='bucket_name', type='string', 
                      help='Name of the bucket to store saved item')
    parser.add_option('-o', '--object-name', action='store', default=None, dest='object_name', type='string', 
                      help='Name of the object to restore')
    parser.add_option('-v', '--object-version', action='store', default=None, dest='object_version', type='string', 
                      help='Version of the object to restore')

    if arg_list:
        options, args = parser.parse_args(arg_list)
    else:
        options, args = parser.parse_args()
    return options, args, parser      

def main(arg_list=[]):
    exit_code = 0
    missing_args = False
    options, args, parser = init(arg_list)
    if not options.replicate and not options.backup and not options.restore:
        parser.print_help()
        exit_code = 1
        return exit_code
    
    if options.replicate:
        if options.type is None:
            print("Missing type option. Usage --type <saved_item>")
            missing_args = True
    if options.backup:
        if options.type is None:
            print("Missing type option. Usage --type <saved_item>")
            missing_args = True
        if options.bucket_name is None:
            print("Missing bucket-name option. Usage -b <bucket_name>")
            missing_args = True
    if options.restore:
        if options.type is None:
            print("Missing type option. Usage --type <saved_item>")
            missing_args = True
        if options.bucket_name is None:
            print("Missing bucket-name option. Usage -b <bucket_name>")
            missing_args = True
        if options.object_name is None:
            print("Missing object-name option. Usage -o <saved_item_name>")
            missing_args = True
    if missing_args:
        parser.print_help()
        exit_code = 1
        return exit_code


    try:
        logs_dir = os.path.join(DEFAULT_LOG_DIR_BASE)
        create_dirs(logs_dir)
        logger = get_logger(options.operation_type, logs_dir)
        manager = SavedItemManager(options, logger)
        
        if options.replicate:
            exit_code = manager.cross_region_replication()
        if options.backup:
            exit_code = manager.backup_saved_item()
        if options.restore:
            exit_code = manager.restore_saved_item()

        if exit_code == 0:
            logger.info('Log Analytics saved item operation completed successfully.')
        else:
            logger.error('Log Analytics saved item operation Failed to complete.')
    except Exception as ex:
        exit_code = 1
        traceback.print_exc()
    return exit_code


if __name__ in ['main', '__main__']:
    sys.exit(main())
