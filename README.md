# Social_Media_Text_Posts_API-fastAPI_project
A CRUD API with JWT authentication and authorization
As the name implies, this type of posts only contain text and they are the most basic form of social media content.
As users sign up, they are added to the database
As they sign in, they are given JWT token with an expiring time 30mins from the time of login. JWT contains user information for which users can update and delete only their posts and not other users
Creating, Reading, Updating and Deleting posts(CRUD) needs authentication from the user before these operations can be done. 
You need to be authenticated to Create and Read but you need to be authorised as the owner of the post to update and delete a post.
Users can also vote on other users posts, because access is given for users to read other users post.

Database Tables

1. Posts
2. Users
3. Votes

Models

  #Post
1. id
2. title
3. published
4. created_at
5. owner_id
6. owner

  #User
1. id
2. email
3. password
4. created_at

   #Vote
1. post_id
2. user_id




  
