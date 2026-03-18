import json
import os
import urllib.parse
import boto3
from datetime import datetime

transcribe = boto3.client("transcribe")
s3 = boto3.client("s3")

OUTPUT_BUCKET = "voice2text-bucket/"
OUTPUT_PREFIX = "transcripts/"
LANGUAGE_CODE = "vi-VN"
OUTPUT_JOB = "transcripts_job/"

SUPPORTED_EXT = {".mp3", ".mp4", ".wav", ".flac", ".m4a", ".ogg", ".webm", ".amr"}

def guess_media_format(key: str):
    lower = key.lower()
    for ext in SUPPORTED_EXT:
        if lower.endswith(ext):
            return ext.lstrip(".")
    return None

def lambda_handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        media_format = guess_media_format(key)
        if not media_format:
            print(f"Skip unsupported file: s3://{bucket}/{key}")
            continue

        # Tạo job name duy nhất, tránh đụng tên
        safe_key = key.replace("/", "-").replace(" ", "_")
        job_name = f"tx-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{safe_key}"[:200]

        media_uri = f"s3://{bucket}/{key}"
        self.client.upload_file(
                    self.file_name, 
                    self.bucket, 
                    self.object_name,
                    Callback = callback,
                    ExtraArgs={'ContentType': self.content_type}
                )
        resp = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=LANGUAGE_CODE,
            MediaFormat=media_format,
            Media={"MediaFileUri": media_uri},
            OutputBucketName=OUTPUT_BUCKET,
            OutputKey=f"{OUTPUT_PREFIX}{job_name}.json"
        )

        print(json.dumps({
            "job_name": job_name,
            "media_uri": media_uri,
            "response": resp["TranscriptionJob"]["TranscriptionJobStatus"]
        }))