from django.contrib.postgres.search import SearchVector
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import Symptom, PatientAppointment
from doctor_profiles.serializers.symptom_serializers import SymptomSerializer, SymptomCreateSerializer, \
    PatientSymptomCreateSerializer, PatientSymptomSerializer


class ApiPublicSymptomList(APIView):
    """
    List of symptoms
    [optional]
    ?s=str
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)

        if s:
            symptoms = Symptom.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(search__icontains=s)
        else:
            symptoms = Symptom.objects.all()

        serializer = SymptomSerializer(symptoms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivateSymptomCreate(APIView):
    """
    Add a new symptom
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SymptomCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPrivatePatientSymptomList(APIView):
    """
    Load symptoms from checkup
    ?appointment_id=id
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment_id', None))
        serializer = PatientSymptomSerializer(appointment.get_symptoms(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPrivatePatientSymptomCreate(APIView):
    """
    Attach symptom to patient
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = PatientSymptomCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
