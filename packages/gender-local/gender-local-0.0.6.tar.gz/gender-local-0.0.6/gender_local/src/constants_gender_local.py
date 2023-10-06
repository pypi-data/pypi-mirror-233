from logger_local.LoggerComponentEnum import LoggerComponentEnum

class ConstantsGenderLocal:
    GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 201
    GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'gender-local-python-package'

    OBJECT_FOR_LOGGER_CODE = {
        'component_id': GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'tal.g@circ.zone'
    }

    OBJECT_FOR_LOGGER_TEST = {
        'component_id': GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': GENDER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'tal.g@circ.zone'
    }
