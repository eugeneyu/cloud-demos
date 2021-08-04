# -*- coding = utf-8 -*-
# @Time : 2021/7/5 18:13
# @Author : lius
# @File :images_spritesheet.py
# @Software : PyCharm

# -*- coding: utf-8 -*-

import argparse
import json

from google.cloud.video import transcoder_v1beta1
from google.cloud.video.transcoder_v1beta1.services.transcoder_service import (
    TranscoderServiceClient,
)
from google.protobuf import duration_pb2 as duration

def create_job_with_periodic_images_spritesheet(
        project_id, location, input_uri, output_uri
):
    """Creates a job based on an ad-hoc job configuration that generates two spritesheets.

    Args:
        project_id: The GCP project ID.
        location: The location to start the job in.
        input_uri: Uri of the video in the Cloud Storage bucket.
        output_uri: Uri of the video output folder in the Cloud Storage bucket."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1beta1.types.Job()
    job.input_uri = input_uri
    job.output_uri = output_uri
    job.config = transcoder_v1beta1.types.JobConfig(
        # Create an ad-hoc job. For more information, see https://cloud.google.com/transcoder/docs/how-to/jobs#create_jobs_ad_hoc.
        # See all options for the job config at https://cloud.google.com/transcoder/docs/reference/rest/v1beta1/JobConfig.
        
        inputs=[
            transcoder_v1beta1.types.Input(
                key="caption_input0",
                uri="gs://alme-test-eyu/transcode_input/subs_2.srt",
            ),
            transcoder_v1beta1.types.Input(
                key="input0",
            )
        ],

        edit_list=[
            transcoder_v1beta1.types.EditAtom(
                key="atom0",
                inputs=[
                    "caption_input0",
                    "input0",
                ],
            ),
        ],

        elementary_streams=[
            # This section defines the output video stream.
            transcoder_v1beta1.types.ElementaryStream(
                key="video-stream0",
                video_stream=transcoder_v1beta1.types.VideoStream(
                    codec="h264",
                    height_pixels=360,
                    width_pixels=640,
                    bitrate_bps=550000,
                    frame_rate=60,
                ),
            ),
            # This section defines the output audio stream.
            transcoder_v1beta1.types.ElementaryStream(
                key="audio-stream0",
                audio_stream=transcoder_v1beta1.types.AudioStream(
                    codec="aac", bitrate_bps=64000
                ),
            ),
            # This section defines the output text stream.
            transcoder_v1beta1.types.ElementaryStream(
                key="text-stream0",
                text_stream=transcoder_v1beta1.types.TextStream(
                    codec="webvtt", 
                    #codec="cea608",
                    language_code="en-US",
                    #mapping=[
                    #    transcoder_v1beta1.types.TextStream.TextAtom(
                    #        key="atom0",
                    #        inputs=[
                    #            transcoder_v1beta1.types.TextStream.TextAtom.TextInput(
                    #                key="caption_input0",
                    #            ),
                    #        ],
                    #    ),
                    #]
                ),
            ),
        ],
        # This section multiplexes the output audio and video together into a container.
        #mux_streams=[
        #    transcoder_v1beta1.types.MuxStream(
        #        key="sd",
        #        container="mp4",
        #        elementary_streams=["video-stream0", "audio-stream0", "text-stream0"],
        #    ),
        #],
        mux_streams=[
            transcoder_v1beta1.types.MuxStream(
                key="sd",
                container="ts",
                elementary_streams=["video-stream0","audio-stream0"],
                #segment_settings=transcoder_v1beta1.types.SegmentSettings(
                #    segment_duration=duration.Duration(seconds=6),
                #    individual_segments=True
                #),
            ),
            #transcoder_v1beta1.types.MuxStream(
            #    key="audio",
            #    container="fmp4",
            #    elementary_streams=["audio-stream0"],
            #    segment_settings=transcoder_v1beta1.types.SegmentSettings(
            #        segment_duration=duration.Duration(seconds=5),
            #        individual_segments=True
            #    ),
            #),
            transcoder_v1beta1.types.MuxStream(
                key="subtitle",
                container="vtt",
                elementary_streams=["text-stream0"],
                segment_settings=transcoder_v1beta1.types.SegmentSettings(
                    segment_duration=duration.Duration(seconds=6),
                    individual_segments=True
                ),
            ),
        ],

        manifests=[
            transcoder_v1beta1.types.Manifest(
                file_name="master.m3u8",
                type_="HLS",
                mux_streams=["sd","subtitle"],
            )
        ],

        # Generate two sprite sheets from the input video into the GCS bucket. For more information, see
        # https://cloud.google.com/transcoder/docs/how-to/generate-spritesheet#generate_image_periodically.
        sprite_sheets=[
            # Generate a sprite sheet with 64x32px images. An image is taken every 7 seconds from the video.
            transcoder_v1beta1.types.SpriteSheet(
                file_prefix="4-3-",
                sprite_width_pixels=720,
                sprite_height_pixels=540,
                column_count=1,
                row_count=1,
                total_count=5,
                #interval=duration.Duration(
                #    seconds=7,
                #),
            ),
            # Generate a sprite sheet with 128x72px images. An image is taken every 7 seconds from the video.
            transcoder_v1beta1.types.SpriteSheet(
                file_prefix="16-9-",
                sprite_width_pixels=960,
                sprite_height_pixels=540,
                column_count=1,
                row_count=1,
                total_count=5,
                #interval=duration.Duration(
                #    seconds=7,
                #),
            ),
        ],
    )
    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


if __name__ == '__main__':
    project_id = 'youzhi-lab'
    #location = 'asia-east1'
    location = 'asia-east1'
    #input_uri = 'gs://orange-bucket-us-210426/video/anime/1/1_0/Digimon%20Adventure%2002%28BDRip%201080p%20Dual%20Audio%29%20Eng%20Dub.mkv'
    #input_uri = 'gs://orange-bucket-us-210426/video/anime/1/1_0/Digimon Adventure 54 (BDRip 1080p Dual Audio) Eng Dub.mkv'
    input_uri = "gs://alme-test-eyu/transcode_input/oasis/[P-O]_Pokemon_519_Diamond_&_Pearl_050_'Tag!_We're_it...!'_[R1-AtoMan]_[05CC7FD3].avi"
    #output_uri = 'gs://orange-backet-210419/screenshots/04/'
    output_uri = 'gs://hk-publish/transcode_output/oasis/20210716-2/'
    create_job_with_periodic_images_spritesheet(project_id, location, input_uri, output_uri)

