from django.shortcuts import render


def home_screen_view(request):
	context = {}
	return render(request, "personal/side-menu-light-profile-overview-1.html", context)
