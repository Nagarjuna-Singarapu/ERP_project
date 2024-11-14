from rest_framework import serializers
from .models import HR_Employee, JobInterviewType, PerformanceReview, PayGrade, PositionType, SalaryStepGrade, TerminationReason,TerminationType, SkillType, LeaveReason, LeaveType, TrainingClassType

class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ['skillTypeId','description']

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

class PerformanceReviewSerializer(serializers.ModelSerializer):
    hr_employee = serializers.PrimaryKeyRelatedField(queryset=HR_Employee.objects.all())
    class Meta:
        model = PerformanceReview
        fields = '__all__'


class PositionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionType
        fields = ['id', 'name', 'parent_type', 'has_table', 'description']

class LeaveReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReason
        fields = ['id', 'leave_reason', 'description']

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'leave_type', 'description']

class JobInterviewTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterviewType
        fields = ['id', 'jobinterviewType', 'description']

class TrainingClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingClassType
        fields = ['id', 'tranningTypeId', 'description']

