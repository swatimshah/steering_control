import argparse
import os
import cv2
import numpy
import time

font = cv2.FONT_HERSHEY_PLAIN

def putIterationsPerSec(frame, frame_id):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, str(frame_id), (20, 40), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    return frame

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)

    frame_id = 0;
    data_list = numpy.empty([0, 2])
    data = numpy.empty([2])

    while True:
        grabbed, frame = cap.read()

        if frame is None:
            break;

        if(frame_id == 0):		
            scale_percent = 35 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)

        frame_id = frame_id + 1	

        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        data[0] = frame_id
        data[1] = round(time.time(), 3)

        data_list = numpy.append(data_list, data.reshape(1, 2), axis=0)

        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(resized, frame_id)
        cv2.imshow("Video", resized)

        # wait for user to press any key
        #key = cv2.waitKey(20)

    numpy.savetxt("auto_car_mapping.csv", data_list, delimiter=",", header="frame_id, timestamp")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    args = vars(ap.parse_args())

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])


    noThreading(args["source"])
    print("no thread")

if __name__ == "__main__":
    main()


