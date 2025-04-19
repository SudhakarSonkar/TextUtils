from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def analyze(request):
    # Get the text input from user
    djtext = request.POST.get('text', '').strip()

    # Get checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcounter = request.POST.get('charcounter', 'off')

    # Return error if no text or no operation is selected
    if not djtext or all(val == 'off' for val in [removepunc, fullcaps, newlineremover, extraspaceremover, charcounter]):
        return render(request, 'analyze.html', {
            'error': 'Please enter some text and select at least one operation.'
        })

    analyzed = djtext
    purpose_list = []

    # Remove punctuations
    if removepunc == "on":
        punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        analyzed = "".join(char for char in analyzed if char not in punctuations)
        purpose_list.append('Removed Punctuations')

    # Convert to UPPERCASE
    if fullcaps == "on":
        analyzed = analyzed.upper()
        purpose_list.append('Converted to UPPERCASE')

    # Remove new lines
    if newlineremover == "on":
        analyzed = "".join(char for char in analyzed if char not in ['\n', '\r'])
        purpose_list.append('Removed New Lines')

    # Remove extra spaces
    if extraspaceremover == "on":
        while "  " in analyzed:
            analyzed = analyzed.replace("  ", " ")
        purpose_list.append('Removed Extra Spaces')

    # Character counter
    if charcounter == "on":
        count = len(analyzed)
        purpose_list.append('Counted Characters')
        return render(request, 'analyze.html', {
            'purpose': ', '.join(purpose_list),
            'analyzed_text': f"Character Count: {count}"
        })

    # Final result
    return render(request, 'analyze.html', {
        'purpose': ', '.join(purpose_list),
        'analyzed_text': analyzed
    })
