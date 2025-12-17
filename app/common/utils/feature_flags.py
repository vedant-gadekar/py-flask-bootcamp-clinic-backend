import os

def _is_enabled(env_key: str, default: str = "true") -> bool:
    return os.getenv(env_key, default).lower() == "true"


FEATURE_FLAGS = {
    #auth
    "registration": _is_enabled("FEATURE_REGISTRATION_ENABLED"),
    "login": _is_enabled("FEATURE_LOGIN_ENABLED"),
    
    # admin
    "create_department": _is_enabled("FEATURE_CREATE_DEPARTMENT"),
    "list_departments": _is_enabled("FEATURE_LIST_DEPARTMENTS"),
    "create_doctor": _is_enabled("FEATURE_CREATE_DOCTOR"),
    "list_doctors": _is_enabled("FEATURE_LIST_DOCTORS"),
    "assign_doctor": _is_enabled("FEATURE_ASSIGN_DOCTOR"),
    "view_appointments": _is_enabled("FEATURE_VIEW_APPOINTMENTS"),
    
    # availabaility
    "create_availability": _is_enabled("FEATURE_CREATE_AVAILABILITY"),
    "get_availability": _is_enabled("FEATURE_GET_AVAILABILITY"),

    # appointment
    "book_appointment": _is_enabled("FEATURE_BOOK_APPOINTMENT"),
    "cancel_appointment": _is_enabled("FEATURE_CANCEL_APPOINTMENT"),
    "list_member_appointments": _is_enabled("FEATURE_LIST_MEMBER_APPOINTMENTS"),  
    "list_doctor_appointments":  _is_enabled("FEATURE_LIST_DOCTOR_APPOINTMENTS"),
    
    # reimbursement
    "submit_claim": _is_enabled("FEATURE_SUBMIT_CLAIM"),
    "review_claim": _is_enabled("FEATURE_REVIEW_CLAIM"),
    "view_all_claims": _is_enabled("FEATURE_VIEW_ALL_CLAIMS"),
}
