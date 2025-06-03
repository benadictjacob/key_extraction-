from django.shortcuts import render,HttpResponse
import json
import pyrebase
from .temp import  loadimg 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import traceback
import os
from .convert import convert_to_key  # Import the function from convert.py
from .test6 import  calculate_similarity
from django.http import JsonResponse
from .firebase_config import db
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from cypher_functions import connect 
from cypher_functions.encription import token_to_data 

import ast


#here we add dictionary that stroes the data about  a database
config={
     "apiKey": "AIzaSyBDbta51BTIhCXEq5xwWQA9l7HoobEsB1g",
  "authDomain": "newproject-2b8c0.firebaseapp.com",
  "databaseURL": "https://newproject-2b8c0-default-rtdb.firebaseio.com",
  "projectId": "newproject-2b8c0",
  "storageBucket": "newproject-2b8c0.firebasestorage.app",
  "messagingSenderId": "201430695093",
  "appId": "1:201430695093:web:3206452e4bbf2fa49292fc",
  "measurementId": "G-83GCZQE8G3"
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
print(database)
# def elec_(request):
#     from django.shortcuts import render
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@login_required
@csrf_protect
def check_in(request):
    request.session['entry_point'] = 'RFID'
    return redirect('finger')
def checked(request):
    return render(request, "checked.html")   
    
    
def see(request)   :
    user=request.user
    username = user.username
    return render(request, "farm_data2.html", {"username": username})
def owner_dash(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        farm_id = data.get('farm_id')
        
        if not farm_id or not isinstance(farm_id, str):
            return JsonResponse({'error': 'Invalid farm_id'}, status=400)
        
        farms_ref = database
        all_farms = farms_ref.child('farms').get().val()
        
        # Case 1: No farms exist at all
        if not all_farms:
            farms_ref.child("farm").child(farm_id).set({
                'created_at': {'.sv': 'timestamp'},
                'status': 'active'
            })
            return JsonResponse({
                'created': True,
                'message': f'First farm {farm_id} created'
            })
        
        # Case 2: Check if farm_id exists among existing farms
        if farm_id in all_farms:
            return JsonResponse({
                'exists': True,
                'message': f'id  already exists',
                'farm_data': all_farms[farm_id]
            })
        user = request.user
        # Case 3: Farms exist but this ID is new
        farms_ref.child('farms').child(farm_id).set({
            'created_at': {'.sv': 'timestamp'},
            'status': 'active',
            'owner': user.username,
            'owner_id': str(user.id),
        })
        #here we have to add the current user finger key and farmid 
        # Get current user details
        
        user_ref = db.collection('users').document(str(user.id))
        existing_data = user_ref.get()
    #    existing_data = user_ref.get()

        matched_key = None
        if existing_data.exists:
            user_data = existing_data.to_dict()
            fingerprint_key_name = f'fingerprint_{1}_key'

            if fingerprint_key_name in user_data:
                        matched_key = user_data[fingerprint_key_name]
                        connect.start_server(matched_key,farm_id)
        
        return JsonResponse({
            'created': True,
            'message': f'New farm {farm_id} added'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@login_required(login_url='/members')
def owner(request):
    request.session['role']=0
    permission=0
    user=request.user
    user_ref = db.collection('users').document(str(user.id))
    doc = user_ref.get(field_paths=['role'])
    if doc.exists:
          permission=  doc.to_dict().get('role')
    if permission =="owner":
        username = user.username
     
        return render(request, "farm_data.html", {"username": username})
    else:
        return redirect('see')
    # data = request.data
    # print("Received data:", data)  # Debug
    # return Response({"status": "success"})
   
    
def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the login page or any other page
    return redirect("/members")  # Adjust the URL as needed
@login_required(login_url='/members')
def home(request):
    
    return render(request,"black.html")
    
def auth_pass(request):
    request.session['entry_point'] = 'auth'
    return render(request,"info2.html")
    

# Create your views here.
def check_pass(request):
    user=request.user
    user_ref = db.collection('users').document(str(user.id))
    existing_data = user_ref.get()
    request.session['entry_point'] = 'register'

    if existing_data.exists:
        existing_user_data = existing_data.to_dict()
        

        # Get all fingerprint-related keys
        # fingerprint_keys = [key for key in existing_user_data if key.startswith("fingerprint_") and key.endswith("_key")]
        # registration_complete=0
        # if len(fingerprint_keys) ==4:
            # User exists AND has fingerprint data
        registration_complete = 1
        return render(request, "black.html", {"registration_complete": registration_complete})
    # else:
    #         # User exists BUT has no fingerprint data
    #         # print("User exists, but no fingerprints found.")
    #         return render(request, "info2.html", {"message": "User exists, but no fingerprint data found."})

    else:
        # User does not exist
        cond = True  # Placeholder till fingerprint scanner is connected
        if cond:
            print("Fingerprint is fetched")
            img = loadimg()
            # cv2.imshow("image", img)

        return render(request, "info2.html", {"message": "New user. Please register."})

    #to check if the port is connected or not 
    
    
def finger(request):
    if request.session.get('entry_point') == 'auth':
        # User is coming from the auth_pass view
        # You can add any specific logic here if needed
       
            
        print("User is coming from auth_pass view")
        # connect.start_server()
        return render(request, "fingerprint.html")
    if request.session.get('entry_point') == 'RFID':
        # User is coming from the auth_pass view
        # You can add any specific logic here if needed
       
            
        print("User is coming from RFID")
        # connect.start_server()
        return render(request, "fingerprint.html")
    if request.method == 'GET':
        # data = json.loads(request.body)  # Parse JSON
            role = request.GET.get('role') 
            request.session['role'] =str(role)    
            print(request.session.get('role'))
        # owner  = request.GET.get('owner')
    return render(request,"fingerprint.html",{"role":role}) 
    
    
def dash(request):
    permission=0
    user=request.user
    user_ref = db.collection('users').document(str(user.id))
    doc = user_ref.get(field_paths=['role'])
    if doc.exists:
        permission=  doc.to_dict().get('role')
        
        # print(permission)
        # print(key1)
    if request.method == 'GET':
        # data = json.loads(request.body)  # Parse JSON
        farm_id = request.GET.get('farmid')
        # owner  = request.GET.get('owner')
        
        print(farm_id)
        # print(owner)
        farms_ref = database
        all_farms = farms_ref.child('farms').get().val()
        #here we need to check if the farm id is valid or not
        # Case 1: No farms exist at all
        if not all_farms:
            
            return redirect('owner')
        base_path = f"farms/{farm_id}"
        owner_id=database.child(f"{base_path}/owner_id").get().val()
        
        # Case 2: Check if farm_id exists among existing farms
        if farm_id in all_farms:
            sensor_readings = database.child(f"{base_path}/sensor_readings").get().val()
             # List to store all decrypted readings
            # if not sensor_readings:
            #     return redirect('owner')
            
        # owner_id=database.child(f"{base_path}/owner_id").get().val()
            if permission == "owner" or user.id == owner_id :
                user_ref = db.collection('users').document(str(owner_id))
                temp = user_ref.get(field_paths=['fingerprint_1_key'])
                key1=temp.to_dict().get('fingerprint_1_key')
                
                # print(key1)
                current_count = 0
                user_permissions=[]
                decrypted_readings = [] 
                permissions = database.child(f"{base_path}/permissions").get().val()
                
# Check if permissions is None (path doesn't exist)
                if permissions is None:
                    return HttpResponse("No permissions found for this farm.")

                # Check if permissions is empty (empty dict {})
                if not permissions:
                    return HttpResponse("Permissions exist but are empty.")

                # Ensure permissions is a dictionary before calling .items()
                if not isinstance(permissions, dict):
                    return HttpResponse("Permissions data is not in the expected format.")

                # Process permissions
                user_permissions = []
                for key, value in permissions.items():
                    try:
                        print(f"Processing user {key} with permission {value}")
                        
                        # Skip if permission value is empty/None
                        if not value:
                            print(f"Warning: Empty permission for user {key}")
                            continue
                            
                        user_permission = {
                            'user_id': key,
                            'permission': value
                        }
                        user_permissions.append(user_permission)
                        
                    except Exception as e:
                        print(f"Error processing user {key}: {str(e)}")
                        continue  # Skip to next user if error occurs

                while True:
                    # Get reading from Firebase
                    x = database.child(f"{base_path}/sensor_readings/readings/{current_count}").get().val()
                    
                    
                    
                    
                
                    # Exit loop if no more data
                    if x is None:
                        break
                    
                    # Convert to dictionary format
                    sensor_data = {
                        "temperature": x['temperature'],
                        "humidity": x['humidity'],
                        "RainStatus": x['RainStatus'],
                        "SoilMoisture": x['SoilMoisture'],
                        "timestamp": x['timestamp']
                    }
                    
                    # Print encrypted values
                    print("Encrypted Values:")
                    print("Temp:", sensor_data['temperature'])
                    print("Humidity:", sensor_data['humidity'])
                    print("Rain:", sensor_data['RainStatus'])
                    print("Soil:", sensor_data['SoilMoisture'])
                    
                    try:
                        # Decrypt each value
                        decrypted_reading = {
                            "temperature": token_to_data(sensor_data['temperature'], key1),
                            "humidity": token_to_data(sensor_data['humidity'], key1),
                            "RainStatus": token_to_data(sensor_data['RainStatus'], key1),
                            "SoilMoisture": token_to_data(sensor_data['SoilMoisture'], key1),
                            "timestamp": sensor_data['timestamp']  # No decryption needed
                        }
                        
                        # Store decrypted reading
                        decrypted_readings.append(decrypted_reading)
                        
                        # Print decrypted values
                        print("\nDecrypted Values:")
                        print("Temp:", decrypted_reading['temperature'])
                        print("Humidity:", decrypted_reading['humidity'])
                        print("Rain:", decrypted_reading['RainStatus'])
                        print("Soil:", decrypted_reading['SoilMoisture'])
                        print("Time:", decrypted_reading['timestamp'])
                        print("-" * 50)
                        
                    except Exception as e:
                        print(f"Failed to decrypt reading {current_count}: {str(e)}")
                    
                    current_count += 1  # Move to next reading

                print(f"\nTotal readings decrypted: {len(decrypted_readings)}")
                
                # here i have to call the values in the farm id 
                return render(request, "dashboard.html", {
                "user": user,
                "decrypted_readings": decrypted_readings,
                "readings_count": len(decrypted_readings),
                'user_permissions':user_permissions,
            })
            #i need to check if there is child node called permissions in the farm_id if ther is not i need to make on and if ther is one i need to add aome thing
            else :
                if'permissions' not in all_farms[farm_id]:
                    #made the user id request for accesss & ans create  a permission child node
                   farms_ref.child('farms').child(farm_id).child('permissions').child(str(user.id)).set("false")
                   return HttpResponse("Your  request  to access this farm have been placed. but you have not been granted access yet.")
                   
                elif str(user.id) not in all_farms[farm_id]['permissions']:
                    #made the user id request for accesss & and permission child already existed
                    farms_ref.child('farms').child(farm_id).child('permissions').child(str(user.id)).set("false")
                    return HttpResponse("Your request to  access  this farm have been placed . but you have not been granted access yet.")
                elif str(user.id) in all_farms[farm_id]['permissions']:
                    permission = all_farms[farm_id]['permissions'][str(user.id)]
                    if permission == "false":
                        # farms_ref.child('farms').child(farm_id).child('permissions').child(str(user.id)).set("flase")
                        farms_ref.child('farms').child(farm_id).child('permissions').child(str(user.id)).set("false")
                        return HttpResponse("Your request to  access  this farm have been placed . but you have not been granted access yet.")
                    elif permission == "true":
                        user_ref = db.collection('users').document(str(owner_id))
                        temp = user_ref.get(field_paths=['fingerprint_1_key'])
                        key1=temp.to_dict().get('fingerprint_1_key')
                        current_count = 0
                        user_permissions=[]
                        decrypted_readings = [] 
                        permissions = database.child(f"{base_path}/permissions").get().val()
                        # for key, value in permissions.items():
                        #     # user_ref = db.collection('users').document(str(key))
                        #     # username = user_ref.get(field_paths=['username'])
                        #     # name=username.to_dict().get('username')
                        #     # print(name)
                        #     print(key)
                        #     print(value)
                        #     user_permission ={
                        #         'user_id': key,
                        #         # 'username': name,
                        #         'permission': value
                        #     }
                        #     user_permissions.append(user_permission)
                        while True:
                            # Get reading from Firebase
                            x = database.child(f"{base_path}/sensor_readings/readings/{current_count}").get().val()
                            
                            
                            
                            
                        
                            # Exit loop if no more data
                            if x is None:
                                break
                            
                            # Convert to dictionary format
                            sensor_data = {
                                "temperature": x['temperature'],
                                "humidity": x['humidity'],
                                "RainStatus": x['RainStatus'],
                                "SoilMoisture": x['SoilMoisture'],
                                "timestamp": x['timestamp']
                            }
                            
                            # Print encrypted values
                            print("Encrypted Values:")
                            print("Temp:", sensor_data['temperature'])
                            print("Humidity:", sensor_data['humidity'])
                            print("Rain:", sensor_data['RainStatus'])
                            print("Soil:", sensor_data['SoilMoisture'])
                            
                            try:
                                # Decrypt each value
                                decrypted_reading = {
                                    "temperature": token_to_data(sensor_data['temperature'], key1),
                                    "humidity": token_to_data(sensor_data['humidity'], key1),
                                    "RainStatus": token_to_data(sensor_data['RainStatus'], key1),
                                    "SoilMoisture": token_to_data(sensor_data['SoilMoisture'], key1),
                                    "timestamp": sensor_data['timestamp']  # No decryption needed
                                }
                                
                                # Store decrypted reading
                                decrypted_readings.append(decrypted_reading)
                                
                                # Print decrypted values
                                print("\nDecrypted Values:")
                                print("Temp:", decrypted_reading['temperature'])
                                print("Humidity:", decrypted_reading['humidity'])
                                print("Rain:", decrypted_reading['RainStatus'])
                                print("Soil:", decrypted_reading['SoilMoisture'])
                                print("Time:", decrypted_reading['timestamp'])
                                print("-" * 50)
                                
                            except Exception as e:
                                print(f"Failed to decrypt reading {current_count}: {str(e)}")
                            
                            current_count += 1  # Move to next reading

                        print(f"\nTotal readings decrypted: {len(decrypted_readings)}")
                        
                        # here i have to call the values in the farm id 
                        return render(request, "dashboard1.html", {
                        "user": user,
                        "decrypted_readings": decrypted_readings,
                        "readings_count": len(decrypted_readings),
                        "role":'viewer'
                        # 'user_permissions':user_permissions,
                    })
                
                    
                    
                
            
            
            
            #here we have to do the rest of the implementation

        # user = request.user
        # Case 3: Farms exist but this ID is new
        return redirect('owner')
        

def mem(request):
    return 
    
def display(request):
    
    con =True
    if con :
              values = database.child('users').child('19').child('sensor_data').child('read1')
            #   all_reads = ref.get()

            #   if not all_reads:
            #     print("No data found.")
            #     return []

            #   all_data = []
            #   for read_name, values in all_reads.items():
              entry = {
                    # "read": read_name,
                    "RainStatus": values.child('RainStatus').get().val(),
                    "Soilmoisture": values.child('Soilmoisture').get().val(),
                    "humidity": values.child('humidity').get().val(),
                    "temperature": values.child('temperature').get().val()
                }
            #   all_data.append(entry)
              
              channel_name =database.child('users').child('19').child('username').get().val()
              channel_email =database.child('users').child('19').child('email').get().val()
            #   sensor =database.child('users').child('19').child('').get().val()
            
    
   
              return render(request,"firebase.html",{"channel_name":channel_name,
                                       "channel_type":channel_email,
                                       "channel_sub":12,
                                       "entry" :entry,})
                                       
                                    #    })
    
        
    
    

@login_required
@csrf_protect
def upload_fingerprint(request):
    if request.session.get('entry_point') == 'auth':
        auth_success=0
        print("User is coming from auth_pass view")
        # finger(request)
        if 'auth_success' not in request.session:
            request.session['auth_success'] = 0    #the same templates and view function are used to by maniulaion function calls to reduce the url made to reduce complications
        if request.session['auth_success'] >=4:
            request.session['auth_success'] = 0
        if request.method == 'POST':
            try:
                # Check if file was uploaded
                if 'fingerprint' not in request.FILES:
                    return JsonResponse({
                        'success': False,
                        'error': 'No file uploaded'
                    })

                fingerprint_file = request.FILES['fingerprint']

                # Validate file type
                if not fingerprint_file.name.lower().endswith('.bmp'):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please upload a BMP file'
                    })

                # Get the finger number from the request
                finger_number = request.POST.get('finger_number', 1)

                # Save the file temporarily
                uploads_dir = 'c:/Users/VICTUS/projectAB/uploads'
                os.makedirs(uploads_dir, exist_ok=True)
                temp_path = os.path.join(uploads_dir, f'fingerprint_{finger_number}.bmp')
                with open(temp_path, 'wb') as f:
                    f.write(fingerprint_file.read())

                # Convert fingerprint to key
                key = convert_to_key(temp_path)

                # Get current user details
                user = request.user
                user_ref = db.collection('users').document(str(user.id))
                existing_data = user_ref.get()

                matched_key = None
                if existing_data.exists:
                    user_data = existing_data.to_dict()
                    fingerprint_key_name = f'fingerprint_{finger_number}_key'

                    if fingerprint_key_name in user_data:
                        matched_key = user_data[fingerprint_key_name]
                        keys1 =matched_key
                        keys2  =key
                        similarity_percentage = calculate_similarity(keys1, keys2)
                        print(f"Similarity percentage: {similarity_percentage:.2f}%")

                            # Check if the similarity percentage is greater than or equal to 90%
                        if similarity_percentage >= 90:
                                request.session['auth_success'] += 1
                                request.session.modified = True
                                auth=request.session.get('auth_success')
                                print(auth)
                                return JsonResponse({
                                'success': True,
                                'message': f'Fingerprint {finger_number} matched successfully',
                                "auth_success":auth ,   
                                })
                                
                        else:
                                print("The fingerprints are not similar.")
                                print(auth_success)
                        
                        # request.session['auth_success'] =0
                        
                        
                    else:
                        return JsonResponse({
                            'success': False,
                            'error': f'Fingerprint key for finger {finger_number} not found in database'
                        })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'User data not found in Firestore'
                    })

                # Clean up temporary files and directories
                for filename in os.listdir(uploads_dir):
                    os.remove(os.path.join(uploads_dir, filename))
                os.rmdir(uploads_dir)

                return JsonResponse({
                    'success': True,
                    'message': f'Fingerprint {finger_number} processed locally',
                    'finger_key_local': key,
                    'finger_key_firebase': matched_key
                })
               

            except Exception as e:
                print(f"Error processing fingerprint: {str(e)}")
                print(traceback.format_exc())
                return JsonResponse({
                    'success': False,
                    'error': 'Error processing fingerprint file'
                })

        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })    
    elif request.session.get('entry_point') == 'register':
        if request.method == 'POST':
            
            try:
                # Check if file was uploaded
                if 'fingerprint' not in request.FILES:
                    return JsonResponse({
                        'success': False,
                        'error': 'No file uploaded'
                    })

                fingerprint_file = request.FILES['fingerprint']
                
                # Validate file type
                if not fingerprint_file.name.lower().endswith('.bmp'):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please upload a BMP file'
                    })

                # Get the finger number from the request
                finger_number = request.POST.get('finger_number', 1)
                role = request.session.get('role')
                # Save the file temporarily
                uploads_dir = 'c:/Users/VICTUS/projectAB/uploads'
                os.makedirs(uploads_dir, exist_ok=True)
                temp_path = os.path.join(uploads_dir, f'fingerprint_{finger_number}.bmp')
                with open(temp_path, 'wb') as f:
                    f.write(fingerprint_file.read())
                
                # Directory to save keys
                keys_dir = 'c:/Users/VICTUS/projectAB/keys'
                os.makedirs(keys_dir, exist_ok=True)

                # Convert fingerprint to key and save to file
                key = convert_to_key(temp_path)
                key_file_path = os.path.join(keys_dir, f'fingerprint_{finger_number}.txt')
                with open(key_file_path, 'w') as key_file:
                    key_file.write(key)

                # Get current user details
                user = request.user
                
                # Check if user already has data in Firestore
                user_ref = db.collection('users').document(str(user.id))
                existing_data = user_ref.get()
                
                # Prepare base user data
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role':role,
                    'last_updated': firestore.SERVER_TIMESTAMP
                }

                if existing_data.exists:
                    # Get existing data
                    existing_user_data = existing_data.to_dict()
                    
                    # Check if this fingerprint number already exists
                    fingerprint_key = f'fingerprint_{finger_number}_key'
                    if fingerprint_key in existing_user_data:
                        return JsonResponse({
                            'success': True,
                            'error': f'Fingerprint {finger_number} already exists for this user'
                        })
                    
                    # Preserve existing fingerprint keys
                    for key_name, key_value in existing_user_data.items():
                        if key_name.startswith('fingerprint_') and key_name.endswith('_key'):
                            user_data[key_name] = key_value
                    
                    # Add the new fingerprint key
                    user_data[f'fingerprint_{finger_number}_key'] = key
                    
                    # Update the document
                    user_ref.update(user_data)
                    message = f'Fingerprint {finger_number} added successfully to existing user data'
                else:
                    # For new users, add the current fingerprint key
                    user_data[f'fingerprint_{finger_number}_key'] = key
                    
                    # Create new document
                    user_ref.set(user_data)
                    message = 'New user data and fingerprint key saved successfully'
                
                # Clean up temporary files and directories
                for filename in os.listdir(uploads_dir):
                    os.remove(os.path.join(uploads_dir, filename))
                os.rmdir(uploads_dir)
                
                for filename in os.listdir(keys_dir):
                    os.remove(os.path.join(keys_dir, filename))
                os.rmdir(keys_dir)
                # connect.start_server()  # Start the Flask server
                return JsonResponse({
                    'success': True,
                    'message': message,
                    'register':1,
                })

            except Exception as e:
                print(f"Error processing fingerprint: {str(e)}")
                print(traceback.format_exc())
                return JsonResponse({
                    'success': False,
                    'error': 'Error processing fingerprint file'
                })
        
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })
    if request.session.get('entry_point') == 'RFID':
        auth_success=0
        print("User is coming for RFID view")
        # finger(request)
        if 'auth_success' not in request.session:
            request.session['auth_success'] = 0    #the same templates and view function are used to by maniulaion function calls to reduce the url made to reduce complications
        if request.session['auth_success'] >=4:
            request.session['auth_success'] = 0
        if request.method == 'POST':
            try:
                # Check if file was uploaded
                if 'fingerprint' not in request.FILES:
                    return JsonResponse({
                        'success': False,
                        'error': 'No file uploaded'
                    })

                fingerprint_file = request.FILES['fingerprint']

                # Validate file type
                if not fingerprint_file.name.lower().endswith('.bmp'):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please upload a BMP file'
                    })

                # Get the finger number from the request
                finger_number = request.POST.get('finger_number', 1)

                # Save the file temporarily
                uploads_dir = 'c:/Users/VICTUS/projectAB/uploads'
                os.makedirs(uploads_dir, exist_ok=True)
                temp_path = os.path.join(uploads_dir, f'fingerprint_{finger_number}.bmp')
                with open(temp_path, 'wb') as f:
                    f.write(fingerprint_file.read())

                # Convert fingerprint to key
                key = convert_to_key(temp_path)

                # Get current user details
                user = request.user
                user_ref = db.collection('users').document(str(user.id))
                existing_data = user_ref.get()

                matched_key = None
                if existing_data.exists:
                    user_data = existing_data.to_dict()
                    fingerprint_key_name = f'fingerprint_{finger_number}_key'

                    if fingerprint_key_name in user_data:
                        matched_key = user_data[fingerprint_key_name]
                        keys1 =matched_key
                        keys2  =key
                        similarity_percentage = calculate_similarity(keys1, keys2)
                        print(f"Similarity percentage: {similarity_percentage:.2f}%")

                            # Check if the similarity percentage is greater than or equal to 90%
                        if similarity_percentage >= 90:
                                request.session['auth_success'] += 1
                                request.session.modified = True
                                auth=request.session.get('auth_success')
                                print(auth)
                                return JsonResponse({
                                'success': True,
                                'message': f'Fingerprint {finger_number} matched successfully',
                                "auth_success":auth ,  
                                "rfid":1 
                                })
                                
                        else:
                                print("The fingerprints are not similar.")
                                print(auth_success)
                        
                        # request.session['auth_success'] =0
                        
                        
                    else:
                        return JsonResponse({
                            'success': False,
                            'error': f'Fingerprint key for finger {finger_number} not found in database'
                        })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'User data not found in Firestore'
                    })

                # Clean up temporary files and directories
                for filename in os.listdir(uploads_dir):
                    os.remove(os.path.join(uploads_dir, filename))
                os.rmdir(uploads_dir)

                return JsonResponse({
                    'success': True,
                    'message': f'Fingerprint {finger_number} processed locally',
                    'finger_key_local': key,
                    'finger_key_firebase': matched_key
                })
               

            except Exception as e:
                print(f"Error processing fingerprint: {str(e)}")
                print(traceback.format_exc())
                return JsonResponse({
                    'success': False,
                    'error': 'Error processing fingerprint file'
                })

        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })
# def owner_auth(request):
    
def update_access(request):
    if request.method =='GET':
        # data = json.loads(request.body)  # Parse JSON
        farm_id = request.GET.get('farmid')
        user_id = request.GET.get('userid')
        action = request.GET.get('action')
        farms_ref = database
        
        if action == 'grant':
             farms_ref.child('farms').child(farm_id).child('permissions').child(str(user_id)).set("true")
             return JsonResponse({'success': True})
        elif action == 'revoke':
                farms_ref.child('farms').child(farm_id).child('permissions').child(str(user_id)).set("false")
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
            
        # Case 1: No farms exist at all
        # if not all_farms:
        #     return redirect('owner')
        
        # # Case 2: Check if farm_id exists among existing farms
        # if farm_id in all_farms:
        #     if permission == "true":
        #         farms_ref.child('farms').child(farm_id).child('permissions').child(user_id).set("true")
        #         return HttpResponse("The user has been granted access to this farm.")
        #     elif permission == "false":
        #         farms_ref.child('farms').child(farm_id).child('permissions').child(user_id).set("false")
        #         return HttpResponse("The user has been denied access to this farm.")
        #     else:
        #         return HttpResponse("Invalid permission value. Use 'true' or 'false'.")