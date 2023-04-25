data_add_coach = {
    "first_name": "Georgi",
    "last_name": "Iordanov",
    "phone_number": "+359899331198",
    "coach_type": "boxing"
}

data_admin_access_required = {
    "first_name": "Georgi",
    "last_name": "Iordanov",
    "phone_number": "+359899331198",
    "coach_type": "boxing"
}

data_buying_equipments = {
    "card_token": "tok_bg",
    "type_equipment": "boxing_equipment",
    "name": "Gosho",
    "email": "k.nenov96@abv.bg",
    "contact": "+359899331198",
    "region": "Varna"
}

data_buying_subscriptions = {
    "subscriber_info": {
        "first_name": "Remi", "last_name": "Emilov", "identity": "9609091062"},
    "email": "k.nenov9@abv.bg", "card_token": "tok_bg",
    "subscription_type": "boxing",
    "region": "Varna", "phone": "+359899331198"
}

response_buying_equipment_all_schema_fields_missing = {
    'message': {
        'card_token': ['Missing data for required field.'],
        'contact': ['Missing data for required field.'],
        'email': ['Missing data for required field.'],
        'name': ['Missing data for required field.'],
        'region': ['Missing data for required field.'],
        'type_equipment': [
            'Missing data for required field.']
    }
}

response_buying_subscriptions_all_schema_fields_missing = {
    'message': {
        'card_token': ['Missing data for required field.'],
        'email': ['Missing data for required field.'],
        'phone': ['Missing data for required field.'],
        'region': ['Missing data for required field.'],
        'subscriber_info': ['Missing data for required field.'],
        'subscription_type': ['Missing data for required field.']
    }
}

response_coach_panel_all_schema_fields_missing = {
    'message': {
        'coach_type': ['Missing data for required field.'],
        'first_name': ['Missing data for required field.'],
        'last_name': ['Missing data for required field.'],
        'phone_number': ['Missing data for required field.']
    }
}
