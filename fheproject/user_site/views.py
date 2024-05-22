from django.shortcuts import render, redirect
from .forms import InsuranceForm, DecryptForm
from .models import InsuranceData
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime



# FHE Stuff
import tenseal as ts
import base64


# Create Admin Approval Page
def admin_approval(request):
    insurance_list = InsuranceData.objects.all()

    if request.user.is_superuser:

        if request.method == 'POST':
            
            id_list = request.POST.getlist('boxes')

            # Uncheck all events
            insurance_list.update(approved=False)

            # Update the list

            for x in id_list:
                InsuranceData.objects.filter(pk=int(x)).update(approved=True)

            
            messages.success(request, ("Insurance Approval successful"))
            return redirect('home')

        else:

            return render(request, 'site/admin_approval.html', {
                "insurance_list": insurance_list, 
        })
    else:
        messages.success(request, ("You aren't authorized to view this page!"))
        return redirect('home')



# Create your views here.

def string_to_numeric_ordinal(string):
  """Encodes a string into a list of numeric values using ordinal encoding."""
  return [ord(char) for char in string]
def extract_name(data_list: list):
   temp_list = data_list

   return ''.join([chr(int(char)) for char in temp_list])



def gen_key(request):

    rest = request.GET.get('rest')
    file_name = str(request.user) + " " + rest + ".txt"
                
    context = ts.context(ts.SCHEME_TYPE.CKKS, 
                poly_modulus_degree = 8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60]
            )

    context.global_scale = 2**40
    context.generate_galois_keys()

    secret_context = context.serialize(save_secret_key=True)

    context.make_context_public()          #drops private key
    public_context = context.serialize()

    if type(secret_context) == bytes:
        secret_context = base64.b64encode(secret_context)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)

    response.write(secret_context)

    return response


