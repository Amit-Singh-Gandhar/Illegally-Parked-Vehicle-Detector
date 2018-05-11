import wx
import os

current_id = 20

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
		self.secure_time = wx.TextCtrl(self.status_panel, 10,value="1")
		self.failure_ignore_time_label = wx.StaticText(self.status_panel, 11, 'Failure Ignore Time (in seconds) : ')
		self.failure_ignore_time = wx.TextCtrl(self.status_panel, 12,value="7")
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
		
		self.video_panel = wx.Panel(self.middle_panel, 20, style=wx.BORDER_SUNKEN)
		self.video_sizer = wx.BoxSizer()
		self.video_sizer.Add(wx.StaticBitmap(self.video_panel, 19,scaled_image(path="G:/Projects/IPVD/cod.jpg", width=700,height=450),(0,0)),-1, wx.EXPAND) 
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
			camera = self.ip_radio.GetValue()
			if camera:
				path = self.src_input.GetValue()
			else:
				path = self.src_input.GetLabel()
			secure_time_v = self.secure_time.GetValue()
			failure_ignore_time_v = self.secure_time.GetValue()
			strict_factor_v = int(self.strict_factor.GetValue()[0:2])/float(100)
			
		except:
			print "Error"
			
app = wx.App()
ControlPanel(None,1,size = (800,600))
app.MainLoop()