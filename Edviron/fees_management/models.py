from django.db import models

# Create your models here.

class School(models.Model):
    school_id = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Student(models.Model):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    student_id=models.IntegerField()
    student_name=models.CharField(max_length=100)

class Installment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    due_date=models.DateField()

class Payment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    installment=models.ForeignKey(Installment,on_delete=models.CASCADE)
    amount=models.IntegerField()
    payment_date=models.DateField()

class Due(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    start_date=models.DateField()
    fee_name=models.CharField(max_length=100,default="2 Month Fee")

class DefaultingStudent(models.Model):
    school_id=models.IntegerField()
    school_name=models.CharField(max_length=100)
    student_id=models.IntegerField()
    student_name=models.CharField(max_length=100)
    defaulting_due_date=models.DateField()
    due_amount=models.IntegerField(null=True, blank=True)
