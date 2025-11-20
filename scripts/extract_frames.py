import cv2
import os
import argparse
import subprocess
import json

def get_video_rotation_ffprobe(video_path):
    """
    Usa ffprobe (de FFmpeg) para leer los metadatos de rotación reales.
    Si no existe rotación, devuelve 0.
    """
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream_tags=rotate",
            "-of", "json",
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info = json.loads(result.stdout)
        rotation = int(info["streams"][0]["tags"].get("rotate", 0))
        print(f"[INFO] Rotación detectada por metadatos: {rotation}°")
        return rotation
    except Exception as e:
        print(f"[WARN] No se pudo leer rotación con ffprobe ({e}) — asumiendo 0°")
        return 0

def rotate_frame(frame, rotation):
    """Aplica la rotación detectada al frame."""
    if rotation == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotation == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif rotation == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame

def extract_frames(video_path, base_output_dir, fps=5, max_frames=None):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(base_output_dir, video_name)
    os.makedirs(output_dir, exist_ok=True)

    rotation = get_video_rotation_ffprobe(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] No se pudo abrir el vídeo: {video_path}")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = int(video_fps / fps) if fps < video_fps else 1

    frame_count, saved_count = 0, 0
    print(f"[INFO] Extrayendo frames de '{video_name}' a {fps} FPS...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # 🔄 Corrige orientación solo si el vídeo lo requiere
            frame = rotate_frame(frame, rotation)

            output_path = os.path.join(output_dir, f"{video_name}_{saved_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            if max_frames and saved_count >= max_frames:
                break
        frame_count += 1

    cap.release()
    print(f"[OK] {saved_count} frames guardados correctamente en '{output_dir}'\n")

def process_videos(input_dir, output_dir, fps=5, max_frames=None):
    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]

    if not video_files:
        print("[ERROR] No se encontraron vídeos en la carpeta especificada.")
        return

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        extract_frames(video_path, output_dir, fps=fps, max_frames=max_frames)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraer frames corrigiendo orientación real del vídeo")
    parser.add_argument("--input_dir", required=True, help="Carpeta con los vídeos")
    parser.add_argument("--output_dir", required=True, help="Carpeta donde guardar los frames")
    parser.add_argument("--fps", type=int, default=5, help="Frames por segundo (default: 5)")
    parser.add_argument("--max_frames", type=int, default=None, help="Máximo de frames por vídeo (opcional)")
    args = parser.parse_args()

    process_videos(args.input_dir, args.output_dir, fps=args.fps, max_frames=args.max_frames)
