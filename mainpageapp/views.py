from django.shortcuts import render
from django.http import HttpResponse
from .dawn_news import dawn
from .express_tribune import tribune
from .express_urdu import express_urdu
from .ml_model import summarize
from .models import ScrapedNewsData, States
# ScrapedNewsData.objects.all().delete()
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        try:
            # Retrieve the related ScrapedNewsData object
            post = ScrapedNewsData.objects.get(id=post_id)
            
            # Get or create the States object
            state, created = States.objects.get_or_create(post=post)
            
            # Check if the user has already liked this post in the session
            session_key = request.session.session_key
            if session_key:
                if f"liked_{post_id}" in request.session:
                    return JsonResponse({'status': 'error', 'message': 'You have already liked this post'}, status=403)

                # Increment the like_count
                state.like_count += 1
                state.save()

                # Save the like status in the session
                request.session[f"liked_{post_id}"] = True
                return JsonResponse({'status': 'success', 'like_count': state.like_count})
            else:
                return JsonResponse({'status': 'error', 'message': 'Session not found'}, status=403)
        except ScrapedNewsData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


class SummarizePendingNewsAPIView(APIView):

    def get(self, request):
        try:
            # Fetch all posts where summary_status is False
            posts_to_summarize = ScrapedNewsData.objects.filter(summary_status=False)
            summarized_posts = []

            # List to store the posts and descriptions
            posts_data = [{'post': post, 'description': post.description} for post in posts_to_summarize]

            # Function to summarize and return the summary along with the post ID
            def summarize_post(post_data):
                summary = summarize(post_data['description'])
                return {
                    'id': post_data['post'].id,
                    'title': post_data['post'].title,
                    'summary': summary,
                    'post': post_data['post']  # Return the post object for later saving
                }

            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor(max_workers=4) as executor:
                future_to_post = {executor.submit(summarize_post, post_data): post_data for post_data in posts_data}
                for future in as_completed(future_to_post):
                    result = future.result()
                    summarized_posts.append({
                        'id': result['id'],
                        'title': result['title'],
                        'summary': result['summary']
                    })
                    # Update the post with the summary and set the summary_status to True
                    post = result['post']
                    post.summary = result['summary']
                    post.summary_status = True
                    post.save()

            if not summarized_posts:
                return Response({
                    'message': 'No posts were pending summarization.'
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'Summaries generated and saved successfully.',
                'summarized_posts': summarized_posts
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# from .summary import summarize
def home(request):

    return HttpResponse('Hello wolrd!')

import threading
@csrf_exempt
def get_new_post(request):
    print(' I m get_new_post ')
    # # Create threads for each function
    # thread1 = threading.Thread(target=dawn)
    # thread2 = threading.Thread(target=tribune)

    # # Start the threads
    # thread1.start()
    # print("started thread 1")
    # print("started thread 1")
    # thread2.start()
    # print("started thread 2")

    # # Wait for the threads to complete
    # thread1.join()
    # thread2.join()
    data = dawn()
    data = tribune()
    # data = express_urdu()
    print('this is the data i got from the news website')
    return HttpResponse('The news are donwloaded')


def summary_api(request):
    # url = 'http://127.0.0.1:8000/summary'
    # summary = summarize('ARTICLE')
    return HttpResponse('this is summary api')
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET"])
def get_news_api(request):
    category = request.GET.get('category', 'home')

    if category == 'home':
        news_data = ScrapedNewsData.objects.all().order_by('-date_published')
    elif category:
        news_data = ScrapedNewsData.objects.filter(category=category).order_by('-date_published')
    else:
        return JsonResponse({'error': 'Category parameter is missing'}, status=400)

    # Transform the queryset into the desired format
    news_list = []
    for news in news_data:
        news_list.append({
            'id': news.id,
            'heading': news.title,
            'description': news.description,
            'published': f"Published: {news.date_published.strftime('%B %d, %Y, %I:%M %p')}",
            'source': news.source,  # Assuming 'source' holds the logo URL
            'image': news.image,
        })

    return JsonResponse(news_list, safe=False, status=200)

@csrf_exempt
def news_list(request):
    if request.method == 'GET':
        # Handle GET request to fetch news data with category 'opinion'
        news_data = ScrapedNewsData.objects.filter(summary_status=True).order_by('-date_published')
    elif request.method == 'POST':
        # Handle POST request to fetch news data based on the 'opinion' parameter
        category = request.POST.get('opinion', 'home')
        if category == "home":
            news_data = ScrapedNewsData.objects.filter(summary_status=True).order_by('-date_published')
        elif category:
            news_data = ScrapedNewsData.objects.filter(category=category, summary_status=True).order_by('-date_published')
        else:
            news_data = ScrapedNewsData.objects.none()

    context = {'news_data': news_data}
    return render(request, 'index.html', context)
# views.py

from django.http import JsonResponse



@csrf_exempt
def get_text(request):
    category = request.GET.get('category')  # Get category from query parameters
    print('category', category)
    data = ScrapedNewsData.objects.all()

    if category:
        data = data.filter(category=category)

    # Order data by date_published in descending order
    data = data.order_by('-date_published')
    
    data = data.values('title', 'summary', 'image', 'date_published', 'link', 'category', 'source')

    data_list = list(data)
    
    return JsonResponse({'data': data_list})


def test_req(request):
    print('I am a test method!')

    return HttpResponse("I am just a test")
# def get_text(request):
#     # Retrieve all fields from the ScrapedNewsData model
#     data = ScrapedNewsData.objects.all().values(
#         'title', 'description', 'image', 'date_published', 'link', 'category'
#     )
    
#     # Convert the QuerySet to a list to make it JSON serializable
#     data_list = list(data)
    
#     # Return all fields as a JSON response
#     return JsonResponse({'data': data_list})