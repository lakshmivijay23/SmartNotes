from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Notes
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from .forms import NotesForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


def add_like_view(request, pk):
    if request.method=="POST":
        note = get_object_or_404(Notes, pk=pk)
        note.likes+=1
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404

def change_visibility_view(request, pk):
    if request.method=="POST":
        note = get_object_or_404(Notes, pk=pk)
        note.is_public=not note.is_public
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404

class NotesUpdateView(UpdateView):
    model=Notes
    success_url='/smart/notes'
    form_class=NotesForm

class NotesDeleteView(DeleteView):
    model=Notes
    # success_url='/smart/notes'
    success_url = reverse_lazy('notes.list')
    template_name='notes/notes_delete.html'
    
class NotesCreateView(CreateView):
    model=Notes
    # fields=["title", "text"]
    success_url='/smart/notes'
    form_class=NotesForm

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name="notes"
    template_name='notes/notes_list.html'
    login_url="/admin"

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(DetailView):
    model=Notes
    context_object_name="note"
    template_name="notes/notes_detail.html"

class NotesPublicDetailView(DetailView):
    model=Notes
    context_object_name="note"
    queryset=Notes.objects.filter(is_public=True)

class PopularNotesListView(ListView):
    model = Notes
    context_object_name="notes"
    template_name='notes/notes_list.html'
    queryset=Notes.objects.filter(likes__gte=1).order_by('-likes')