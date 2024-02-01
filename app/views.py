import os

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View


class HomePage(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'app/homepage.html', {})


class SaveStream(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        audio_dir = 'audio_files'

        chunk_file = request.FILES['chunk']
        chunk_count = request.POST['chunk_count']

        file_name = f'temporary_chunk_{chunk_count}.webm'
        file_path = os.path.join(audio_dir, file_name)

        try:
            with open(file_path, 'wb') as file:
                for chunk_data in chunk_file.chunks():
                    file.write(chunk_data)
        except Exception as E:
            print(E)

        return JsonResponse({
            'data': 'ack'
        }, status=200)


class SaveAudio(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        audio_dir = 'audio_files'

        total_chunk = int(request.POST['total_chunk'])
        final_file = os.path.join(audio_dir, 'final_file.webm')

        for index in range(1, total_chunk + 1):
            file_name = f'temporary_chunk_{index}.webm'
            chunk_file = os.path.join(audio_dir, file_name)

            with open(final_file, 'ab') as file:
                with open(chunk_file, 'rb') as chunk_file:
                    file.write(chunk_file.read())

        return JsonResponse({
            'data': 'ack'
        }, status=200)
