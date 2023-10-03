from airgen.types import Vector3r, Quaternionr, GeoPoint
import math

# Radius of the Earth in meters
R_EARTH = 6371000
EARTH_SEMI_MAJOR_AXIS = R_EARTH
FLATTENING = 1.0 / 298.0
ECC = 0.08181919084
ECC_SQUARED = ECC * ECC
EARTH_SEMI_MINOR_AXIS = EARTH_SEMI_MAJOR_AXIS * (1 - FLATTENING)


def lla2ecef(pos: GeoPoint) -> Vector3r:
    # pylint: disable=C0103
    """
    Convert LLA to ECEF. Units on latitude and longitude are degrees and units on
    altitude are meters.
    """

    clat = math.cos(pos.latitude * math.pi / 180)
    clon = math.cos(pos.longitude * math.pi / 180)
    slat = math.sin(pos.latitude * math.pi / 180)
    slon = math.sin(pos.longitude * math.pi / 180)

    ne = EARTH_SEMI_MAJOR_AXIS / math.sqrt(1 - (ECC_SQUARED * slat**2))
    h = ne + pos.altitude

    x = h * clat * clon
    y = h * clat * slon
    z = (ne * (1 - ECC_SQUARED) + pos.altitude) * slat

    return Vector3r(x, y, z)


def ecef2ned(ecef_pos: Vector3r, ref: GeoPoint) -> Vector3r:
    # pylint: disable=C0103
    """
    Convert ECEF to NED. Units on reference latitude and longitude are degrees.
    Units on reference altitude and the ECEF position are meters.
    """

    ref_ecef = lla2ecef(ref)

    relx = ecef_pos.x_val - ref_ecef.x_val
    rely = ecef_pos.y_val - ref_ecef.y_val
    relz = ecef_pos.z_val - ref_ecef.z_val

    clat = math.cos(ref.latitude * math.pi / 180)
    clon = math.cos(ref.longitude * math.pi / 180)
    slat = math.sin(ref.latitude * math.pi / 180)
    slon = math.sin(ref.longitude * math.pi / 180)

    n = -slat * clon * relx + -slat * slon * rely + clat * relz
    e = -slon * relx + clon * rely
    d = -clat * clon * relx + -clat * slon * rely + -slat * relz

    return Vector3r(n, e, d)


def ned2ecef(ned_pos: Vector3r, ref: GeoPoint) -> Vector3r:
    # pylint: disable=C0103
    """
    Convert NED to ECEF. Units on reference latitude and longitude are radians.
    Units on reference altitude and NED position are meters.
    """

    ref_ecef = lla2ecef(ref)

    clat = math.cos(ref.latitude)
    clon = math.cos(ref.longitude)
    slat = math.sin(ref.latitude)
    slon = math.sin(ref.longitude)

    x = -slat * clon * ned_pos.x_val + -slon * ned_pos.y_val + -clat * clon * ned_pos.z_val
    y = -slat * slon * ned_pos.x_val + clon * ned_pos.y_val + -clat * slon * ned_pos.z_val
    z = clat * ned_pos.x_val + -slat * ned_pos.z_val

    return Vector3r(x + ref_ecef.x_val, y + ref_ecef.y_val, z + ref_ecef.z_val)


def ecef2lla(ecef: Vector3r) -> GeoPoint:
    # pylint: disable=C0103
    """Convert ECEF (m, m, m) to LLA (deg, deg, m)"""
    lla = GeoPoint(0, 0, 0)

    a = EARTH_SEMI_MAJOR_AXIS
    e2 = ECC_SQUARED
    a1 = a * e2
    a2 = a1 * a1
    a3 = a1 * e2 * 0.5
    a4 = 5 * a2 * 0.5
    a5 = a1 + a3
    a6 = 1 - e2

    zp = abs(ecef.z_val)
    w2 = ecef.x_val**2 + ecef.y_val**2
    w = math.sqrt(w2)
    z2 = ecef.z_val**2
    r2 = w2 + z2
    r = math.sqrt(r2)

    if r < 100000:
        return GeoPoint(0, 0, 1e-7)

    lla.longitude = math.atan2(ecef.y_val, ecef.x_val)

    s2 = z2 / r2
    c2 = w2 / r2
    u = a2 / r
    v = a3 - a4 / r

    if c2 > 3:
        s = (zp / r) * (1 + c2 * (a1 + u + s2 * v) / r)
        lla.latitude = math.asin(s)
        ss = s * s
        c = math.sqrt(1 - ss)
    else:
        c = (w / r) * (1 - s2 * (a5 - u - c2 * v) / r)
        lla.latitude = math.acos(c)
        ss = 1 - c * c
        s = math.sqrt(ss)

    g = 1 - e2 * ss
    rg = a / math.sqrt(g)
    rf = a6 * rg
    u = w - rg * c
    v = zp - rf * s
    f = c * u + s * v
    m = c * v - s * u
    p = m / (rf / g + f)

    lla.latitude = lla.latitude + p
    lla.altitude = f + m * p * 0.5
    if ecef.z_val < 0:
        lla.altitude = -lla.altitude

    return lla