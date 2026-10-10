"""
manim_runner.py — Render a Manim scene and return the video bytes.
"""

import os
import subprocess
import tempfile


def render_manim_scene(scene_code: str, scene_class: str, quality: str = "low_quality"):
    """
    Render a Manim scene. Returns MP4 bytes, or None on failure.
    """
    with tempfile.TemporaryDirectory() as tmp:
        scene_file = os.path.join(tmp, "scene.py")
        with open(scene_file, "w") as f:
            f.write(scene_code)

        media_dir = os.path.join(tmp, "media")
        cmd = [
            "manim",
            "-ql",          # low quality = fast render
            "--media_dir", media_dir,
            scene_file,
            scene_class,
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, timeout=120
            )
        except subprocess.CalledProcessError as e:
            print("[manim] render failed:", e.stderr[-2000:])
            return None
        except subprocess.TimeoutExpired:
            print("[manim] render timed out")
            return None

        # Find the rendered .mp4
        for root, _, files in os.walk(media_dir):
            for f in files:
                if f.endswith(".mp4"):
                    with open(os.path.join(root, f), "rb") as fh:
                        return fh.read()

        print("[manim] no mp4 found")
        return None