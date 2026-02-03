import csv
from django.http import JsonResponse
from django.db.models import Q
from .models import County, SubCounty, Ward

# GET /api/counties/
def get_counties(request):
    counties = County.objects.all().order_by('name').values('id', 'name', 'latitude', 'longitude')
    return JsonResponse(list(counties), safe=False)


# GET /api/subcounties/?county=Nairobi
def get_subcounties(request):
    county_name = request.GET.get('county')
    subcounties = SubCounty.objects.filter(
        county__name=county_name
    ).order_by('name').values('id', 'name')

    return JsonResponse(list(subcounties), safe=False)


# GET /api/wards/?subcounty=Westlands
def get_wards(request):
    subcounty_name = request.GET.get('subcounty')
    wards = Ward.objects.filter(
        subcounty__name=subcounty_name
    ).values(
        'id',
        'name',
        'subcounty__name',
        'subcounty__county__name'
    )

    data = [
        {
            "id": w["id"],
            "name": w["name"],
            "sub_county_name": w["subcounty__name"],
            "county_name": w["subcounty__county__name"],
        }
        for w in wards
    ]

    return JsonResponse(data, safe=False)


# GET /api/wards/<id>/
def get_ward(request, ward_id):
    ward = Ward.objects.select_related(
        'subcounty__county'
    ).get(id=ward_id)

    return JsonResponse({
        "id": ward.id,
        "name": ward.name,
        "sub_county_name": ward.subcounty.name,
        "county_name": ward.subcounty.county.name,
    })

def get_nearest_ward(request):
    try:
        lat = float(request.GET.get("lat"))
        lng = float(request.GET.get("lng"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid coordinates"}, status=400)

    # Simple nearest calculation (Euclidean for demo; use Haversine for real)
    wards = Ward.objects.all().values(
        "id", "name", "subcounty__name", "subcounty__county__name", "latitude", "longitude"
    )

    def distance(w):
        return (w["latitude"] - lat)**2 + (w["longitude"] - lng)**2

    nearest = min(wards, key=distance)

    return JsonResponse({
        "id": nearest["id"],
        "name": nearest["name"],
        "sub_county_name": nearest["subcounty__name"],
        "county_name": nearest["subcounty__county__name"],
        "latitude": nearest["latitude"],
        "longitude": nearest["longitude"],
    })


# GET /api/wards/search/?q=Kangemi
def search_wards(request):
    q = request.GET.get("q", "")
    wards = Ward.objects.filter(name__icontains=q)[:20]
    data = [
        {
            "id": w.id,
            "name": w.name,
            "sub_county_name": w.subcounty.name,
            "county_name": w.subcounty.county.name,
        }
        for w in wards
    ]
    return JsonResponse(data, safe=False)

def get_latitude_longitude(request):
    data = {
        "counties": list(
            County.objects.values("id", "name", "latitude", "longitude")
        ),
        "subcounties": list(
            SubCounty.objects.values("id", "name", "latitude", "longitude")
        ),
        "wards": list(
            Ward.objects.values("id", "name", "latitude", "longitude")
        ),
    }

    return JsonResponse(data)

