from django.http import HttpResponse


from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        <p>Hello, world. You're at the root index.</p>
        <p>
            You can find the documentation
            <a href="https://team-suyi.postman.co/workspace/Awar-Denen~b469bc55-bbfa-421b-997c-1060f691a88d/collection/32834286-8517484d-b4ae-407f-bc68-3b27c57fa545?action=share&creator=32834286">
                here
            </a>.
        </p>
    """)