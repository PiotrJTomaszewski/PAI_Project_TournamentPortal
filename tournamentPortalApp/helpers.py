from django.contrib import messages
from django.core.files import File

from io import BytesIO
from PIL import Image

def formErrorsToMessage(form, request):
    for error in form.errors:
        err_msg = ', '.join(form.errors[error])
        messages.add_message(request, messages.ERROR, ': '.join([error.title(), err_msg]))

def makeThumbnail(org_image, size=(200, 200)):
    image = Image.open(org_image)
    image.convert('RGB')
    image.thumbnail(size)
    b_io = BytesIO()
    image.save(b_io, 'WebP')
    thumbnail = File(b_io, name=org_image.name)
    return thumbnail