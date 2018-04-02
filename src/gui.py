import tkinter
import tkinter.messagebox as messagebox
import student
import os  
  
class App(object):
	"""docstring for App"""
	def __init__(self, master):
		self.master= master
		pad=3
		self._geom= '800x600+0+0'
		master.geometry("{0}x{1}+0+0".format(
			master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.bind('<Escape>',self.toggle_geom)
		self.rowIndex = 0
		self.Frame()
		self.Start() 
		# layout all of the main containers
		self.master.grid_rowconfigure(1, weight=1)
		self.master.grid_columnconfigure(0, weight=1)

	def toggle_geom(self, event):
	    geom=self.master.winfo_geometry()
	    print(geom,self._geom)
	    self.master.geometry(self._geom)
	    self._geom=geom

	def Analyze(self):
		# photo = tkinter.PhotoImage(file= "FlowChart.png")
		# w = tkinter.Label(self.master, text= "Rouge", fg= "red")
		# w = tkinter.Label(self.mast, image= photo)
		# w.photo = photo
		# w.grid(row=4, column=3)

		st = student.StudentAnalyze("pedro")
		st.Analyze()
		st2 = student.StudentAnalyze("pedro")
		st2.Analyze()
		self.IntervTable(st)
		self.loadImage(st, "Emotion.png", "../files/student/",self.plotframe)
		self.loadImage(st, "strength.png", "../files/student/",self.plotCake)
		self.IntervTable(st2)
		self.loadImage(st2, "Emotion.png", "../files/student/",self.plotframe)
		self.loadImage(st2, "strength.png", "../files/student/",self.plotCake)		
		self.Menu([st,st2])

	def Menu(self, studentsGroup):
		for x in range(0,len(studentsGroup)):
			button = tkinter.Button(self.menuframe, text= studentsGroup[x].name, command= self.Analyze, height = 2, width = 15)
			button.grid(row=x,column=0) 

	def Table(self, values):
		# create the center widgets
		tableframe = tkinter.Frame(self.tableframe, bg='red', width=450, height=50)
		tableframe.grid(row=1, columnspan=3,sticky="WENS")
		for column in range(0,len(values)):
			for row in range(0,len(values[column])):
				l = tkinter.Label(tableframe, text=values[column][row], relief=tkinter.RIDGE, font=("-weight bold",20))
				l.grid(row=row, column=column, sticky='WENS')
			
	def loadImage(self, student, imagename, filepath, frame):
		imageframe = tkinter.Frame(frame, bg='red', width=20, height=10, pady=3)
		imageframe.grid(row=0, sticky="nw")
		print("the path is:", filepath)
		photo = tkinter.PhotoImage(file=filepath+student.name+"/"+imagename)
		w = tkinter.Label(text= "Rouge", fg= "red")
		w = tkinter.Label(imageframe, image= photo)
		w.photo = photo
		w.grid(row=0, column=0, sticky="nw")

	def IntervTable(self, student):
		intervention = ["Int"]
		intStart = ["Inicio"]
		intEnd = ["Fin"]
		interventionTime = student.interventionTime
		speakTime = student.interventionSpeakTime
		energyAVG = student.energyInterventionAVG
		values = []
		for x in range(len(student.intervention)):
			intStart.append(student.intervention[x][0][0])
			intEnd.append(student.intervention[x][1][-1])
			intervention.append(x+1)
		intStart.append(student.intervention[0][0][0])
		intEnd.append(student.intervention[-1][1][-1])
		#Set column title
		intervention.append("Total")
		interventionTime.insert(0,"Duración")
		interventionTime.append(student.interventionTotalTime)
		speakTime.insert(0,"Tiempo de habla")
		speakTime.append(student.interventionTotalSpeakTime)
		energyAVG.insert(0,"Vol Prom")
		energyAVG.append(student.energyInterventionTotalAVG)
		values.append(intervention)
		values.append(intStart)
		values.append(intEnd)
		values.append(interventionTime)
		values.append(speakTime)
		values.append(energyAVG)
		self.Table(values)

	def Start(self):
		title = tkinter.Label(self.topframe, text= "Nuevo Reporte")
		groupname = tkinter.Label(self.topframe, text= "Nombre del grupo")
		example = tkinter.Label(self.topframe, text= "Last Name")
		e1 = tkinter.Entry(self.topframe)
		e2 = tkinter.Entry(self.topframe)
		button = tkinter.Button(self.topframe, text= "Grabar", command= self.Analyze)
		title.grid(row=0, columnspan=4, sticky="ew")
		groupname.grid(row=1, column=0, sticky="w")
		example.grid(row=2, column=0, sticky="w")
		e1.grid(row=1, column=1)
		e2.grid(row=2, column=1)
		button.grid(row=3, column=1)
		
		
	def Frame(self):
		top_frame = tkinter.Frame(self.master, bg='cyan', width=450, height=50, pady=3)
		center = tkinter.Frame(self.master, bg='gray2', width=50, height=10, padx=3, pady=3)
		top_frame.grid(row=0, sticky="ew")
		center.grid(row=1, sticky="nw")
	
		# create the center widgets
		center.grid_rowconfigure(0, weight=1)
		center.grid_columnconfigure(1, weight=1)

		menu = tkinter.Frame(center, bg='blue', width=500, height=800)
		menu.grid(row=0, column=0, sticky="nw")
		center.grid_rowconfigure(1, weight=1)
		center.grid_columnconfigure(0, weight=1)
		table = tkinter.Frame(center, bg='yellow', width=500, height=50, padx=3, pady=3)
		plot = tkinter.Frame(center, bg='red', width=500, height=400, padx=3, pady=3)
		plotCake = tkinter.Frame(center, bg='green', width=500, height=400, padx=3, pady=3)
		
		table.grid(row=0, column=1, sticky="nw")
		plot.grid(row=1, column=1, sticky="nw")	
		plotCake.grid(row=1, column =2, sticky="w")

		self.menuframe = menu
		self.tableframe = table
		self.plotframe = plot
		self.topframe = top_frame
		self.plotCake = plotCake


top = tkinter.Tk()
top.title("Análisis Trabajo Grupal")
app = App(top)
top.mainloop()	

