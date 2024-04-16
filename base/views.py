import uuid
from django.db.models import Q
from .models import UploadedPDF, Chunk
from .forms import UploadPDFForm
from django.http import FileResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from langchain.document_loaders import PyPDFLoader
#from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

def home(request):
    return render(request, 'home.html')

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # text_splitter = TokenTextSplitter(
    #     chunk_size=10000,
    #     chunk_overlap=1000,
    # )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000, 
        separators=[ "(?<=\. )", "\n\n", "\n", " ", ""]
    )

    docs = text_splitter.split_documents(pages)
    chunks = [doc.page_content for doc in docs]

    return chunks

def pdf_upload(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.pdf_uuid = uuid.uuid4()
            pdf.save()
            chunks = process_pdf(pdf.PDF_file.path)

            for chunk in chunks:
                Chunk.objects.create(pdf=pdf, content=chunk)

            return redirect('pdf_list')
    else:
        form = UploadPDFForm()
    return render(request, 'pdf_upload.html', {'form': form})

def pdf_list(request):
    pdfs = UploadedPDF.objects.all()
    items_per_page = 20
    
    paginator = Paginator(pdfs, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pdf_list.html', {'page_obj': page_obj})

def pdf_detail(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    chunks = Chunk.objects.filter(pdf=pdf).order_by('id')

    items_per_page = 20
    paginator = Paginator(chunks, items_per_page)
    page_number = request.GET.get('page')
    chunks_page = paginator.get_page(page_number)

    return render(request, 'pdf_detail.html', {'pdf': pdf, 'chunks': chunks_page})

def pdf_delete(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    if request.method == 'POST':
        pdf.delete()
        return redirect('pdf_list')
    return render(request, 'pdf_delete.html', {'pdf': pdf})

def pdf_download(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    response = FileResponse(open(pdf.pdf_file.path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.pdf_file.name}"'
    return response

def search_results(request):
    query = request.GET.get('q')
    if query:
        results = UploadedPDF.objects.filter(
            Q(title__icontains=query) | Q(PDF_file__icontains=query)
        )
    else:
        results = []

    items_per_page = 20
    paginator = Paginator(results, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_results.html', {'page_obj': page_obj, 'query': query})

def chunk_detail(request, pdf_id, chunk_index):
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    chunk = get_object_or_404(Chunk, pdf=pdf, id=chunk_index)
    return render(request, 'chunk_detail.html', {'pdf': pdf, 'chunk': chunk})