from rest_framework import serializers
from .models import HR_Employee, PerformanceReview, PartySkill, PayGrade, SalaryStepGrade, TerminationReason,TerminationType

class PayGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGrade
        fields = ['id', 'grade_name']

class SalaryStepGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStepGrade
        fields = ['id', 'step_name']

class TerminationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminationType
        fields = ['id', 'termination_type']

class TerminationReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminationReason
        fields = ['id', 'termination_reason']

class HREmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR_Employee
        fields = '__all__'  # Serialize all fields

class PerformanceReviewSerializer(serializers.ModelSerializer):
    hr_employee = serializers.PrimaryKeyRelatedField(queryset=HR_Employee.objects.all())
    class Meta:
        model = PerformanceReview
        fields = '__all__'

