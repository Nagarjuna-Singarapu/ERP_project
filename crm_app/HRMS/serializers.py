from rest_framework import serializers
from .models import LeaveReason, LeaveType, PayGrade, PositionType, SalaryStepGrade, TerminationReason,TerminationType, SkillType

class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ['skillTypeId','description']

from .models import PayGrade, PositionType, SalaryStepGrade, TerminationReason,TerminationType


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
