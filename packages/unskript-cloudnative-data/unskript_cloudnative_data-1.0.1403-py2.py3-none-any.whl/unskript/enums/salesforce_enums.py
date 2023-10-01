from unskript.enums.enum_by_name import EnumByName
import enum


@enum.unique
class Status(str, EnumByName):
    NEW = "New"
    WORKING = "Working"
    ESCALATED = "Escalated"


@enum.unique
class CaseOrigin(str, EnumByName):
    PHONE = 'Phone'
    EMAIL = 'Email'
    WEB = "Web"


@enum.unique
class CaseType(str, EnumByName):
    MECHANICAL = 'Mechanical'
    ELECTRICAL = 'Electrical'
    ELECTRONIC = 'Electronic'
    STRUCTURAL = 'Structural'


@enum.unique
class Priority(str, EnumByName):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'


@enum.unique
class CaseReason(str, EnumByName):
    INSTALLATION = 'Installation'
    EQUIPMENTCOMPLEXITY = 'Equipment Complexity'
    PERFORMANCE = 'Performance'
    BREAKDOWN = 'Breakdown'
    EQUIPMENTDESIGN = 'Equipment Design'
    FEEDBACK = 'Feedback'
    OTHER = 'Other'


@enum.unique
class PotentialLiability(str, EnumByName):
    NO = 'No'
    YES = 'Yes'


@enum.unique
class SLAViolation(str, EnumByName):
    NO = 'No'
    YES = 'Yes'