def decrypt_and_view(request, username):
    if request.method == 'POST':
        form = DecryptForm(request.POST, request.FILES)
        if form.is_valid():
            secret_key_file = form.cleaned_data['secret_key_file']
            secret_key_content = secret_key_file.read()
            secret_context_bytes = base64.b64decode(secret_key_content)
            context = ts.context_from(secret_context_bytes)
    
            # Fetch all insurances under the user
            insurances = InsuranceData.objects.filter(user__username=username)
            insurances = list(insurances)

            required_insurances = []

            list_len = len(insurances)
            
            # Decrypt data for each entry
            for counter in range(0, list_len, 1):
                
                insurance = insurances[counter]

                try:
                    dec_first_name = insurance.enc_first_name
                    dec_first_name = base64.b64decode(dec_first_name)
                    dec_first_name = ts.ckks_vector_from(context, dec_first_name)
                    dec_first_name = list(map(lambda x: round(x, 2), dec_first_name._decrypt()))

                    dec_first_name = extract_name(dec_first_name)

                    insurance.first_name = dec_first_name

                    # --------------------------------------------------------------------------------

                    dec_last_name = insurance.enc_last_name
                    dec_last_name = base64.b64decode(dec_last_name)
                    dec_last_name = ts.ckks_vector_from(context, dec_last_name)
                    dec_last_name = list(map(lambda x: round(x, 2), dec_last_name._decrypt()))
                    dec_last_name = extract_name(dec_last_name)

                    insurance.last_name = dec_last_name

                    # --------------------------------------------------------------------------------

                    dec_date_of_birth = insurance.enc_date_of_birth
                    dec_date_of_birth = base64.b64decode(dec_date_of_birth)
                    dec_date_of_birth = ts.ckks_vector_from(context, dec_date_of_birth)
                    dec_date_of_birth = list(map(lambda x: round(x, 2), dec_date_of_birth._decrypt()))
                    dec_date_of_birth = extract_name(dec_date_of_birth)

                    date_object_dob = datetime.strptime(dec_date_of_birth, '%Y-%m-%d').date()

                    insurance.date_of_birth = date_object_dob

                    # --------------------------------------------------------------------------------

                    dec_address = insurance.enc_address
                    dec_address = base64.b64decode(dec_address)
                    dec_address = ts.ckks_vector_from(context, dec_address)
                    dec_address = list(map(lambda x: round(x, 2), dec_address._decrypt()))
                    dec_address = extract_name(dec_address)

                    insurance.address = dec_address

                    # --------------------------------------------------------------------------------

                    dec_city = insurance.enc_city
                    dec_city = base64.b64decode(dec_city)
                    dec_city = ts.ckks_vector_from(context, dec_city)
                    dec_city = list(map(lambda x: round(x, 2), dec_city._decrypt()))
                    dec_city = extract_name(dec_city)

                    insurance.city = dec_city

                    # --------------------------------------------------------------------------------

                    dec_state = insurance.enc_state
                    dec_state = base64.b64decode(dec_state)
                    dec_state = ts.ckks_vector_from(context, dec_state)
                    dec_state = list(map(lambda x: round(x, 2), dec_state._decrypt()))
                    dec_state = extract_name(dec_state)

                    insurance.state = dec_state

                    # --------------------------------------------------------------------------------

                    dec_zip_code = insurance.enc_zip_code
                    dec_zip_code = base64.b64decode(dec_zip_code)
                    dec_zip_code = ts.ckks_vector_from(context, dec_zip_code)
                    dec_zip_code = list(map(lambda x: round(x, 2), dec_zip_code._decrypt()))

                    insurance.zip_code = int(dec_zip_code[0])

                    # --------------------------------------------------------------------------------

                    dec_phone_number = insurance.enc_phone_number
                    dec_phone_number = base64.b64decode(dec_phone_number)
                    dec_phone_number = ts.ckks_vector_from(context, dec_phone_number)
                    dec_phone_number = list(map(lambda x: round(x, 2), dec_phone_number._decrypt()))

                    insurance.phone_number = int(dec_phone_number[0])

                    # --------------------------------------------------------------------------------

                    dec_email = insurance.enc_email
                    dec_email = base64.b64decode(dec_email)
                    dec_email = ts.ckks_vector_from(context, dec_email)
                    dec_email = list(map(lambda x: round(x, 2), dec_email._decrypt()))
                    dec_email = extract_name(dec_email)

                    insurance.email = dec_email

                    # --------------------------------------------------------------------------------

                    dec_gender = insurance.enc_gender
                    dec_gender = base64.b64decode(dec_gender)
                    dec_gender = ts.ckks_vector_from(context, dec_gender)
                    dec_gender = list(map(lambda x: round(x, 2), dec_gender._decrypt()))
                    dec_gender = extract_name(dec_gender)

                    insurance.gender = dec_gender

                    # --------------------------------------------------------------------------------

                    if insurance.enc_height == None and insurance.enc_weight == None:
                        pass
                    else:
                        dec_height = insurance.enc_height
                        dec_height = base64.b64decode(dec_height)
                        dec_height = ts.ckks_vector_from(context, dec_height)
                        dec_height = list(map(lambda x: round(x, 2), dec_height._decrypt()))

                        insurance.height = int(dec_height[0])

                        # --------------------------------------------------------------------------------

                        dec_weight = insurance.enc_weight
                        dec_weight = base64.b64decode(dec_weight)
                        dec_weight = ts.ckks_vector_from(context, dec_weight)
                        dec_weight = list(map(lambda x: round(x, 2), dec_weight._decrypt()))

                        insurance.weight = int(dec_weight[0])

                    # --------------------------------------------------------------------------------

                    if insurance.enc_dl_no == None and insurance.enc_license_plate == None:
                        pass
                    else:
                        dec_dl_no = insurance.enc_dl_no
                        dec_dl_no = base64.b64decode(dec_dl_no)
                        dec_dl_no = ts.ckks_vector_from(context, dec_dl_no)
                        dec_dl_no = list(map(lambda x: round(x, 2), dec_dl_no._decrypt()))
                        dec_dl_no = extract_name(dec_dl_no)

                        insurance.dl_no = dec_dl_no

                        # --------------------------------------------------------------------------------

                        dec_license_plate = insurance.enc_license_plate
                        dec_license_plate = base64.b64decode(dec_license_plate)
                        dec_license_plate = ts.ckks_vector_from(context, dec_license_plate)
                        dec_license_plate = list(map(lambda x: round(x, 2), dec_license_plate._decrypt()))
                        dec_license_plate = extract_name(dec_license_plate)

                        insurance.license_plate = dec_license_plate

                    # --------------------------------------------------------------------------------

                    dec_insurance_type = insurance.enc_insurance_type
                    dec_insurance_type = base64.b64decode(dec_insurance_type)
                    dec_insurance_type = ts.ckks_vector_from(context, dec_insurance_type)
                    dec_insurance_type = list(map(lambda x: round(x, 2), dec_insurance_type._decrypt()))
                    dec_insurance_type = extract_name(dec_insurance_type)

                    insurance.insurance_type = dec_insurance_type

                    # --------------------------------------------------------------------------------

                    dec_coverage_amount = insurance.enc_coverage_amount
                    dec_coverage_amount = base64.b64decode(dec_coverage_amount)
                    dec_coverage_amount = ts.ckks_vector_from(context, dec_coverage_amount)
                    dec_coverage_amount = list(map(lambda x: round(x, 2), dec_coverage_amount._decrypt()))

                    insurance.coverage_amount = float(dec_coverage_amount[0])

                    # --------------------------------------------------------------------------------

                    dec_start_date = insurance.enc_start_date
                    dec_start_date = base64.b64decode(dec_start_date)
                    dec_start_date = ts.ckks_vector_from(context, dec_start_date)
                    dec_start_date = list(map(lambda x: round(x, 2), dec_start_date._decrypt()))
                    dec_start_date = extract_name(dec_start_date)

                    date_object_sod = datetime.strptime(dec_start_date, '%Y-%m-%d').date()

                    insurance.start_date = date_object_sod

                    # --------------------------------------------------------------------------------

                    dec_end_date = insurance.enc_end_date
                    dec_end_date = base64.b64decode(dec_end_date)
                    dec_end_date = ts.ckks_vector_from(context, dec_end_date)
                    dec_end_date = list(map(lambda x: round(x, 2), dec_end_date._decrypt()))
                    dec_end_date = extract_name(dec_end_date)

                    date_object_eod = datetime.strptime(dec_end_date, '%Y-%m-%d').date()

                    insurance.end_date = date_object_eod

                    required_insurances.append(insurance)
                
                except:
                    pass

                

            return render(request, 'site/show_insurances.html', {
                'insurances': required_insurances,
                })
    else:
        form = DecryptForm()
    return render(request, 'site/decrypt_data.html', {'form': form})


