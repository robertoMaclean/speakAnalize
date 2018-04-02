import matplotlib.pyplot as plt
import os
from public import *

class GroupAnalyze(object):
	"""docstring for GroupAnalyze"""
	def __init__(self, studentList, name):
		self.students = studentList
		self.name = name
		print("hola")

	def Analyze(self):
		for x in range(0,len(self.students)):
			print("hello")


	def EventTime(self):
		total = 0
		for x in range(0, len(self.students)):
			total += self.students[x].interventionTotalTime
		return total

	def InterventionCount(self):
		count = 0
		for x in range(0,len(self.students)):
			count += self.students[x].interventionCount
		return count

	def listarEstudiantes(self):
		for x in range(0, len(self.students)):
			print("nombre: ",self.students[x].name)

	def EnergiAVG(self):
		total = 0
		for x in range(0, len(self.students)):
			total += self.students[x].emergyTotalAVG
		return total

	#def EnergiAVGPlot(self):

	def InterventionPlot(self):	
		interventionValue = []
		for x in range(0, len(self.students)):
			studentsName.append(self.students[x].name)
			interventionValue.append(self.students[x].interventionTotalTime)
		self.CakePlot(values=interventionValue, labels=studentsName)

	def CakePlot(self, labels, values):
		filepath = "../files/group/"+self.name+"/"
		fig1, ax1 = plt.subplots()
		ax1.pie(values , labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
		ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
		EnsureDir(filepath=filepath)
		plt.savefig(filepath+"CakePlot")
		plt.show()





