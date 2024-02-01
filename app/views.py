import json
import logging
import os
from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)


class HomePage(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'app/homepage.html', {})


class SaveStream(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        audio_dir = 'audio_files'

        chunk_file = request.FILES['chunk']

        timestamp = datetime.now().timestamp()

        file_name = f'file_chunk_{timestamp}.webm'
        file_path = os.path.join(audio_dir, file_name)

        try:
            with open(file_path, 'wb') as file:
                for chunk_data in chunk_file.chunks():
                    file.write(chunk_data)

                return JsonResponse({
                    'file_name': file_name
                }, status=200)
        except Exception as E:
            logger.error(str(E), exc_info=True)

        return JsonResponse({
            'status': 'error'
        }, status=500)


class SaveAudio(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        audio_dir = 'audio_files'
        timestamp = datetime.now().timestamp()

        chunk_files = json.loads(request.POST['file_chunks'])

        final_file = os.path.join(audio_dir, f'final_file_{timestamp}.webm')

        try:
            for current_chunk in chunk_files:
                chunk_file = os.path.join(audio_dir, current_chunk)

                with open(final_file, 'ab') as file:
                    with open(chunk_file, 'rb') as chunk_file:
                        file.write(chunk_file.read())

            return JsonResponse({
                'file_name': final_file
            }, status=200)

        except Exception as E:
            logger.error(str(E), exc_info=True)

        return JsonResponse({
            'status': 'error'
        }, status=500)