def insurance_list(request, username):

    form = DecryptForm()

    return render(request, 'site/decrypt_data.html', {
        "form": form,
    })


def insurance_register(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES, request=request)
        if form.is_valid():

            # FHE logic goes here
            secret_key_file = form.cleaned_data['secret_key_file']
            
            secret_key_content = secret_key_file.read()
            secret_context_bytes = base64.b64decode(secret_key_content)
            context = ts.context_from(secret_context_bytes)     # creating context from uploaded secret key


            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']

            gender = form.cleaned_data['gender']

            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']

            dl_no = form.cleaned_data['dl_no']
            license_plate = form.cleaned_data['license_plate']

            insurance_type = form.cleaned_data['insurance_type']
            coverage_amount = form.cleaned_data['coverage_amount']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            name_convention = first_name + " - " + insurance_type


            enc_first_name = list(string_to_numeric_ordinal(first_name))
            enc_first_name = ts.ckks_vector(context, enc_first_name)
            enc_first_name = enc_first_name.serialize()
            enc_first_name = base64.b64encode(enc_first_name)

            enc_last_name = string_to_numeric_ordinal(last_name)
            enc_last_name = ts.ckks_vector(context, enc_last_name)
            enc_last_name = enc_last_name.serialize()
            enc_last_name = base64.b64encode(enc_last_name)

            enc_date_of_birth = list(string_to_numeric_ordinal(str(date_of_birth)))
            enc_date_of_birth = ts.ckks_vector(context, enc_date_of_birth)
            enc_date_of_birth = enc_date_of_birth.serialize()
            enc_date_of_birth = base64.b64encode(enc_date_of_birth)

            enc_address = list(string_to_numeric_ordinal(address))
            enc_address = ts.ckks_vector(context, enc_address)
            enc_address = enc_address.serialize()
            enc_address = base64.b64encode(enc_address)

            enc_city = list(string_to_numeric_ordinal(city))
            enc_city = ts.ckks_vector(context, enc_city)
            enc_city = enc_city.serialize()
            enc_city = base64.b64encode(enc_city)

            enc_state = list(string_to_numeric_ordinal(state))
            enc_state = ts.ckks_vector(context, enc_state)
            enc_state = enc_state.serialize()
            enc_state = base64.b64encode(enc_state)

            
            enc_zip_code = ts.ckks_vector(context, [zip_code])
            enc_zip_code = enc_zip_code.serialize()
            enc_zip_code = base64.b64encode(enc_zip_code)

            
            enc_phone_number = ts.ckks_vector(context, [phone_number])
            enc_phone_number = enc_phone_number.serialize()
            enc_phone_number = base64.b64encode(enc_phone_number)

            enc_email = list(string_to_numeric_ordinal(str(email)))
            enc_email = ts.ckks_vector(context, enc_email)
            enc_email = enc_email.serialize()
            enc_email = base64.b64encode(enc_email)

            enc_gender = list(string_to_numeric_ordinal(gender))
            enc_gender = ts.ckks_vector(context, enc_gender)
            enc_gender = enc_gender.serialize()
            enc_gender = base64.b64encode(enc_gender)

            if (height == 0 and weight==0) or insurance_type == 'auto':
                enc_height = None
                enc_weight = None
            else:                    
                enc_height = ts.ckks_vector(context, [height])
                enc_height = enc_height.serialize()
                enc_height = base64.b64encode(enc_height)

                enc_weight = ts.ckks_vector(context, [weight])
                enc_weight = enc_weight.serialize()
                enc_weight = base64.b64encode(enc_weight)



            if (str(dl_no) == "None" and str(license_plate) == "None") or insurance_type == 'health':
                enc_dl_no = None
                enc_license_plate = None
            else:
                enc_dl_no = list(string_to_numeric_ordinal(dl_no))
                enc_dl_no = ts.ckks_vector(context, enc_dl_no)
                enc_dl_no = enc_dl_no.serialize()
                enc_dl_no = base64.b64encode(enc_dl_no)    

                enc_license_plate = list(string_to_numeric_ordinal(license_plate))
                enc_license_plate = ts.ckks_vector(context, enc_license_plate)
                enc_license_plate = enc_license_plate.serialize()
                enc_license_plate = base64.b64encode(enc_license_plate)

            enc_insurance_type = list(string_to_numeric_ordinal(insurance_type))
            enc_insurance_type = ts.ckks_vector(context, enc_insurance_type)
            enc_insurance_type = enc_insurance_type.serialize()
            enc_insurance_type = base64.b64encode(enc_insurance_type)


            enc_coverage_amount = ts.ckks_vector(context, [coverage_amount])
            enc_coverage_amount = enc_coverage_amount.serialize()
            enc_coverage_amount = base64.b64encode(enc_coverage_amount)

            enc_start_date = list(string_to_numeric_ordinal(str(start_date)))
            enc_start_date = ts.ckks_vector(context, enc_start_date)
            enc_start_date = enc_start_date.serialize()
            enc_start_date = base64.b64encode(enc_start_date)

            enc_end_date = list(string_to_numeric_ordinal(str(end_date)))
            enc_end_date = ts.ckks_vector(context, enc_end_date)
            enc_end_date = enc_end_date.serialize()
            enc_end_date = base64.b64encode(enc_end_date)


            
            insurance_data = InsuranceData(
                user=request.user,
                name_convention=name_convention,
                first_name=None,
                enc_first_name=enc_first_name,
                last_name=None,
                enc_last_name=enc_last_name,
                date_of_birth = None,
                enc_date_of_birth=enc_date_of_birth,
                address = None,
                enc_address=enc_address,
                city = None,
                enc_city=enc_city,
                state = None,
                enc_state=enc_state,
                zip_code = None,
                enc_zip_code=enc_zip_code,
                phone_number = None,
                enc_phone_number=enc_phone_number,
                email = None,
                enc_email=enc_email,
                gender = None,
                enc_gender=enc_gender,
                height = None,
                enc_height = enc_height,
                weight = None,
                enc_weight = enc_weight,
                dl_no = None,
                enc_dl_no = enc_dl_no,
                license_plate = None,
                enc_license_plate = enc_license_plate,
                insurance_type = None,
                enc_insurance_type=enc_insurance_type,
                coverage_amount = None,
                enc_coverage_amount=enc_coverage_amount,
                start_date = None,
                enc_start_date=enc_start_date,
                end_date = None,
                enc_end_date=enc_end_date,
            )

            insurance_data.save()
            


            # form.save()  # Save the data if the form is valid
            messages.success(request, ("Insurance Form submission successful..."))
            return redirect('home')  # Redirect to a success page
    else:
        form = InsuranceForm(request=request)

    return render(request, 'site/insurance_register.html', {'form': form,
                                                            "date_t": datetime.today()})



def home(request):

    return render(request, "site/home.html", {})