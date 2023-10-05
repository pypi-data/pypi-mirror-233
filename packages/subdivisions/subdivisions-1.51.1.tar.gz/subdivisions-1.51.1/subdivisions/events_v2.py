from enum import Enum


class OrderEvents(Enum):
    ORDER_PROPOSAL_REQUEST = "order_proposal_request"
    ORDER_PROPOSAL_CALCULATED = "order_proposal_calculated"
    ORDER_PROPOSAL_RECALCULATED = "order_proposal_recalculated"
    ORDER_PROPOSAL_ANALYZED = "order_proposal_analyzed"
    ORDER_PROPOSAL_AVAILABLE = "order_proposal_available"
    ORDER_PROPOSAL_ACCEPTED = "order_proposal_accepted"
    ORDER_PROPOSAL_REACCEPTED = "order_proposal_reaccepted"
    ORDER_PROPOSAL_REFUSED = "order_proposal_refused"
    ORDER_SCHEDULE_REQUEST = "order_schedule_request"
    ORDER_DISBURSEMENT_MADE = "order_disbursement_made"
    ORDER_ALLOCATION_SELECTED = "order_allocation_selected"
    ORDER_ALLOCATED = "order_allocated"


class ERPEvent(Enum):
    NEW_ERP_DATA_AVAILABLE = "new_erp_data_available"


class CustomerEvents(Enum):
    REGISTERED = "registered"
    DATA_SOURCE_CONNECTED = "data_source_connected"
    VALIDATION_FINISHED = "validation_finished"


class BankEvent(Enum):
    NEW_BOLETOS_ISSUED = "new_boletos_issued"
    BANK_ACCOUNT_STATUS = "bank_account_status"


class CollateralEvent(Enum):
    LOWER_COLLATERAL_APPROVED = "lower_collateral_approved"
