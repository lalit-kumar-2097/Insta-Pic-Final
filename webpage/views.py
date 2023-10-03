from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return HttpResponse("Hello World")


def show_images(request):
    if request.method == 'POST':        
        image_urls = request.POST.get('image_urls')
        image_list = image_urls.split(',')
        print(type(image_list))        
        serial_no = list(range(1,len(image_list)+1))
        print(type(serial_no))
        # context = {'image_list': image_list,'serial_no': serial_no}
        context = {'image_list': zip(image_list,serial_no)}
        return render(request, 'show_images.html', context)
    else:
        return render(request, 'image_input.html')
    
    






