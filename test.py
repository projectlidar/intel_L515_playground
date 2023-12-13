import pyrealsense2 as rs

pipeline = rs.pipeline()
pipeline.start()

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth:
            continue

        coverage = [0]*64
        for y in range(480):
            for x in range(640):
                dist = depth.get_distance(x, y)
                if 0 < dist and dist < 1:
                    coverage[x//10] += 1

            if y % 20 is 19:
                line = ""
                for c in coverage:
                    line += " .',;:clodxkOBXW"[c//13]
                coverage = [0]*64
                print(line)
        print("--------------------------------------------------")

finally:
    pipeline.stop()
