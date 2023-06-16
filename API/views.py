import json
from django.http import JsonResponse
from rest_framework import viewsets
from .models import User,Admin,Post,Problems,Results
from .serializers import UserSerializer, AdminSerializer, PostSerializer,ProblemsSerializer,ResultsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from bson import ObjectId
import subprocess
import traceback


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_queryset(self):
       return self.queryset.order_by('-date_added').values()

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problems.objects.all()
    serializer_class = ProblemsSerializer
    def get_queryset(self):
       return self.queryset.order_by('-Prob_level').values()

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    def get_queryset(self):
       return self.queryset.order_by('-Prob_level').values()

@csrf_exempt
def get_unsolved_problems(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        
        try:
            
            problems = Problems.objects.all()
            user_results = Results.objects.filter(user_id=user_id)
            solved_problem_ids = user_results.values_list('prob_id', flat=True)


            unsolved_problems = []
            for problem in problems:
                if problem.id not in solved_problem_ids:
                    unsolved_problems.append({
                        'id': problem.id,
                        'Prob_img': problem.Prob_img,
                        'Prob_name': problem.Prob_name,
                        'solvedby': problem.solvedby,
                        'Prob_description': problem.Prob_description,
                        'Prob_isactive': problem.Prob_isactive,
                        'output': problem.output,
                        'solution': problem.solution,
                        'Prob_level': problem.Prob_level
                    })

            
            
            return JsonResponse(list(unsolved_problems), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

def getproblemdetails(request):
    if request.method == 'GET':
        name = request.GET.get('id')
        problem = Problems.objects.filter(Prob_name=name).first()
        if problem and problem.Prob_isactive=='True':
            # Retrieve all the information for the user
            problem_details = {
                'id':problem.id,
                'name':problem.Prob_name,
                'Prob_description':problem.Prob_description,
                'output':problem.output,
                'solution':problem.solution,
                # Add other fields as needed
            }
            return JsonResponse({'user_details': problem_details})
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt      
def addFriend(request):
    if request.method == 'POST':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)
            
        # Extracting the values of the fields from the JSON object
        friendid = str(json_data.get('friendId'))
        user_id = json_data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            friends_list = user.friends_list
            if friendid not in friends_list:
                friends_list += ',' + friendid
                user.friends_list = friends_list
                user.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'already_exists'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'user_not_found'})


@csrf_exempt
def run_python(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')

        try:
            output = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT)
            output = output.decode('utf-8').strip()
            return JsonResponse({'output': output})
        except subprocess.CalledProcessError as e:
            error = e.output.decode('utf-8').strip()
            return JsonResponse({'error': error}, status=500)
        except Exception:
            error = traceback.format_exc()
            return JsonResponse({'error': error}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_posts_by_user(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        posts = Post.objects.filter(user_id=user_id)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

@csrf_exempt
def submitresult(request):
    if request.method == 'POST':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)

        user_id = json_data.get('user_id')
        prob_id = json_data.get('prob_id')
        result = json_data.get('result')

        # Save the data in the Results table
        Results.objects.create(user_id=user_id, prob_id=prob_id, result=result)

        # Return a JSON response indicating the success status
        return JsonResponse({'status': 'Data saved successfully'})

    # Return a JSON response with an error message if the request method is not POST
    return JsonResponse({'status': 'Invalid request method'})

@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)

        # Extracting the values of the fields from the JSON object
        name = json_data.get('name')
        age = json_data.get('age')
        email = json_data.get('email')
        contact = json_data.get('contact')
        password = json_data.get('password')
        country = json_data.get('country')
        date_of_joining = json_data.get('date_of_joining')
        description = json_data.get('description')
        profile_picture = json_data.get('profile_picture')
        cover_photo = json_data.get('cover_photo')

        User.insert_user(name=name, age=age, email=email, contact=contact, password=password,
                         country=country, description=description, profile_picture=profile_picture,
                         cover_photo=cover_photo)

        # return redirect('http://localhost:3000/signup')
        return JsonResponse({'status': 'success'})


@csrf_exempt
def login_check(request):
    if request.method == 'POST':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)

        # Extracting the values of the fields from the JSON object
        email = json_data.get('email')
        password = json_data.get('password')

        # Checking if the email and password match any entry in the database
        user = User.objects.filter(email=email, password=password).first()
        if user:
            response_data = {
                'status': 'success',
                'name': user.name,
                'email': user.email,
                'id': user.id,
                'profile_picture':user.profile_picture,

            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'status': 'fail'})


@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)

        # Extracting the values of the fields from the JSON object
        email = json_data.get('email')
        password = json_data.get('password')

        # Checking if the email and password match any entry in the database
        admin = Admin.objects.filter(email=email, password=password).first()
        if admin:
            response_data = {
                'status': 'success',
                'email': admin.email,
                'id': admin.id
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'status': 'fail'})


def listview(request):
    output = [{"employee": user.name, "department": user.email}
              for user in User.objects.all()]

    users = User.objects.values('id', 'name', 'email')

    return JsonResponse({'users': list(users)})


def getuserdetails(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Retrieve all the information for the user
            user_details = {
                'email': user.email,
                'name': user.name,
                'id': user.id,
                'contact': user.contact,
                'age': user.age,
                'date_of_joining': user.date_of_joining,
                'country': user.country,
                'password': user.password,
                'profile_picture': user.profile_picture,
                'cover_photo': user.cover_photo,
                'description': user.description
                # Add other fields as neede
            }
            return JsonResponse({'user_details': user_details})
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        # Assuming that the request body contains a JSON object
        json_data = json.loads(request.body)

        # Extracting the values of the fields from the JSON object
        email = json_data.get('email')

        # Checking if the user exists
        user = User.objects.filter(email=email).first()
        if user:
            # Updating the user fields if the user exists
            user.name = json_data.get('name', user.name)
            user.age = json_data.get('age', user.age)
            user.contact = json_data.get('contact', user.contact)
            user.password = json_data.get('password', user.password)
            user.country = json_data.get('country', user.country)

            # Saving the updated user
            user.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def getallusers(request):
    output = [{"employee": user.name, "department": user.email}
              for user in User.objects.all()]

    users = User.objects.values('id', 'name', 'age', 'email', 'contact', 'user_type', 'password', 'country',
                                'date_of_joining', 'description', 'profile_picture',
                                'requests_sent_to_groups', 'pending_requests_to_groups',
                                'approved_requests')

    return JsonResponse({'users': list(users)})


