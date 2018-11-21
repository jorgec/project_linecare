"""
- InsuranceProvider
--- ApiPublicInsuranceProviderList
--- ApiPublicInsuranceProviderDetail
--- ApiPrivateInsuranceProviderCreate

- DoctorInsurance
--- ApiPublicDoctorInsuranceList
--- ApiPublicDoctorInsuranceDetail
--- ApiPrivateDoctorInsuranceDetail
--- ApiPrivateDoctorInsuranceCreate
--- ApiPrivateDoctorInsuranceUpdate
--- ApiPrivateDoctorInsuranceDelete
"""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from doctor_profiles.models import InsuranceProvider, DoctorInsurance
from doctor_profiles.serializers import InsuranceProviderCreateSerializer, InsuranceProviderSerializer, \
    DoctorInsuranceSerializer, DoctorInsuranceCreateSerializer, DoctorInsuranceUpdateSerializer, \
    DoctorInsurancePublicSerializer, InsuranceProviderPublicSerializer


class ApiPrivateInsuranceProviderCreate(APIView):
    """
    Create Insurance Provider
    Requires doctor profile
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.doctor_profile():
            return Response("Only Doctors can perform this action", status=status.HTTP_401_UNAUTHORIZED)

        serializer = InsuranceProviderCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPublicInsuranceProviderList(APIView):
    """
    Get list of all approved Insurance Providers
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        insurance_providers = InsuranceProvider.objects.filter(is_approved=True)
        serializer = InsuranceProviderPublicSerializer(insurance_providers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicInsuranceProviderDetail(APIView):
    """
    Get specific Insurance Provider
    ?id=id or ?slug=slug
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        slug = request.GET.get('slug', None)
        if id is not None:
            try:
                insurance_provider = InsuranceProvider.objects.get(id=id, is_approved=True)
            except InsuranceProvider.DoesNotExist:
                insurance_provider = None
        elif slug is not None:
            try:
                insurance_provider = InsuranceProvider.objects.get(slug=slug, is_approved=True)
            except InsuranceProvider.DoesNotExist:
                insurance_provider = None
        else:
            insurance_provider = None

        if insurance_provider is not None:
            serializer = InsuranceProviderPublicSerializer(insurance_provider)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


################################################################################
# Doctor Insurance
################################################################################


class ApiPublicDoctorInsuranceList(APIView):
    """
    Get Insurance Providers of doctor profile
    ?user=n
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, id=request.GET.get('user', None))
        if user.doctor_profile():
            insurance_providers = user.doctor_profile().get_insurance_providers()
            serializer = DoctorInsuranceSerializer(insurance_providers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND)


class ApiPrivateDoctorInsuranceCreate(APIView):
    """
    Create Insurance Provider to doctor profile
    ?user=n
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.doctor_profile():
            serializer = DoctorInsuranceCreateSerializer(data=request.data)

            if serializer.is_valid():
                doctor_insurance_kwargs = serializer.validated_data
                doctor_insurance_kwargs['doctor'] = user.doctor_profile()

                doctor_insurance = DoctorInsurance(**doctor_insurance_kwargs)
                try:
                    doctor_insurance.save()
                except IntegrityError:
                    return Response(
                        {
                            "Duplicate Insurance Provider": "You already registered this insurance provider!"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except ValueError as err:
                    return Response(
                        {
                            "Value Error": str(err)
                        }, status=status.HTTP_400_BAD_REQUEST)
                return_serializer = DoctorInsuranceSerializer(doctor_insurance)
                return Response(return_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User does not have a Doctor profile", status=status.HTTP_404_NOT_FOUND)


class ApiPrivateDoctorInsuranceUpdate(APIView):
    """
    Updates Insurance Provider of doctor profile
    ?insurance=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_insurance = get_object_or_404(DoctorInsurance, id=request.GET.get('insurance', None),
                                             doctor=request.user.doctorprofile)

        serializer = DoctorInsuranceUpdateSerializer(data=request.data)

        if serializer.is_valid():
            doctor_insurance.identifier = serializer.validated_data['identifier']
            doctor_insurance.save()
            return_serializer = DoctorInsuranceSerializer(doctor_insurance)
            return Response(return_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)


class ApiPrivateDoctorInsuranceDelete(APIView):
    """
    Deletes Insurance Provider of doctor profile
    ?insurance=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_insurance = get_object_or_404(DoctorInsurance, id=request.GET.get('insurance', None),
                                             doctor=request.user.doctorprofile)

        doctor_insurance.delete()
        return Response("Insurance deleted", status=status.HTTP_200_OK)


class ApiPrivateDoctorInsuranceDetail(APIView):
    """
    Detail of Insurance Provider of doctor profile
    ?insurance=id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_insurance = get_object_or_404(DoctorInsurance, id=request.GET.get('insurance', None),
                                             doctor=request.user.doctorprofile)

        serializer = DoctorInsuranceSerializer(doctor_insurance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicDoctorInsuranceDetail(APIView):
    """
    Public details of Insurance Provider
    ?insurance=id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor_insurance = get_object_or_404(DoctorInsurance, id=request.GET.get('insurance', None))

        serializer = DoctorInsurancePublicSerializer(doctor_insurance)
        return Response(serializer.data, status=status.HTTP_200_OK)
