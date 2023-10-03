from django.shortcuts import render

def show_images(request):
    if request.method == 'POST':
        image_urls = request.POST.get('image_urls')
        image_list = image_urls.split(',')
        context = {'image_list': image_list}
        return render(request, 'show_images.html', context)
    else:
        return render(request, 'image_input.html')
