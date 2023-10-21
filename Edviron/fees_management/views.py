from django.http import JsonResponse
from fees_management.models import Payment, Installment, DefaultingStudent
from django.utils import timezone
import datetime
# Create your views here.
def Filter_by(request):
    x=request.GET.items()
    arr=[]
    for p,q in x:
        arr.append(p)
        arr.append(q)
    if arr[0]=="school_id":
        data=DefaultingStudent.objects.filter(school_id=int(q))
    elif arr[0]=="school_name":
        data=DefaultingStudent.objects.filter(school_name=q)
    elif arr[0]=="student_name":
        data=DefaultingStudent.objects.filter(student_name=q)
    elif arr[0]=="student_id":
        data=DefaultingStudent.objects.filter(student_id=int(q))
    elif arr[0]=="date":
        date = timezone.datetime.strptime(q,"%Y-%m-%d").date()
        data = DefaultingStudent.objects.filter(defaulting_due_date__lt=date)
    else:
        return JsonResponse("no match found",safe=False)
    result_list=[]
    for obj in data:
        result_list.append(
            {
                "school_id":obj.school_id,
                "school_id":obj.school_id,
                "student_id":obj.student_id,
                "student_name":obj.student_name,
                "defaulting due date":obj.defaulting_due_date,
                "due_amount": obj.due_amount
            }
            )
    if len(result_list)==0:
        return JsonResponse("no recond found for this {} ".format(p),safe=False)
    return JsonResponse(result_list,safe=False)



def mark_defaulters(request):
    current_date=timezone.now().date()
    defaulters=[]
    overdue_installments=Installment.objects.filter(due_date__lt=current_date)
    for installment in overdue_installments:
        school=installment.student.school
        student_name=installment.student.student_name
        defaulter_details={
            "school_id": school.id,
            "school_name": school.name,
            "student_id": installment.student.student_id,
            "student_name": student_name,
            "due_date": installment.due_date,
            "due_amount": installment.student.defaultingstudent.due_amount
            
        }

        if not Payment.objects.filter(installment=installment).exists():
            defaulters.append(defaulter_details)
            defaulting_student=DefaultingStudent(
                student_name=student_name,
                school_id=school.id,
                school_name=school.name,
                student_id=installment.student.student_id,
                defaulting_due_date=installment.due_date,
                due_amount=installment.student.defaultingstudent.due_amount
            )
            defaulting_student.save()
        else:
            installment.due_date=installment.due_date + datetime.timedelta(days=60)
            installment.save()

    return JsonResponse({'defaulters': defaulters})
