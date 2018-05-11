import wx
import os
import numpy as np
import argparse
import time
import threading
import cv2

current_frame = 1
illegally_v_container = {}

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
		confidence_m = detections[0, 0, i, 2]
		idx = int(detections[0, 0, i, 1])
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if  confidence_m >= display.confidence and CLASSES[idx] == "car":
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
		if illegally_v_container[x][0] + display.f_i_t < current_frame:
			del illegally_v_container[x]
		elif current_frame - illegally_v_container[x][1] >= display.s_t:
			y = x[1] - 15 if x[1] - 15 > 15 else x[1] + 15
			cv2.putText(image, "Illegally Parked Vehicle Detected", (x[0], y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
		else:
			continue
	#print illegally_v_container
	return image

			
def scaled_image(path, width, height):
	img = wx.Image(path,wx.BITMAP_TYPE_ANY)
	img = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	return wx.Bitmap(img)
	
class ControlPanel(wx.Frame):
	def __init__(self, parent, id, size):
		wx.Frame.__init__(self, parent, id, size=(800,600),title = "Illegally Parked Vehicle Detector")
		self.errors = 0
		#Main Panel
		
		self.main_panel = wx.ScrolledWindow(self)
		self.main_sizer = wx.GridBagSizer(5,5)
		self.main_panel.SetScrollbars(20, 20, 55, 40)
		self.main_panel.Scroll(50,10)
		
		
		#self.middle_panel
		
		self.middle_panel = wx.Panel(self.main_panel, 21)
		self.middle_sizer = wx.BoxSizer()
		
		
		
		#Header Panel
		
		self.header_panel = wx.Panel(self.main_panel,4)
		self.header_sizer = wx.GridBagSizer(5,5)
		self.logo = wx.StaticBitmap(self.header_panel, 18,scaled_image(path="G:/Projects/IPVD/a.png", width=70,height=50))
		self.header_title = wx.StaticBitmap(self.header_panel, 19,scaled_image(path="G:/Projects/IPVD/t.png", width=325,height=50))
		self.header_sizer.Add(self.header_title, (0,0), flag= wx.LEFT | wx.TOP | wx.RIGHT, border=30)
		self.header_sizer.Add(self.logo, (0,1), flag= wx.EXPAND |wx.TOP | wx.RIGHT, border=25)
		self.header_sizer.AddGrowableCol(0)
		self.header_panel.SetSizer(self.header_sizer)
		
		self.main_line = wx.StaticLine(self.main_panel)
		
		
		
		#Status Panel
		
		self.status_panel = wx.Panel(self.middle_panel, 3)
		self.status_sizer = wx.GridBagSizer(5,5)
		
				
		self.source_text = wx.StaticText(self.status_panel, 5, 'Select a Source of Video File : ')
		self.video_radio = wx.RadioButton(self.status_panel, 6, 'Video File', (10,10), style = wx.RB_GROUP) 
		self.ip_radio = wx.RadioButton(self.status_panel, 7, 'IP Cam', (20,20)) 
		self.src_open = wx.Button(self.status_panel, 701,'Choose Video')
		self.input_txt =  wx.StaticText(self.status_panel, 8, 'Select a video file : ')
		self.secure_time_label = wx.StaticText(self.status_panel, 9, 'Secure Time (in seconds) : ')
		self.secure_time = wx.TextCtrl(self.status_panel, 10,value="7")
		self.failure_ignore_time_label = wx.StaticText(self.status_panel, 11, 'Failure Ignore Time (in seconds) : ')
		self.failure_ignore_time = wx.TextCtrl(self.status_panel, 12,value="1")
		self.strict_factor_label = wx.StaticText(self.status_panel, 13, 'Strict Factor : ')
		self.strict_factor = wx.ComboBox(self.status_panel, 14, choices=[str(x)+"%" for x in xrange(10,100,10)],style=wx.CB_READONLY,value = "60%")
		self.alarm_cb_label = wx.StaticText(self.status_panel, 15, 'Activarte Alarm on detection : ')
		self.alarm_cb = wx.CheckBox(self.status_panel, 16, style=wx.ALIGN_RIGHT)
		self.start_btn = wx.Button(self.status_panel, 171, 'Start', (10,10))
		
			
		
		
		self.status_sizer.Add(self.source_text, (0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
		self.status_sizer.Add(self.video_radio, (0, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
		self.status_sizer.Add(self.ip_radio, (0, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.input_txt, (1, 0),  flag=wx.TOP | wx.LEFT | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.src_open, (1, 1), (1,6),  flag= wx.TOP | wx.BOTTOM, border=  15)
		self.status_sizer.Add(self.secure_time_label, (2, 0),  flag= wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.secure_time, (2, 1),  flag=wx.EXPAND|wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.failure_ignore_time_label, (3, 0),  flag= wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.failure_ignore_time, (3, 1),  flag=wx.EXPAND|wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.strict_factor_label, (4, 0),  flag= wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.strict_factor, (4, 1),  flag=wx.EXPAND|wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.alarm_cb_label, (5, 0),  flag = wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.alarm_cb , (5, 1),  flag = wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_sizer.Add(self.start_btn , (7, 0),  flag=wx.LEFT | wx.TOP | wx.BOTTOM, border = 15)
		self.status_panel.SetSizerAndFit(self.status_sizer)
		
		#video panel
		
		self.video_panel = wx.Panel(self.middle_panel, 201, style=wx.BORDER_SUNKEN)
		self.video_sizer = wx.BoxSizer()
		self.Bmp = wx.StaticBitmap(self.video_panel, 19,scaled_image(path="G:/Projects/IPVD/cod.jpg", width=700,height=450),(0,0))
		self.video_sizer.Add(self.Bmp,-1, wx.EXPAND) 
		self.video_panel.SetSizerAndFit(self.video_sizer)
	
		#Adding video panel and status panel to middle panel
		
		self.middle_sizer.Add(self.status_panel, 1,flag= wx.EXPAND | wx.TOP, border=40)
		self.middle_sizer.Add(self.video_panel, 1,flag= wx.EXPAND | wx.LEFT, border=10)
		self.middle_panel.SetSizer(self.middle_sizer)
		
		#Adding header panel and middle panel to self.main_panel
	
		self.main_sizer.Add(self.header_panel,(0,0), flag=wx.EXPAND)
		self.main_sizer.Add(self.main_line, (1,0), flag= wx.EXPAND | wx.TOP | wx.BOTTOM, border = 20)
		self.main_sizer.Add(self.middle_panel,(4,0), flag=wx.EXPAND | wx.LEFT |wx.RIGHT, border = 20)
		self.main_sizer.AddGrowableCol(0)
		
		self.main_panel.SetSizer(self.main_sizer)
		
		#event Bindings
		self.Bind(wx.EVT_RADIOBUTTON, self.SetSource, id = 6)
		self.Bind(wx.EVT_RADIOBUTTON, self.SetSource, id = 7)
		self.Bind(wx.EVT_BUTTON, self.ChooseVideo, id=701)
		self.Bind(wx.EVT_BUTTON, self.Integrate, id = 171)
		self.Bind(wx.EVT_CLOSE, self.OnClose)	
		
		self.Center()
		self.Show(True)
		self.Maximize(True)
		self.SetMinSize(wx.Size(1200,720))
	
	def SetSource(self, event):
		if self.video_radio.GetValue():
			try:
				self.input_txt.Destroy()
				self.src_input.Destroy()
				self.src_open.Destroy()
			except:
				self.errors += 1
			self.src_open = wx.Button(self.status_panel, 701,'Choose Video')
			self.input_txt =  wx.StaticText(self.status_panel, 8, 'Select a video file : ')
			self.status_sizer.Add(self.input_txt, (1, 0),  flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
			self.status_sizer.Add(self.src_open, (1, 1), (1,6),  flag= wx.TOP | wx.BOTTOM, border=15)
			self.status_sizer.Layout()
			self.status_panel.Fit()
		
		else:
			try:
				self.input_txt.Destroy()
				self.src_open.Destroy()
				self.src_input.Destroy()
			except:
				self.errors += 1
			self.src_input = wx.TextCtrl(self.status_panel, 7,value = "")
			self.input_txt =  wx.StaticText(self.status_panel, 8, 'IP of CCTV Camera : ')
			self.status_sizer.Add(self.input_txt, (1, 0),  flag=wx.TOP | wx.LEFT | wx.BOTTOM, border = 15)
			self.status_sizer.Add(self.src_input, (1, 1), (1,6),  flag= wx.EXPAND | wx.TOP | wx.BOTTOM, border = 15)
			self.status_sizer.Layout()
			self.status_panel.Fit()
	
	def ChooseVideo(self, event):
		wcd = 'MP4 files (*.mp4)|*.mp4|AVI files (*.avi)|*.avi'
		dir = os.getcwd()
		open_dlg = wx.FileDialog(self, message='Choose a file', defaultDir=dir, defaultFile='',wildcard=wcd, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if open_dlg.ShowModal()==wx.ID_OK: 
			path = open_dlg.GetPath()
			try:
				self.src_open.Destroy()
				self.src_input.Destroy()
			except:
				self.errors += 1
			self.src_open = wx.Button(self.status_panel, 701,'Choose Video')
			self.src_input = wx.StaticText(self.status_panel, 7,path[0 if len(path)<30 else len(path)-20:len(path)])
			self.status_sizer.Add(self.src_input, (1, 1), (1,3),  flag= wx.EXPAND | wx.TOP | wx.BOTTOM, border = 15)
			self.status_sizer.Add(self.src_open, (1, 4),  flag=  wx.TOP | wx.BOTTOM, border = 15)
			self.status_sizer.Layout()
			self.status_panel.Fit()
			
	def Integrate(self,event):
		try:
			global current_frame, illegally_v_container

			current_frame = 1
			illegally_v_container = {}

			self.camera = self.ip_radio.GetValue()
			if self.camera:
				self.path = self.src_input.GetValue()
			else:
				self.path = self.src_input.GetLabel()
			self.capv = cv2.VideoCapture("http://"+self.path+":8080/video?.mp4") if self.camera else cv2.VideoCapture(self.path)
		
			(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
		
			if int(major_ver)  < 3:
				self.fps = self.capv.get(cv2.cv.CV_CAP_PROP_FPS)
			else:
				self.fps = self.capv.get(cv2.CAP_PROP_FPS)
			
			self.s_t = int(self.secure_time.GetValue())*self.fps
			self.f_i_t = int(self.failure_ignore_time.GetValue())*self.fps
			self.confidence = int(self.strict_factor.GetValue()[0:2])/float(100)
			self.Bmp.Destroy()
			
		except:
			print "Error in integration"
		
		try:
			self.video_panel.Unbind(wx.EVT_PAINT)
			self.video_panel.Unbind(wx.EVT_TIMER)
		except:
			print "Error in unbinding"
		
		ret, frame = self.capv.read()
		height, width = 650, 460
		frame = VehicleDetector(image = frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.buildBmp = wx.Bitmap.FromBuffer(650, 460, frame)
		self.video_panel.Refresh()
		self.timer = wx.Timer(self.video_panel)
		self.timer.Start(1000.0/self.fps)

		self.video_panel.Bind(wx.EVT_PAINT, self.onPaint)
		self.video_panel.Bind(wx.EVT_TIMER, self.run_vehicle_detector)
		
        
	def onPaint(self, evt):
		if self.buildBmp:
			dc=wx.BufferedPaintDC(self.video_panel)
			dc.DrawBitmap(self.buildBmp,0,0)
		evt.Skip()
		
		
	def run_vehicle_detector(self, event):
		global current_frame
		ret, frame = self.capv.read()
		if ret == True:
			current_frame += 1;
			#a = os.system('cls')
			#print "Current Frame : ",current_frame
			frame = cv2.resize(frame, (650, 460))			
			outframe = VehicleDetector(image = frame)
			
			#cv2.imshow("",display.outframe)
			#cv2.waitKey(0)
			
			outframe = cv2.cvtColor(outframe, cv2.COLOR_BGR2RGB)
					
			self.buildBmp.CopyFromBuffer(outframe)
			
			self.video_panel.Refresh()
		event.Skip()
	
	def OnClose(self, event):
		self.video_panel.Unbind(wx.EVT_PAINT)
		self.video_panel.Unbind(wx.EVT_TIMER)
		self.Destroy();
""""""""""""""""""""""""""""""""""""""""""""""""""" Argument Parser """""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == "__main__":
	#Global vehicle container
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
	COLORS[7] = [0,255,0]
	net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "deploy.caffemodel")
	app = wx.App()
	display = ControlPanel(None,1,size = (800,600))
	app.MainLoop()