# Importing Libraries
import glob
import time
import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline


#pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'

# HuggingFace Transformer for Information Extraction
hft = pipeline(task="document-question-answering",
               model='impira/layoutlm-invoices')


# Fuction to get Final Diagnosis
def get_information_from_text(img):

    # Getting Final Diagnosis
    text = pytesseract.image_to_string(img)
    start = text.find('Final Diagnosis')
    end = text.find('Electronically')
    final_diagnosis = text[start:end]

    # Getting Gender
    index = text.find('yrs')
    gender = text[index-6]

    return final_diagnosis, gender


# Function to get information from 1st Page
def get_infomation_from_first_page(img, pipe):

    age = pipe(image=img,
               question="What is the age of the patient at top right of the page?")[0]['answer']
    dob = pipe(image=img,
               question="What is the date of birth of the patient at top right of the page?")[0]['answer']
    auth_provider = pipe(image=img,
                         question="What is the complete name of authorising provider?")[0]['answer']
    comment = pipe(image=img,
                   question="What is the comnplete comment?")[0]['answer']
    clinical_informtaion = pipe(image=img,
                                question="What is the clinical information?")[0]['answer']
    final_diagnosis = pipe(image=img,
                           question="What are the points in final diagnosis?")[0]['answer']

    return (age, dob, auth_provider, comment,
            clinical_informtaion, final_diagnosis)


# Function to get information from 2nd Page
def get_infomation_from_second_page(img, pipe):

    name = pipe(image=img,
                question="What is the name of the patient at top left of the page?")[0]['answer']
    resulting_lab = pipe(image=img,
                         question="What is the Resulting Labs?")[0]['answer']

    return (name, resulting_lab)


# Funtion to get information
def get_information(path):
    # # Getting list of Documents
    # list_of_pdfs = glob.glob(r'Paragraph/Data/*.pdf')
    # Getting list of Documents
    #list_of_pdfs = glob.glob(path+'/*.pdf')
    #print(list_of_pdfs)
    info_dict={}
    #for pdf in list_of_pdfs:

    # Converting PDF into Images
    # images = convert_from_path(pdf, poppler_path=r'Morgan/poppler-0.68.0\bin')
    images = convert_from_path(path,poppler_path = r'poppler-0.68.0\bin')

    # Extracting the information
    age, dob, auth_provider, comment, clinical_informtaion, final_diagnosis = get_infomation_from_first_page(images[0], hft)
    age = str(age)
    name, resulting_lab = get_infomation_from_second_page(images[1], hft)
    final_diagnosis, gender = get_information_from_text(images[0])
    if gender == 'M':
        gender = 'Male'
    else:
        gender = 'Female'
    key=path.split('\\')[-1]
    info_dict[key]={'Name': name, 'Age': age, 'Gender': gender, 'Date of Birth': dob,
            'Authorising Provider': auth_provider, 'Clinical Information': clinical_informtaion,
            'Final Diagnosis': final_diagnosis, 'Resulting Lab': resulting_lab}
    return info_dict

# # Calling Function for getting the output
# print(get_information())


# # System End Time
# sys_end = time.time()
#
# print('Total Time of Execution :', sys_end - sys_start, 'seconds!')
