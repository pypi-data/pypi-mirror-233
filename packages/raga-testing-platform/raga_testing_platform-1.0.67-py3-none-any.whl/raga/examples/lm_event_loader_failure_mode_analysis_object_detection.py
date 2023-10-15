import pathlib
from raga import *
import pandas as pd
import datetime

# def 

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    return StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/StopSign_Part1_event.json/data_points/{pathlib.Path(x).stem}/{x}")

def model_a_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_1_outputs"][0]["frame_id"]
    end_frame = row["model_1_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections


def model_b_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_1_outputs"][0]["frame_id"]
    end_frame = row["model_1_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections

def model_a_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_1_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_b_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_2_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_image_inference(row):
    AnnotationsV1 = ImageDetectionObject()
    for index, detection in enumerate(row["detections"]):
        AnnotationsV1.add(ObjectDetection(Id=detection["Id"], ClassId=0, ClassName=detection['ClassName'], Confidence=detection['Confidence'], BBox= detection['BBox'], Format=detection['Format']))
    return AnnotationsV1



def json_parser(event_1, event_2, model_1, model_2):
    event_1_df = pd.read_json(event_1)
    event_2_df = pd.read_json(event_2)
    model_1_df = pd.read_json(model_1)
    model_2_df = pd.read_json(model_2)
    event_1_df_exploded = event_1_df.explode('inputs')
    event_2_df_exploded = event_2_df.explode('inputs')
    model_1_df_exploded = model_1_df.explode('inputs')
    model_2_df_exploded = model_2_df.explode('inputs')
    attributes = event_2_df["attributes"].apply(pd.Series)
    event_2_df_exploded = pd.concat([event_2_df_exploded, attributes], axis=1)
    event_2_df_exploded.rename(columns={"outputs": "new_outputs"}, inplace=True)
    model_1_df_exploded.rename(columns={"outputs": "model_1_outputs"}, inplace=True)
    model_2_df_exploded.rename(columns={"outputs": "model_2_outputs"}, inplace=True)
    merged_df = pd.merge(event_1_df_exploded, event_2_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_1_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_2_df_exploded, on='inputs', suffixes=[None, "_model_2"])
    data_frame = pd.DataFrame()
    data_frame["videoId"] = merged_df["inputs"].apply(lambda x: StringElement(pathlib.Path(x).stem))
    data_frame["videoUrl"] = merged_df["inputs"].apply(lambda x: img_url(x))
    data_frame["timeOfCapture"] = merged_df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["sourceLink"] = merged_df["inputs"].apply(lambda x: StringElement(x))
    data_frame["dutyType"] = merged_df["dutyType"].apply(lambda x: StringElement(x))
    data_frame["time_of_day"] = merged_df["time_of_day"].apply(lambda x: StringElement(x))
    data_frame["weather"] = merged_df["weather"].apply(lambda x: StringElement(x))
    data_frame["scene"] = merged_df["scene"].apply(lambda x: StringElement(x))
    data_frame["tags"] = merged_df["tags"].apply(lambda x: StringElement(x))
    data_frame["complexEvent"] = merged_df.apply(model_a_inference, axis=1)
    data_frame["productionEvent"] = merged_df.apply(model_b_inference, axis=1)
    data_frame["complexModel"] = merged_df.apply(model_a_video_inference, axis=1)
    data_frame["productionModel"] = merged_df.apply(model_b_video_inference, axis=1)
    return data_frame.head(10)

def make_image_df(video_df:pd.DataFrame):
    df = data_frame_extractor(video_df)
    videos = df["videoId"]
    complex_model = df['complexModel']
    production_model = df['productionModel']
    data_frame_list = []
    for index, output in enumerate(complex_model):
        frames  = output['frames']
        video = videos[index]
        complex_model_outputs = complex_model[index]['frames']
        production_model_outputs = production_model[index]['frames']
        for frame_index, frame in enumerate(frames):
            complex_detection = complex_model_outputs[frame_index]
            production_detection = production_model_outputs[frame_index]
            data_frame_list.append({
                "imageId":StringElement(f"img_{video}_{str(frame.get('frameId')).zfill(8)}"),
                "frame":StringElement(frame.get('frameId')),
                "videoId":StringElement(video),
                "imageUrl":StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/StopSign_Part1_event.json/data_points/{video}/images/img_{video}_{str(frame.get('frameId')).zfill(8)}.jpg"),
                "timeOfCapture":TimeStampElement(get_timestamp_x_hours_ago(frame.get('frameId'))),
                "sourceLink":StringElement(f"img_{video}_{str(frame.get('frameId')).zfill(8)}"),
                "dutyType":StringElement(df["dutyType"][index]),
                "time_of_day":StringElement(df["time_of_day"][index]),
                "weather":StringElement(df["weather"][index]),
                "scene":StringElement(df["scene"][index]),
                "tags":StringElement(df["tags"][index]),
                "complexModel": model_image_inference(complex_detection),
                "productionModel": model_image_inference(production_detection)
            })

    return pd.DataFrame(data_frame_list)

pd_video_data_frame = json_parser("assets/Complex-Vienna-Stop-Event.json", "assets/Production-Vienna-Stop-Event.json", "./assets/Complex-Vienna-Stop-Model.json", "assets/Production-Vienna-Stop-Model.json")
# data_frame_extractor(pd_video_data_frame).to_csv("assets/event_ds_10.csv", index=False)
pd_image_data_frame = make_image_df(pd_video_data_frame)
data_frame_extractor(pd_image_data_frame).to_csv("assets/event_ds_pd_image_data_frame.csv", index=False)

image_ds_schema = RagaSchema()
image_ds_schema.add("imageId", PredictionSchemaElement())
image_ds_schema.add("frame", FrameSchemaElement())
image_ds_schema.add("videoId", ParentSchemaElement())
image_ds_schema.add("imageUrl", ImageUriSchemaElement())
image_ds_schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
image_ds_schema.add("sourceLink", FeatureSchemaElement())
image_ds_schema.add("weather", AttributeSchemaElement())
image_ds_schema.add("time_of_day", AttributeSchemaElement())
image_ds_schema.add("scene", AttributeSchemaElement())
image_ds_schema.add("complexModel", InferenceSchemaElement(model="Complex-Vienna-Stop-Event"))
image_ds_schema.add("productionModel", InferenceSchemaElement(model="Production-Vienna-Stop-Event"))

run_name = f"lm_video_loader_failure_mode_analysis_object_detection-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

creds = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")
#create test_ds object of Dataset instance
video_ds = Dataset(test_session=test_session,
                  name="stopsign-event-image-ds-v1",
                  type=DATASET_TYPE.VIDEO,
                  data=pd_image_data_frame,
                  schema=image_ds_schema,
                  creds=creds)

#load schema and pandas data frame
video_ds.load()


schema = RagaSchema()
schema.add("videoId", PredictionSchemaElement())
schema.add("videoUrl", ImageUriSchemaElement())
schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
schema.add("sourceLink", FeatureSchemaElement())
schema.add("dutyType", AttributeSchemaElement())
schema.add("time_of_day", AttributeSchemaElement())
schema.add("weather", AttributeSchemaElement())
schema.add("scene", AttributeSchemaElement())
schema.add("tags", AttributeSchemaElement())
schema.add("complexEvent", EventInferenceSchemaElement(model="Complex-Vienna-Stop-Event"))
schema.add("productionEvent", EventInferenceSchemaElement(model="Production-Vienna-Stop-Event"))

#create test_ds object of Dataset instance
image_ds = Dataset(test_session=test_session,
                  name="stopsign-event-video-ds-v1",
                  type=DATASET_TYPE.VIDEO,
                  data=pd_video_data_frame,
                  schema=schema,
                  creds=creds,
                  parent_dataset="stopsign-event-image-ds-v1")

#load schema and pandas data frame
image_ds.load()