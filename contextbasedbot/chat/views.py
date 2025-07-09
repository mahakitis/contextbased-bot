from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Document, ChatHistory
from .services.embedding import embed_and_store_text
from .services.retrieval import search_similar_chunks, get_context_from_results
from .services.pdf_handler import process_pdf_upload
from .services.web_scraper import scrap_website
from .services.youtube_handler import get_youtube_subtitle_text
from .services.llm_call import generate_answer, rephrase_question
import json

class HomePageView(View):
    def get(self, request):
        return render(request, 'chat/index.html')

    def post(self, request):
        input_type = request.POST.get('input_type')
        uploaded_file = request.FILES.get('input_value')
        input_value_url = request.POST.get('input_value_url')

        if input_type == 'pdf' and uploaded_file:
            content = process_pdf_upload(uploaded_file)
            title = uploaded_file.name
        elif input_type == 'web':
            content = scrap_website(input_value_url)
            title = input_value_url
        elif input_type == 'youtube':
            content = get_youtube_subtitle_text(input_value_url)
            title = input_value_url
        else:
            return render(request, 'chat/index.html', {'error': 'Invalid input'})

        document = Document.objects.create(title=title, doc_type=input_type)
        request.session['doc_id'] = str(document.doc_id)

        embed_and_store_text(content, document)
        return redirect('/chat/')

class ChatView(View):
    def get(self, request):
        doc_id = request.session.get('doc_id')
        if not doc_id:
            return redirect('/')
        history = ChatHistory.objects.filter(document_id=doc_id).order_by('asked_at')
        return render(request, 'chat/chat.html', {'history': history})

class ChatQueryAPI(View):
    def post(self, request):
        doc_id = request.session.get('doc_id')
        if not doc_id:
            return JsonResponse({"error": "No session found"}, status=400)

        try:
            data = json.loads(request.body)
            question = data.get('question')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)

        previous_qa = ChatHistory.objects.filter(document_id=doc_id).order_by('-asked_at').first()
        previous_question = previous_qa.question if previous_qa else None

        rephrased_question = rephrase_question(question, previous_question)

        results = search_similar_chunks(rephrased_question, top_k=5, document_id=doc_id)
        context = get_context_from_results(results)

        answer = generate_answer(rephrased_question, context)

        ChatHistory.objects.create(
            document_id=doc_id,
            question=question, 
            answer=answer
        )

        return JsonResponse({"answer": answer})


class NewSessionView(View):
    def get(self, request):
        request.session.pop('doc_id', None)
        document = Document.objects.create(title="New Session", doc_type="blank")
        request.session['doc_id'] = str(document.doc_id)
        return redirect('/chat/')
