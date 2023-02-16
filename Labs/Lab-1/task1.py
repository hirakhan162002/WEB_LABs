# Lab 01
# Task 1

mylist = []
mydic1 = {"Name": "Hira", "HwMarks": [20, 34, 9], "QuizMarks": [2, 45, 6], "ProjectMarks": 25}
mydic2 = {"Name": "Kalsom", "HwMarks": [25, 40, 50], "QuizMarks": [2, 45, 23], "ProjectMarks": 15}
mydic3 = {"Name": "Subhan", "HwMarks": [20, 30, 45], "QuizMarks": [21, 41, 6], "ProjectMarks": 25}
mydic4 = {"Name": "Hira", "HwMarks": [20, 30, 20], "QuizMarks": [29, 30, 20], "ProjectMarks": 25}
mylist.append(mydic1)
mylist.append(mydic2)
mylist.append(mydic3)
mylist.append(mydic4)
print(mylist)


def print_students(stu_dic):
    for key in stu_dic.keys():
        print(key, "=", stu_dic[key])


#print_students(mydic1)


def avg(list1):
    s = 0
    total = 0
    for i in list1:
        s = s + i
        total = total + 1
    avg1 = float(s / total)
    return avg1

#l  = [1,1,1,1,1]
#print( "The Avg of this list = ",Avg(l ))


def get_avg_of_student(stu_dic2):
    sum1 = avg(stu_dic2["HwMarks"])
    average1 = float(sum1 / 2)
    sum2 = avg(stu_dic2["QuizMarks"])
    average2 = float(sum2 / 2)
    stu_tup = (average1, average2)
    #print( "The Average Marks of HW AND QUIZ ARE : ", tuple)
    return stu_tup


#get_avg_of_student(mydic2)


def weighted_avg(tup, pro_marks):
    h = float(tup[0] * 25) / 100
    q = float(tup[1] * 40) / 100
    p = float(pro_marks * 35) / 100
    print("The weighted Avg is  =", h + q + p)
    return h + q + p


#avg_tuple = (get_avg_of_student(mydic1)) --- To Test Function
#Grade = Weighted_avg(avg_tuple, mydic1["ProjectMarks"])


def get_latter_grade(number):
    if 100 <= number >= 80:
        return "A"
    elif 79 <= number >= 70:
        return "B"
    elif 69 <= number >= 60:
        return "C"
    elif 59 <= number >= 50:
        return "D"
    else:
        return "F"


#g = Get_latter_grade(Grade) --- To test Function
#print("The Grade of Student " , g)


def get_class_avg(stu_list):
    return avg(stu_list)
