#where we create the endpoints
from django.http import JsonResponse
from .models import DocumentToRead
from .serializers import DocumentToReadSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .rag import *

@api_view(['GET','POST'])
def document_extracton(request):
    if request.method == 'GET':
        documents = DocumentToRead.objects.all()
        serializer = DocumentToReadSerializer(documents, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DocumentToReadSerializer(data=request.data)
        if serializer.is_valid():
            base64_encoded_pdf = serializer._validated_data['base64_string']
            prompt_description = serializer._validated_data['prompt_description']
            document_result = run_document_analysis(base64_encoded_pdf, prompt_description)
            return JsonResponse(document_result, safe=False)  # Ensure safe serialization
       
        else:
            return JsonResponse(serializer.errors, status=400)  # Return validation errors



@api_view(['GET', 'POST'])
def documents_list(request):

    if request.method == 'GET':
        documents = DocumentToRead.objects.all()
        serializer = DocumentToReadSerializer(documents, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DocumentToReadSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

     
@api_view(['GET', 'PUT', 'DELETE'])
def document_info(request, id):
    try:
        document = DocumentToRead.objects.get(pk=id)
    except DocumentToRead.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    DocumentToRead.objects.get(pk=id)

    if request.method == 'GET':
        seriarializer = DocumentToReadSerializer(document)
        return Response(seriarializer.data)
    elif request.method == 'POST':
        seriarializer = DocumentToReadSerializer(document, data = request.data)
        if seriarializer.is_valid():
            seriarializer.save()
            return Response(seriarializer.data)
        return Response(seriarializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
