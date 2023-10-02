import json
import os
import jams
import sys


# converts the json file contents into jams format
def create_jams_from_json(input_json_file, output_directory):
     # read the JSON file into a dictionary
    with open(input_json_file, 'r') as f:
        json_data = json.load(f)

    # create a new JAMS object
    jam = jams.JAMS()

    # create an annotation object for segments
    annotation = jams.Annotation(namespace='segment_open', time=0, duration=json_data['beats'][-1])

    # iterate through the segments in the JSON data and create annotations
    for segment in json_data['segments']:
        start_i = segment['start']
        end_i = segment['end']
        label_i = segment['label']

        data_point = {
            "time": start_i,
            "duration": end_i - start_i,
            "value": label_i,
            "confidence": 1.0
        }

        annotation.append(**data_point)

    # add the annotation to the JAMS object
    jam.annotations.append(annotation)

    # extract song name from path
    song_name = os.path.basename(json_data['path']).split('.')[0]
    jam.file_metadata.title = song_name
    jam.file_metadata.artist = ""
    jam.file_metadata.release = ""
    jam.file_metadata.duration = json_data['beats'][-1]

    # save JAMS object to a file
    output_filename = os.path.join(output_directory, f"{song_name}.jams")
    jam.save(output_filename)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python json_to_jams.py <input_json_file> <output_directory>")
        sys.exit(1)
    elif len(sys.argv) == 3:
        input_json_file = sys.argv[1]
        output_directory = sys.argv[2]

    os.makedirs(output_directory, exist_ok=True)

    # create JAMS file
    create_jams_from_json(input_json_file, output_directory)

    print("Conversion from json to jams is complete.")

