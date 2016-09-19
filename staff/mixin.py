from django.shortcuts import render

class UserCheckMixin(object):

	def get(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')


	# def dispatch(self, request, *args, **kwargs):
	# 	if not self.check_user(request.user):
	# 		return self.user_check_failed(request, *args, **kwargs)
	# 	return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)