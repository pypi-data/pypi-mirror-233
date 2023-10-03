import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ZatcaKey(models.Model):
    PRODUCTION_CSID_ONBOARDING = 'PRODUCTION_CSID_ONBOARDING'
    PRODUCTION_CSID_RENEWING = 'PRODUCTION_CSID_RENEWING'
    COMPLIANCE_CSID = 'COMPLIANCE_CSID'

    TYPE_CHOICES = [
        (PRODUCTION_CSID_ONBOARDING, 'Production CSID Onboarding',),
        (PRODUCTION_CSID_RENEWING, 'Production CSID Renewing',),
        (COMPLIANCE_CSID, 'Compliance CSID',),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=5000, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    meta_data = models.JSONField(blank=True, null=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "takamol_einvoice.zatca_keys"


class ZatcaLog(models.Model):
    """
        This model will log all communication between Server and Zatca
    """
    COMPLIANCE_CSID = 'COMPLIANCE_CSID'
    COMPLIANCE_CHECK = 'COMPLIANCE_CHECK'
    PRODUCTION_CSID_ONBOARDING = 'PRODUCTION_CSID_ONBOARDING'
    PRODUCTION_CSID_RENEWING = 'PRODUCTION_CSID_RENEWING'
    REPORTING_INVOICE = 'REPORTING_INVOICE'

    REQUEST_TYPE_CHOICES = [
        (COMPLIANCE_CSID, 'Compliance CSID',),
        (COMPLIANCE_CHECK, 'Compliance Check',),
        (PRODUCTION_CSID_ONBOARDING, 'Production CSID Onboarding',),
        (PRODUCTION_CSID_RENEWING, 'Production CSID Renewing',),
        (REPORTING_INVOICE, 'Reporting Invoice',),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    req = models.JSONField(null=True, blank=True)
    res = models.JSONField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    request_type = models.CharField(max_length=50, null=True, blank=True, choices=REQUEST_TYPE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "takamol_einvoice.zatca_logs"
