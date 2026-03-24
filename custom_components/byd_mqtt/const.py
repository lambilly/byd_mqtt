"""Constants for BYD MQTT integration."""

DOMAIN = "byd_mqtt"
DEFAULT_TOPIC = "/carInfo"
DEVICE_NAME = "比亚迪"
DEVICE_MANUFACTURER = "BYD"
DEVICE_MODEL = "王朝系列"
DEVICE_ID = "byd_car"

CONF_TOPIC = "topic"
CONF_RESET_CACHE = "reset_cache"

SERVICE_RESET_CACHE = "reset_cache"

# 传感器定义
SENSORS = [
    ("byd_vin", "车架号", None, None, None),
    ("byd_range", "剩余续航", "km", "distance", None),
    ("byd_soc", "剩余电量", "%", "battery", None),
    ("byd_energy", "剩余能量", "kWh", None, None),
    ("byd_mileage", "总里程", "km", "distance", "total_increasing"),
    ("byd_temp_out", "车外温度", "°C", "temperature", None),
    ("byd_temp_in", "车内温度", "°C", "temperature", None),
    ("byd_humidity", "车内湿度", "%", "humidity", None),
    ("byd_door_lock", "门锁状态", None, None, None),
    ("byd_seatbelt", "主驾安全带", None, None, None),
    ("byd_power", "空调开关", None, None, None),
    ("byd_ac", "A/C开关", None, None, None),
    ("byd_wind", "风量档级", None, None, None),
    ("byd_defrost_front", "前除霜", None, None, None),
    ("byd_defrost_rear", "后除霜", None, None, None),
    ("byd_speed", "车速", "km/h", "speed", None),
    ("byd_moto_speed", "电机转速", "rpm", None, None),
    ("byd_wheel_angle", "方向盘角度", "°", None, None),
    ("byd_brake_depth", "制动深度", "%", None, None),
    ("byd_accelerate", "油门深度", "%", None, None),
    ("byd_update_time", "更新时间", None, None, None),
]

# 传感器图标映射
SENSOR_ICONS = {
    "byd_vin": "mdi:card-account-details",
    "byd_energy": "mdi:battery-high",
    "byd_wind": "mdi:fan",
    "byd_moto_speed": "mdi:engine",
    "byd_wheel_angle": "mdi:steering",
    "byd_brake_depth": "mdi:car-brake-hold",
    "byd_accelerate": "mdi:car-accelerator",
    "byd_update_time": "mdi:clock",
    "byd_door_lock": "mdi:car-door-lock",
    "byd_seatbelt": "mdi:seatbelt",
    "byd_power": "mdi:air-conditioner",
    "byd_ac": "mdi:snowflake",
    "byd_defrost_front": "mdi:car-defrost-front",
    "byd_defrost_rear": "mdi:car-defrost-rear",
}

# 聚合传感器
AGGREGATE_SENSORS = {
    "tyre_pressure": {
        "name": "轮胎气压",
        "unit": "kPa",
        "device_class": None,
        "state_class": None,
        "icon": "mdi:car-tire-pressure",
    },
    "tyre_temp": {
        "name": "轮胎温度",
        "unit": "°C",
        "device_class": None,
        "state_class": None,
        "icon": "mdi:thermometer",
    },
}

BINARY_SENSORS = [
    ("byd_windows", "车窗状态"),
]

BINARY_SENSOR_ICONS = {
    "byd_windows": "mdi:car-window",
}