#!/usr/bin/env python3
"""
Quick demonstration of Flask-SQLAlchemy application functionality.
Run this after starting the application with: python app.py
"""
import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:5000/api/v1"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def create_user():
    """Create a new user."""
    print_section("Creating User")
    
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepass123",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        user = response.json()['user']
        print("✅ User created successfully!")
        pprint(user)
        return user['id']
    else:
        print("❌ Failed to create user")
        pprint(response.json())
        return None

def get_users():
    """Get all users with pagination."""
    print_section("Getting Users (Page 1)")
    
    response = requests.get(f"{BASE_URL}/users?page=1&page_size=10")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} users")
        print(f"Showing page {data['pagination']['page']} of {data['pagination']['pages']}")
        for user in data['users']:
            print(f"  - {user['username']} ({user['email']})")
    else:
        print("❌ Failed to get users")
        pprint(response.json())

def create_post(author_id):
    """Create a new post."""
    print_section("Creating Post")
    
    post_data = {
        "title": "My First Flask Post",
        "content": "This is an example post created through the Flask-SQLAlchemy API. "
                   "It demonstrates the full CRUD functionality with proper validation "
                   "and error handling.",
        "author_id": author_id,
        "published": False
    }
    
    response = requests.post(f"{BASE_URL}/posts", json=post_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        post = response.json()['post']
        print("✅ Post created successfully!")
        pprint(post)
        return post['id']
    else:
        print("❌ Failed to create post")
        pprint(response.json())
        return None

def publish_post(post_id):
    """Publish a post."""
    print_section(f"Publishing Post {post_id}")
    
    response = requests.post(f"{BASE_URL}/posts/{post_id}/publish")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        post = response.json()['post']
        print(f"✅ Post published! Status: {post['published']}")
    else:
        print("❌ Failed to publish post")
        pprint(response.json())

def get_posts(published=None, search=None):
    """Get posts with optional filters."""
    filters = []
    if published is not None:
        filters.append(f"published={str(published).lower()}")
    if search:
        filters.append(f"search={search}")
    
    query_string = "&".join(filters) if filters else ""
    title = "Getting All Posts" if not filters else f"Getting Posts ({', '.join(filters)})"
    
    print_section(title)
    
    response = requests.get(f"{BASE_URL}/posts?{query_string}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} posts")
        for post in data['posts']:
            status = "📢 Published" if post['published'] else "📝 Draft"
            print(f"  {status} - {post['title']}")
    else:
        print("❌ Failed to get posts")
        pprint(response.json())

def get_post_with_author(post_id):
    """Get a specific post with author details."""
    print_section(f"Getting Post {post_id} with Author")
    
    response = requests.get(f"{BASE_URL}/posts/{post_id}?include_author=true")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        post = response.json()['post']
        print("✅ Post retrieved with author details!")
        print(f"Title: {post['title']}")
        print(f"Author: {post['author']['username']} ({post['author']['email']})")
        print(f"Published: {post['published']}")
        print(f"Content: {post['content'][:100]}...")
    else:
        print("❌ Failed to get post")
        pprint(response.json())

def update_user(user_id):
    """Update user information."""
    print_section(f"Updating User {user_id}")
    
    update_data = {
        "first_name": "Johnny",
        "last_name": "Doe-Smith"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        user = response.json()['user']
        print("✅ User updated successfully!")
        print(f"New name: {user['first_name']} {user['last_name']}")
    else:
        print("❌ Failed to update user")
        pprint(response.json())

def search_posts(search_term):
    """Search posts by content."""
    print_section(f"Searching Posts for '{search_term}'")
    
    response = requests.get(f"{BASE_URL}/posts?search={search_term}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} matching posts")
        for post in data['posts']:
            print(f"  - {post['title']}")
    else:
        print("❌ Search failed")
        pprint(response.json())

def main():
    """Run the demonstration."""
    print("\n" + "="*60)
    print("  Flask-SQLAlchemy Application Demo")
    print("  Make sure the application is running at localhost:5000")
    print("="*60)
    
    try:
        # Create a user
        user_id = create_user()
        if not user_id:
            print("\n⚠️  Demo stopped: Could not create user")
            return
        
        # Get all users
        get_users()
        
        # Create a post
        post_id = create_post(user_id)
        if not post_id:
            print("\n⚠️  Demo stopped: Could not create post")
            return
        
        # Get posts (drafts)
        get_posts(published=False)
        
        # Publish the post
        publish_post(post_id)
        
        # Get published posts
        get_posts(published=True)
        
        # Get post with author details
        get_post_with_author(post_id)
        
        # Update user
        update_user(user_id)
        
        # Search posts
        search_posts("Flask")
        
        print_section("Demo Complete!")
        print("✅ All operations completed successfully!")
        print(f"\nCreated:")
        print(f"  - User ID: {user_id}")
        print(f"  - Post ID: {post_id}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the application.")
        print("Please make sure the Flask application is running:")
        print("  python app.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
