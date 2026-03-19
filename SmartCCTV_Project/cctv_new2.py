import cv2
import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

from config import SETTINGS
from detector import Detector
from rules import (
    PERSON_CLASS_NAME,
    VEHICLE_CLASS_NAMES,
    person_likely_fallen,
    vehicle_stopped,
    crowding,
    bbox_center,
)
from utils import TrackHistory
from alert import send_sms, make_call

# ---------------- VIDEO PATH ----------------
VIDEO_PATH = r"C:\Users\Ponjanani\Desktop\Ponjanani\SmartCCTV_Project\SmartCCTV_Project\Videos\test2.mp4"

# ---------------- LOGS ----------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- CRASH PARAMETERS ----------------
CRASH_DISTANCE_THR = 150
SPEED_DROP_THR = 1.0
CRASH_COOLDOWN_FRAMES = 20

last_crash_frame = {}


def pair_key(a: int, b: int) -> Tuple[int, int]:
    return (a, b) if a <= b else (b, a)


def run(weights="yolov8n.pt", do_call=False):
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        raise RuntimeError(f"❌ Could not open video file: {VIDEO_PATH}")

    print("🚀 Smart CCTV running… press 'q' to quit")

    det = Detector(
        weights=weights,
        conf=SETTINGS.conf_thresh,
        iou=SETTINGS.iou_thresh
    )

    track_hist = TrackHistory(maxlen=30)
    static_counts: Dict[int, int] = {}
    last_speeds: Dict[int, float] = {}

    log_rows = []
    frames = 0
    last_fps_t = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            print("❌ Video ended.")
            break

        fh, fw = frame.shape[:2]
        frames += 1

        results = det.track(frame)
        res = results[0]
        annotated = res.plot()

        boxes = res.boxes
        names = det.model.names

        persons = 0
        suspicious_msgs: List[str] = []
        vehicle_tracks: Dict[int, dict] = {}

        # ---------------- DETECTIONS ----------------
        if boxes is not None:
            for b in boxes:
                cls_id = int(b.cls[0])
                cls_name = names.get(cls_id, str(cls_id))
                xyxy = b.xyxy[0].tolist()
                tid = int(b.id[0]) if b.id is not None else -1

                # PERSON
                if cls_name == PERSON_CLASS_NAME:
                    persons += 1
                    if person_likely_fallen(xyxy, frame_h=fh):
                        suspicious_msgs.append("Person possibly fallen")

                # VEHICLE
                if cls_name in VEHICLE_CLASS_NAMES and tid != -1:
                    center = bbox_center(xyxy)
                    track_hist.update(tid, center)
                    speed = track_hist.speed(tid)

                    vehicle_tracks[tid] = {
                        "center": center,
                        "speed": speed
                    }

                    prev = static_counts.get(tid, 0)
                    static_counts[tid] = prev + 1 if speed < 1.5 else 0

                    if vehicle_stopped(speed, static_counts[tid]):
                        suspicious_msgs.append(f"Vehicle #{tid} stopped abnormally")

        # ---------------- CROWDING ----------------
        if crowding(persons, frame_area=fw * fh):
            suspicious_msgs.append("Crowd density high")

        # ---------------- CRASH DETECTION ----------------
        tids = list(vehicle_tracks.keys())

        for i in range(len(tids)):
            for j in range(i + 1, len(tids)):
                a, b = tids[i], tids[j]

                c1 = vehicle_tracks[a]["center"]
                c2 = vehicle_tracks[b]["center"]

                dist = ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5

                sp_a = vehicle_tracks[a]["speed"]
                sp_b = vehicle_tracks[b]["speed"]

                prev_a = last_speeds.get(a, sp_a)
                prev_b = last_speeds.get(b, sp_b)

                sudden_stop = (prev_a - sp_a > SPEED_DROP_THR) or \
                              (prev_b - sp_b > SPEED_DROP_THR)

                if dist < CRASH_DISTANCE_THR and sudden_stop:
                    key = pair_key(a, b)
                    if frames - last_crash_frame.get(key, 0) > CRASH_COOLDOWN_FRAMES:
                        suspicious_msgs.append(
                            f"🚨 Vehicle collision detected between #{a} and #{b}"
                        )
                        last_crash_frame[key] = frames

        # ---------------- SAVE SPEEDS ----------------
        for tid, data in vehicle_tracks.items():
            last_speeds[tid] = data["speed"]

        # ---------------- ALERT ----------------
        if suspicious_msgs:
            msg = "⚠️ SmartCCTV Alert: " + "; ".join(sorted(set(suspicious_msgs)))
            print(msg)

            try:
                send_sms(msg)
                if do_call:
                    make_call(msg)
            except Exception as e:
                print("❌ Alert error:", e)

            log_rows.append({
                "time": pd.Timestamp.now().isoformat(),
                "event": msg,
                "persons": persons
            })

        # ---------------- FPS ----------------
        if frames % 15 == 0:
            now = time.time()
            fps = 15 / max(1e-6, (now - last_fps_t))
            last_fps_t = now
            cv2.putText(
                annotated,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # -------- REDUCE VIDEO HEIGHT --------
        HEIGHT_SCALE = 0.6
        new_width = annotated.shape[1]
        new_height = int(annotated.shape[0] * HEIGHT_SCALE)
        annotated = cv2.resize(annotated, (new_width, new_height))
        # ------------------------------------

        cv2.imshow("AI Smart CCTV (q to quit)", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ---------------- SAVE LOG ----------------
    if log_rows:
        df = pd.DataFrame(log_rows)
        ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        csv_path = LOG_DIR / f"events_{ts}.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Events saved -> {csv_path}")


if __name__ == "__main__":
    run(weights="yolov8n.pt", do_call=False)
