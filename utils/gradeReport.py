import os
from bson.objectid import ObjectId
import numpy as np
import matplotlib.pyplot as plt
from api.uploadMedia import uploadMedia 
from api.media import sendMedia
from utils.db import db
import pyimgur
import requests
from fpdf import FPDF

# IMGUR client
IMGUR_CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
imgurclient = pyimgur.Imgur(IMGUR_CLIENT_ID)

# ____________MatPlotLib & IMGUR Trial_____________
def studentProgress(receiver, studentId, courseId, sessionId):
    # collection = db["test"]
    # student  = collection.find_one({ '_id': studentId})
    student = db['test'].find_one({'_id': studentId})
    courseSelected = {}
    for i in range(0, len(student['courses'])):
        if student['courses'][i]['courseId'] == courseId:
            courseSelected = student['courses'][i]
    
    
    if courseSelected['courseType'] == 'static':
        quizMarks = []
        quizIds = []
        for i in range(0, len(courseSelected['courseQuizzes'])):
            quizIds.append(courseSelected['courseQuizzes'][i]['quizId'])
            quizMarks.append(courseSelected['courseQuizzes'][i]['quizScore'])
    
        plt.barh(quizIds, quizMarks, align="center")
        plt.ylabel('Quizzes')
        plt.xlabel('Marks')
        plt.title('Progress of Student ID: {}'.format(studentId))
        plt.savefig('static/gradeMedia/studentplot.png')

        mediaId, mediaType = uploadMedia('studentplot.png', 'static/gradeMedia/studentplot.png', 'png')
        print(mediaId, mediaType)
        sendMedia(receiver, mediaId, mediaType, sessionId)
        
        return ''
    
    if courseSelected['courseType'] == 'dynamic':
        pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 25)
        pdf.set_text_color(0, 0, 0)
        pdf.image('static/gradeMedia/IQ_sample.png', x = 0, y = 0, w = 210, h = 297)
        pdf.text(20, 110, studentId)
        pdf.text(20, 150, courseSelected['courseId'])
        pdf.output('static/gradeMedia/studentPdf.pdf')
        mediaId, mediaType = uploadMedia('studentPdf.pdf', 'static/gradeMedia/studentPdf.pdf', 'pdf')
        print(mediaId, mediaType)
        sendMedia(receiver, mediaId, mediaType, sessionId)
        
        return ''

    
    return ''