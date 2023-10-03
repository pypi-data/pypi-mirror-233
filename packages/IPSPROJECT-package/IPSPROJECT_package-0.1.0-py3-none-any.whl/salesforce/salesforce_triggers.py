# from django.db import models
from django.db.models.signals import pre_save, post_save
# from simple_salesforce.exceptions import SalesforceError
from .salesforce_trigger_handler import insertOpportunity,updateOpportunity
from django.dispatch import receiver
# from simple_salesforce import Salesforce
from salesforce.models import SalesforceOppportunity

@receiver(post_save, sender=SalesforceOppportunity)
def opportunity_post_save(sender, instance, created, **kwargs):
    # Trigger logic after insert/update goes here
    if created:
        insertOpportunity()
        print("Trigger called after insert")
    else:
        updateOpportunity()
        print("Trigger called after update")