import math
import time
from rich.console import Console
from rich.live import Live

console = Console()

R = 12  # radius of globe
frames = 120  # how many rotation frames
density = " .:-=+*#%@"
density_len = len(density)

def render_frame(rot):
    output = []
    for y in range(-R, R):
        line = ""
        for x in range(-2*R, 2*R):
            z = math.sqrt(max(0, R**2 - (x/2)**2 - y**2))
            lon = math.atan2(z, x/2) + rot
            lat = math.asin(y / R)
            val = math.sin(lat) * math.cos(lon)
            shade = density[int((val + 1) / 2 * (density_len - 1))]
            line += shade
        output.append(line)
    return "\n".join(output)

with Live(refresh_per_second=10, console=console) as live:
    for i in range(frames):
        rot = (i / frames) * 2 * math.pi
        live.update(render_frame(rot))
        time.sleep(0.05)
import math
import time
from rich.console import Console
from rich.live import Live

console = Console()

R = 12
frames = 180
density = " .:-=+*#%@"
density_len = len(density)

# Real radio stations (name, latitude, longitude)
stations = [
    ("BBC Radio 1", 51.509865, -0.118092),
    ("NPR", 38.9072, -77.0369),
    ("Radio Mirchi", 19.0760, 72.8777),
    ("NHK Radio", 35.6895, 139.6917),
    ("Triple J", -33.8688, 151.2093),
]

def latlon_to_xyz(lat, lon):
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    x = math.cos(lat_r) * math.cos(lon_r)
    y = math.sin(lat_r)
    z = math.cos(lat_r) * math.sin(lon_r)
    return (x, y, z)

station_points = [latlon_to_xyz(lat, lon) for _, lat, lon in stations]

def render_frame(rot):
    output = []
    for y in range(-R, R):
        line = ""
        for x in range(-2*R, 2*R):
            z = math.sqrt(max(0, R**2 - (x/2)**2 - y**2))
            lon = math.atan2(z, x/2) + rot
            lat = math.asin(y / R)
            val = math.sin(lat) * math.cos(lon)
            shade = density[int((val + 1) / 2 * (density_len - 1))]
            line += shade
        output.append(list(line))

    # Project and draw station markers
    for sx, sy, sz in station_points:
        # rotate point
        rx = sx * math.cos(rot) - sz * math.sin(rot)
        rz = sx * math.sin(rot) + sz * math.cos(rot)
        # project to 2D screen
        if rz > 0:  # front side only
            px = int(R + rx * R)
            py = int(R - sy * R)
            if 0 <= py < len(output) and 0 <= px < len(output[0]):
                output[py][px] = "*"

    return "\n".join("".join(row) for row in output)

with Live(refresh_per_second=5, console=console) as live:
    for i in range(frames):
        rot = (i / frames) * 2 * math.pi
        frame = render_frame(rot)
        live.update(frame)
        if i % 30 == 0:  # print debug every few frames
            console.print(f"[cyan]Rotation {i}, rot={rot:.2f}[/cyan]")
        time.sleep(0.05)
