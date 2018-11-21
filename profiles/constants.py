SMART = 0
GLOBE = 1
SUN = 2
PLDT = 5
OTHER = 6

PHONE_CARRIERS = (
    (PLDT, "PLDT"),
    (SMART, "Smart/Talk N Text"),
    (GLOBE, "Globe/Touch Mobile"),
    (SUN, "Sun Cellular"),
    (OTHER, "Other")
)


PHONE_NAME_CHOICES = (
    ('Mobile', 'Mobile'),
    ('Home', 'Home'),
    ('Work', 'Work'),
)


MOBILE_CARRIER_PREFIXES = {
    SMART: [
        907, 908, 909, 910, 912, 918, 919, 920, 921, 928, 929, 930, 938, 939, 989
    ],
    GLOBE: [
        905, 906, 915, 916, 917, 925, 926, 927, 935, 936, 937, 996, 997
    ],
    SUN: [
        922, 923, 932, 933
    ]
}