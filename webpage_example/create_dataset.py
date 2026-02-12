import rerun as rr

from math import tau
import numpy as np
from pathlib import Path
from rerun.utilities import build_color_spiral
from rerun.utilities import bounce_lerp

DESCRIPTION = """
# Rerun webpage example

Static screenshots and videos belong in the past. In this guide, we will walk through deploying a live, interactive webpage integrated with Rerun. By embedding a hosted Rerun viewer, you are not just showing your results — you are handing your audience the keys to explore your data in 3D, scrub through timelines, and inspect your model's logic in real-time.

In a fast-moving industry, the ability to provide an immersive, 'hands-on' demo is the difference between a project that gets glanced at and one that gets remembered. Here we will go through the steps to create your webpage with Rerun integrated, you will see that it is simple and quick process that does not take away valuable development or writing time.
"""

# Setup recording
recording_path = Path("recordings")
recording_name = "dna_structure.rrd"
recording_path.mkdir(parents=True, exist_ok=True)

rr.init("rerun_webpage_example")

# Spawn Rerun viewer
rr.spawn()

# Save to file instead of streaming to viewer
# rr.save(str(recording_path / recording_name))

rr.log(
    'description',
    rr.TextDocument(DESCRIPTION, media_type=rr.MediaType.MARKDOWN),
    static=True,
)

rr.set_time("stable_time", duration=0)

NUM_POINTS = 100

# Points and colors are both np.array((NUM_POINTS, 3))
points1, colors1 = build_color_spiral(NUM_POINTS)
points2, colors2 = build_color_spiral(NUM_POINTS, angular_offset=tau*0.5)

rr.log("dna/structure/left", rr.Points3D(points1, colors=colors1, radii=0.08))
rr.log("dna/structure/right", rr.Points3D(points2, colors=colors2, radii=0.08))

rr.log(
    "dna/structure/scaffolding",
    rr.LineStrips3D(np.stack((points1, points2), axis=1),
                    colors=[128, 128, 128])
)

offsets = np.random.rand(NUM_POINTS)
beads = [bounce_lerp(points1[n], points2[n], offsets[n])
         for n in range(NUM_POINTS)]
colors = [[int(bounce_lerp(80, 230, offsets[n] * 2))]
          for n in range(NUM_POINTS)]
rr.log(
    "dna/structure/scaffolding/beads",
    rr.Points3D(beads, radii=0.06, colors=np.repeat(colors, 3, axis=-1)),
)

time_offsets = np.random.rand(NUM_POINTS)

for i in range(400):
    time = i * 0.01
    rr.set_time("stable_time", duration=time)

    times = np.repeat(time, NUM_POINTS) + time_offsets
    beads = [bounce_lerp(points1[n], points2[n], times[n])
             for n in range(NUM_POINTS)]
    colors = [[int(bounce_lerp(80, 230, times[n] * 2))]
              for n in range(NUM_POINTS)]
    rr.log(
        "dna/structure/scaffolding/beads",
        rr.Points3D(beads, radii=0.06, colors=np.repeat(colors, 3, axis=-1)),
    )
    rr.log(
        "dna/structure",
        rr.Transform3D(rotation=rr.RotationAxisAngle(
            axis=[0, 0, 1], radians=time / 4.0 * tau)),
    )
