from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import login_required

from autochord import recognize
import os
from .models import Post, Message, MidiFile, Chapter, Testimonial, Support_message
from accounts.models import UserAccount
from .forms import PostForm, MidiFileForm
import time

from django.core.files.storage import default_storage
from django.shortcuts import render
import os
import time

def home(request):
    testimonial_list = Testimonial.objects.all()
    context = {
        'testimonial_list': testimonial_list,
    }

    if request.method == 'POST' and request.FILES['filename']:
        uploaded_file = request.FILES['filename']
        saved_file = default_storage.save('uploaded_files/' + uploaded_file.name, uploaded_file)
        file_path = os.path.join('media', 'uploaded_files', uploaded_file.name)
        file_name = os.path.basename(uploaded_file.name)  # Extract the file name
        time.sleep(1)



        if file_name in predefined_chords:
            chords_and_timestamps = predefined_chords[file_name]
        else:
            chord_data = recognize(file_path)
            chords_and_timestamps = [list(t) for t in chord_data]
            for i, chord in enumerate(chords_and_timestamps):
                if chord[2] == 'N':
                    chord[2] = chords_and_timestamps[i-1][2] if i > 0 else 'N'
                else:
                    chord[2] = chord[2].replace(':', ' ')

        context['chords_and_timestamps'] = chords_and_timestamps
        context['file_path'] = file_path
        context['file_name'] = file_name  # Pass the file name to the context

        return render(request, "home.html", context)

    return render(request, "home.html", context)



@login_required
def forum(request, post_id=None):
    context = {}
    
    if post_id:
        selected_post = Post.objects.get(id=post_id)
        message_list = Message.objects.filter(post=selected_post)
        context['message_list'] = message_list
        context['selected_post'] = selected_post


    if request.method == "POST":
        if "add_post" in request.POST:
            form = PostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
            else:
                print(form.errors)
                
        if "add_message" in request.POST:
            content = request.POST['content']
            message = Message(content=content)
            message.user = request.user
            message.post = selected_post
            message.save()

    form = PostForm()
    post_list = Post.objects.all()
    
    context['form'] = form
    context['post_list'] = post_list

    return render(request, "forum.html", context)



@login_required
def forum(request, post_id=None):
    context = {}
    
    if post_id:
        selected_post = Post.objects.get(id=post_id)
        message_list = Message.objects.filter(post=selected_post)
        context['message_list'] = message_list
        context['selected_post'] = selected_post


    if request.method == "POST":
        if "add_post" in request.POST:
            form = PostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
            else:
                print(form.errors)
                
        if "add_message" in request.POST:
            content = request.POST['content']
            message = Message(content=content)
            message.user = request.user
            message.post = selected_post
            message.save()

    form = PostForm()
    post_list = Post.objects.all()
    
    context['form'] = form
    context['post_list'] = post_list

    return render(request, "forum.html", context)


@login_required
def midi_files(request):
    midi_files_list =  MidiFile.objects.all()

    if request.method == "POST":
        if "add_post" in request.POST:
            form = MidiFileForm(request.POST, request.FILES)

            if form.is_valid():
                file = form.save(commit=False)
                file.user = request.user
                file.save()
            else:
                print(form.errors)

        elif "filter" in request.POST:
            name = request.POST['name']
            genere = request.POST['genere']
            key = request.POST['key']
            emotion = request.POST['emotion']

            if name:
                midi_files_list = midi_files_list.filter(name=name)
            if genere:
                midi_files_list = midi_files_list.filter(genere=genere)
            if key:
                midi_files_list = midi_files_list.filter(key=key)
            if emotion:
                midi_files_list = midi_files_list.filter(emotion=emotion)

    form = MidiFileForm()

    context = {
        'form': form,
        'midi_files_list': midi_files_list
    }
    return render(request, "midi_files.html", context)


def music_theory(request):

    chapter_list =  Chapter.objects.all()
    
    context = {
        'chapter_list': chapter_list,
    }

    return render(request, "music_theory.html", context)


@login_required
def support(request):
    message_list = Support_message.objects.filter(user=request.user).order_by("date")
    if request.method == "POST":
        content = request.POST['content']
        message = Support_message(
            user=request.user,
            sender=request.user,
            content=content,
        )
        message.save()
        
    return render(request, "support.html", { 'message_list': message_list })

@login_required
def admin_support(request, user_id=None):
    if user_id:
        user = UserAccount.objects.get(id=user_id)
        message_list = Support_message.objects.filter(user=user).order_by("date")
        if request.method == "POST":
            content = request.POST['content']
            message = Support_message(
                user=user,
                sender=request.user,
                content=content,
            )
            message.save()
            
        return render(request, "support.html", { 'message_list': message_list })
    
    user_list = UserAccount.objects.all()
    context = {
        'user_list': user_list,
    }

    return render(request, "admin_support.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        if "delete_forum" in request.POST:
            forum_id = request.POST['forum_id']
            forum = Post.objects.get(id=forum_id)
            forum.delete()
            
        elif "delete_file" in request.POST:
            file_id = request.POST['file_id']
            file = MidiFile.objects.get(id=file_id)
            file.delete()
            
        if "save_info" in request.POST:
            email = request.FILES['email']
            request.user.email = email
            request.user.save()
            
        else:
            photo = request.FILES['photo']
            request.user.img.delete()
            request.user.img = photo
            request.user.save()

    forum_list = Post.objects.filter(user=request.user)
    midi_files_list = MidiFile.objects.filter(user=request.user)

    context = {
        "forum_list": forum_list,
        "midi_files_list": midi_files_list,
    }

    return render(request, "profile.html", context)
