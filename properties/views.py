from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .utils import get_all_properties


@cache_page(60 * 15)
def property_list(request):
	"""Return all properties (cached at view level for 15 minutes)."""
	properties = get_all_properties()

	data = [
		{
			'id': p.id,
			'title': p.title,
			'description': p.description,
			'price': str(p.price),
			'location': p.location,
			'created_at': p.created_at.isoformat(),
		}
		for p in properties
	]

	return JsonResponse(data, safe=False)
