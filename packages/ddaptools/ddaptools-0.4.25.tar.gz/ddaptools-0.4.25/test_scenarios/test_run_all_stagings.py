from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *



def run_procesing(staging_guid = "42c6cd4b-a6ea-4087-ab6a-b8b5bed8b256"):
    """
    1. Email event.
    2. Publishes in database should result in updated start and updated endtime.
    """
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }

    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)

    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)

    # Salesforce Sample:  588e876e-31e6-91d4-863f-e0986fd90dad
    processor = PostgresS3ConnectorBasedCommonProcessor(
        
        job_parameters={"guid": staging_guid},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database




def test_multiple():
    # Query all staging events guids
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }
    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)
    all_staging_events_guids = organizationDBProvider.get_all_staging_events_guids(organization_guid='123e4567-e89b-12d3-a456-1231231')
    print(all_staging_events_guids)
    for staging_guid in all_staging_events_guids:
        print("Processing: ", staging_guid)
        run_procesing(staging_guid=staging_guid)






