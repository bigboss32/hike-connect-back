from rest_framework import serializers
import re
from collections import defaultdict


class MoodleGetParamsSerializer(serializers.Serializer):
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    options = serializers.DictField(child=serializers.ListSerializer(
        child=serializers.IntegerField()
    ))

    def to_internal_value(self, data):
        """
        Convierte options[ids][0] y similares a una estructura Python.
        Permite vacío solo en options[ids][0].
        """

        parsed_data = {
            'wstoken': data.get('wstoken'),
            'wsfunction': data.get('wsfunction'),
            'options': {}
        }

        options_dict = defaultdict(list)
        patron = re.compile(r'options\[(\w+)\]\[(\d+)\]')

        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                key = match.group(1)
                index = int(match.group(2))

                # Permitir vacío solo en options[ids][0]
                if valor == '':
                    if not (key == 'ids' and index == 0):
                        raise serializers.ValidationError({key: 'El valor no puede estar vacío.'})
                    # simplemente no añadir el valor (queda None)
                    while len(options_dict[key]) <= index:
                        options_dict[key].append(None)
                    continue

                try:
                    valor = int(valor)
                except ValueError:
                    raise serializers.ValidationError({key: f'Valor inválido: {valor}'})

                while len(options_dict[key]) <= index:
                    options_dict[key].append(None)

                options_dict[key][index] = valor

        for key, lista in options_dict.items():
            parsed_data['options'][key] = [x for x in lista if x is not None]

        return super().to_internal_value(parsed_data)
