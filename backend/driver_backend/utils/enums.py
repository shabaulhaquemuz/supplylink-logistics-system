"""
Enums for Driver Backend
⭐ 8-Line Description of enums.py

This file defines all the enums (fixed value categories) used in the driver backend to represent different shipment and delivery states.

Enums help keep the system consistent by ensuring values like shipment status or customs status are always spelled correctly and predictable.

ShipmentStatus stores every stage a delivery can go through (pending, assigned, picked up, delivered, etc.).

ShipmentType and InternationalMode describe whether a shipment is domestic or international, and the mode of transport (air, sea, truck).

CustomsStatus tracks international cargo clearance progress at ports/airports.

FailureReason and DelayReason store the acceptable reasons for delivery failure or delays (traffic, wrong address, accident, etc.).

CODStatus helps track cash-on-delivery payments and whether the driver collected the money.

PortLocation provides a list of major Indian ports and airports, making international logistics handling easier and standardized.
"""
from enum import Enum

class ShipmentStatus(str, Enum):
    """Shipment status enum"""
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ShipmentType(str, Enum):
    """Shipment type enum"""
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"

class InternationalMode(str, Enum):
    """International shipment mode"""
    AIR = "air"
    SEA = "sea"
    TRUCK = "truck"

class CustomsStatus(str, Enum):
    """Customs clearance status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    CLEARED = "cleared"
    HELD = "held"

class FailureReason(str, Enum):
    """Delivery failure reasons"""
    RECIPIENT_NOT_AVAILABLE = "recipient_not_available"
    WRONG_ADDRESS = "wrong_address"
    PHONE_UNREACHABLE = "phone_unreachable"
    REFUSED_DELIVERY = "refused_delivery"
    ADDRESS_INCOMPLETE = "address_incomplete"
    OTHER = "other"

class DelayReason(str, Enum):
    """Traffic/delay reasons"""
    TRAFFIC_JAM = "traffic_jam"
    VEHICLE_BREAKDOWN = "vehicle_breakdown"
    WEATHER = "weather"
    ACCIDENT = "accident"
    CUSTOMS_DELAY = "customs_delay"
    OTHER = "other"

class CODStatus(str, Enum):
    """Cash on Delivery status"""
    PENDING = "pending"
    COLLECTED = "collected"
    NOT_APPLICABLE = "not_applicable"

class PortLocation(str, Enum):
    """Major Indian ports/airports"""
    MUMBAI_PORT = "mumbai_port"
    MUMBAI_AIRPORT = "mumbai_airport"
    DELHI_AIRPORT = "delhi_airport"
    CHENNAI_PORT = "chennai_port"
    CHENNAI_AIRPORT = "chennai_airport"
    KOLKATA_PORT = "kolkata_port"
    BANGALORE_AIRPORT = "bangalore_airport"
    HYDERABAD_AIRPORT = "hyderabad_airport"
    MUNDRA_PORT = "mundra_port"
    NHAVA_SHEVA_PORT = "nhava_sheva_port"