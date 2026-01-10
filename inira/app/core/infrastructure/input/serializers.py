from rest_framework import serializers
from collections import defaultdict
import re

class EnrolmentSerializer(serializers.Serializer):
    userid = serializers.IntegerField(required=True)
    courseid = serializers.IntegerField(required=True)


class MoodleEnrolmentParamsSerializer(serializers.Serializer):
    """
    Parser automático para parámetros Moodle del tipo:
    enrolments[0][userid]=...
    enrolments[0][courseid]=...
    """
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    moodlewsrestformat = serializers.CharField(required=False)
    enrolments = EnrolmentSerializer(many=True, required=True)

    def to_internal_value(self, data):

        parsed_data = {
            'wstoken': data.get('wstoken'),
            'wsfunction': data.get('wsfunction'),
            'moodlewsrestformat': data.get('moodlewsrestformat', 'json'),
        }

        enrolments_dict = defaultdict(dict)

        patron = re.compile(r'enrolments\[(\d+)\]\[(\w+)\]')

        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                indice = int(match.group(1))
                campo = match.group(2)

                # Validaciones de número
                if campo in ['userid', 'courseid']:
                    if valor == '':
                        raise serializers.ValidationError({
                            campo: "Este campo es obligatorio y debe ser un número."
                        })
                    try:
                        valor = int(valor)
                    except ValueError:
                        raise serializers.ValidationError({
                            campo: f"Valor inválido: {valor}"
                        })

                enrolments_dict[indice][campo] = valor

        parsed_data['enrolments'] = [
            enrolments_dict[i] for i in sorted(enrolments_dict.keys())
        ]

        return super().to_internal_value(parsed_data)
