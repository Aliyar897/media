# from celery import shared_task
# from mainpageapp.views import dawn
# @shared_task
# def fetch_articles():
#     return dawn()  # Assuming dawn() is defined and accessible

from celery import shared_task
from mainpageapp.dawn_news import dawn
from mainpageapp.express_tribune import tribune
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import ScrapedNewsData
from .ml_model import summarize  # Assuming summarize is defined in summarizer.py


def summarize_pending_news():
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

        return {
            'message': 'Summaries generated and saved successfully.',
            'summarized_posts': summarized_posts
        }

    except Exception as e:
        return {
            'error': str(e)
        }
@shared_task
def fetch_articles():
    try:
        # Create a ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Run dawn and tribune in parallel
            futures = {
                executor.submit(dawn): 'dawn',
                executor.submit(tribune): 'tribune'
            }
            for future in as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    print(f"{name} function completed successfully")
                except Exception as e:
                    print(f"{name} function raised an exception: {e}")

        # Run the summarize function after both have completed
        summarize_pending_news()
        return "The celery task is finished!!!!"
    
    except Exception as e:
        return f"An error occurred: {e}"

@shared_task
def fetch_tribune_articles():
    return tribune()
