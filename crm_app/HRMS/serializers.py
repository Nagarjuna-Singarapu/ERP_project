from rest_framework import serializers

from .models import SkillType, PayGrade, SalaryStepGrade, TerminationReason,TerminationType


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
