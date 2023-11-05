from django.shortcuts import render
from .mongo_utils import get_metadata  # Adjust the import path as necessary

def search_metadata_view(request):
    # Initialize the context with None or empty values
    context = {
        'metadata': None,
        'age_min': '',
        'age_max': '',
        'sex': '',
        'anatomical_sites': ['anterior torso', 'upper extremity', 'posterior torso', 'lower extremity', 'lateral torso', 'head/neck', 'palms/soles', 'oral/genital'],  # this should be a predefined list of sites
        'diagnosis_options': ["MEL", "NV", "BCC", "AK", "BKL", "DF", "VASC", "SCC", "UNK"],  # this should be a predefined list of diagnosis codes
        'selected_anatomical_sites': [],  # this will hold what the user has selected
        'selected_diagnosis_codes': []  # this will hold what the user has selected
    }

    if request.method == 'GET':
        age_min = request.GET.get('age_min')
        age_max = request.GET.get('age_max')
        sex = request.GET.get('sex')
        selected_anatomical_sites = request.GET.getlist('anatomical_site')  # This gets a list of items selected by the user
        selected_diagnosis_codes = request.GET.getlist('diagnosis_code')  # This gets a list of diagnosis codes selected by the user

        # Only apply age range filter if both min and max are provided
        age_range = (int(age_min), int(age_max)) if age_min and age_max else None

        # Update context with the selected form data for persistence in the form fields
        context.update({
            'age_min': age_min,
            'age_max': age_max,
            'sex': sex,
            'selected_anatomical_sites': selected_anatomical_sites,
            'selected_diagnosis_codes': selected_diagnosis_codes
        })

        # Call the function with the filters
        if age_range or sex or selected_anatomical_sites or selected_diagnosis_codes:
            context['metadata'] = get_metadata(
                age_range=age_range,
                sex=sex,
                anatomical_sites=selected_anatomical_sites,
                diagnosis_codes=selected_diagnosis_codes
            )

    # Render the page with the form and the search results (if any)
    return render(request, 'search_results.html', context)
