# import the necessary packages
import numpy as np
import argparse
import cv2
import os


def get_iou(bb1, bb2):
    
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou



def VehicleDetector(image):
	global current_frame
	# load our serialized model from disk
		
	# load the input image and construct an input blob for the image
	# by resizing to a fixed 300x300 pixels and then normalizing it
	# (note: normalization is done via the authors of the MobileNet SSD
	# implementation)

	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,(300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	
	#computing object detections
	
	net.setInput(blob)
	detections = net.forward()
	
	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		global current_frame,conf
	
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
		idx = int(detections[0, 0, i, 1])
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if  confidence >= conf and CLASSES[idx] == "car":
			flag = True
			# extract the index of the class label from the `detections`,
			# then compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			#print("[INFO] {}".format(label))
			cv2.rectangle(image, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			
			bb1 = {'x1':startX,'y1':startY,'x2':endX,'y2':endY}
			for x in illegally_v_container.keys():
				if not illegally_v_container[x][2]:
					bb2 = {'x1':x[0],'y1':x[1],'x2':x[2],'y2':x[3]}
					if get_iou(bb1, bb2)>0.70:
						illegally_v_container[x][0] += 1
						illegally_v_container[x][2] = True
						flag = False
						break
			if flag:
				illegally_v_container[(startX, startY, endX, endY)] = [current_frame,current_frame,True]	
	for x in illegally_v_container.keys():
		illegally_v_container[x][2] = False
		if illegally_v_container[x][0] + M_t < current_frame:
			del illegally_v_container[x]
		elif current_frame - illegally_v_container[x][1] >= I_t:
			y = x[1] - 15 if x[1] - 15 > 15 else x[1] + 15
			cv2.putText(image, "Illegally Parked Vehicle Detected", (x[0], y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
		else:
			continue
	#print illegally_v_container
	return image

def run_vehicle_detector(videofile ,showPlayback, ip):
	global current_frame
	cap = cv2.VideoCapture("http://"+videofile+":8080/video?.mp4") if ip else cv2.VideoCapture(videofile)
	width = int(cap.get(3))
	height = int(cap.get(4))
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			current_frame += 1;
			#a = os.system('cls')
			#print "Current Frame : ",current_frame
			frame = cv2.resize(frame, (800, 500))
			outframe = VehicleDetector(image = frame)
			outframe = cv2.cvtColor(outframe, cv2.COLOR_RGB2BGR)
			if showPlayback:
				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('c'):
					break
		else:
			break
	cap.release()
	cv2.destroyAllWindows()


""""""""""""""""""""""""""""""""""""""""""""""""""" Argument Parser """""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == "__main__":
	#Global vehicle container
	illegally_v_container = {}
	current_frame = 0
	conf = 0.30
	M_t = 30    # Number of frames to declare a vehicle as a ghost vehicle
	I_t = 200  # Time in terms of frame to declare a vehicle illegally parked


	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", required=False,
		help="path to Video file")

	args = vars(ap.parse_args())

	# initialize the list of class labels MobileNet SSD was trained to
	# detect, then generate a set of bounding box colors for each class
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
	COLORS[7] = [0,255,0]
	videoname = args["video"]
	ip = raw_input("Enter IP of an CCTV Camera : ") if videoname == None else videoname
	net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "deploy.caffemodel")
	run_vehicle_detector(videofile = ip, showPlayback = True, ip = True if videoname == None else False)