from rest_framework import serializers


class TeacherFolderSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    alternateLink = serializers.CharField()


class GradeCategorySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    weight = serializers.IntegerField()
    defaultGradeDenominator = serializers.IntegerField()


class GradebookSettingsSerializer(serializers.Serializer):
    calculationType = serializers.CharField()
    displaySetting = serializers.CharField()
    gradeCategories = GradeCategorySerializer(many=True)


class CursoGetResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    section = serializers.CharField()
    descriptionHeading = serializers.CharField()
    description = serializers.CharField()
    ownerId = serializers.CharField()
    creationTime = serializers.CharField()
    updateTime = serializers.CharField()
    enrollmentCode = serializers.CharField()
    courseState = serializers.CharField()
    alternateLink = serializers.CharField()
    teacherGroupEmail = serializers.CharField()
    courseGroupEmail = serializers.CharField()
    teacherFolder = TeacherFolderSerializer()
    guardiansEnabled = serializers.BooleanField()
    gradebookSettings = GradebookSettingsSerializer()
