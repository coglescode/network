
document.addEventListener('DOMContentLoaded', function() {
  

  editPost();
  likePosts();
  followUser();

});


function followUser(){

  document.querySelectorAll(".follow").forEach(a => {
    
    a.onclick = function()  {
      
      const x = this.dataset;
      console.log(x);

      const user = x.id;
      //console.log(user);

      const action = x.action;
      //console.log(action);

      fetch (`/followuser`, {
        method: 'POST',
        body: JSON.stringify({
          user: user,
          action: action        
        })
      })
      .then(response => response.json())
      .then(result => {
        // Print result
        //console.log(result); 
        
        if (result.status == "ok"){
          const previous_action = action;
         
          document.querySelector(".follow").innerHTML = previous_action == "follow"? "<h3>Unfollow</h3>" : "<h3>Follow</h3>";
          
          const followers_count = document.querySelector(".followers .total");        

          const previous_followers = parseInt(followers_count.textContent);
    
          followers_count.textContent = previous_action == "follow" ? previous_followers + 1 : previous_followers - 1;
          
          saveFollowersCount(followers_count.textContent, user);

          this.dataset.action = previous_action == "follow" ? "unfollow": "follow";
        }        
      })    
      .catch(error => {
        console.log('Error:', error);
      });   

     

    };    
  })
}


function saveFollowersCount(count, user){

  follower_count = parseInt(count);
  console.log(follower_count);

  fetch (`/savecounter?user=${user}`, {
    method: 'POST',
    body: JSON.stringify({
      follower_count: follower_count,
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result); 
  })    
  .catch(error => {
    console.log('Error:', error);
  });      

  

}

function editPost(){
  document.querySelectorAll(".edit").forEach(a => {

    a.onclick = function() {

      const data = this.dataset;
      //console.log(data);

      const post_id = data.postid;
      //console.log(post_id);

      const action = data.action 
      //console.log(action);   

      const maincontent = document.querySelector(`#content_${post_id}`);
      maincontent.style.display = "none";

      const textarea = document.querySelector(`textarea#post_${post_id}`);
      textarea.style.display = "block";

      const previous_action = action;
      this.innerHTML = previous_action == "edit"? "<h4>Save</h4>" : "<h4>Edit Post</h4>";
      
      textarea.value = maincontent.textContent;

      textarea.style.display = "block";

      this.dataset.action = "save";
      const save = this.id = "save";
      this.className = "save";
       
      saveEditedpost(post_id, action);
    }  
  })
}

  
function saveEditedpost(id, action){

  const previous_action = action;
  document.querySelectorAll(".save").forEach(a =>{
    
    a.onclick = function() {

      const maincontent = document.querySelector(`#content_${id}`);    

      const textarea = document.querySelector(`textarea#post_${id}`);
    
      textarea.style.display = "none";

      maincontent.innerHTML = textarea.value; 
          
      maincontent.style.display = "block";    
      
      if ( previous_action == "edit") {        
        this.dataset.action = "edit";
      }
      
      this.id = "edit";
      this.className = "edit";
      this.innerHTML = action == "save"? "<h4>Save</h4>" : "<h4>Edit Post</h4>";
      
      editPost();

      fetch (`/editpost?id=${id} `, {
        method: 'POST',
        body: JSON.stringify({ 
          post: textarea.value 
        })      
      })
      .then(response => response.json())
      .then(res => {
  
        console.log(res)           
  
      }) 
      .catch(error => {
        console.log("error", error);
      });  
    }    
  })      
}



function likePosts(){

  document.querySelectorAll(".like").forEach(a => {
    
    a.onclick = function()  {
      
      const x = this.dataset;
      console.log(x);

      const post_id = x.id;
      console.log(post_id);

      const action = x.action;
    
      const previous_action = action;
      
      const icon_star = document.querySelector(`#icon_${post_id}`);

      icon_star.className = previous_action == "like"? "bi bi-star-fill": "bi bi-star";
      
      this.dataset.action = previous_action == "like" ? "unlike": "like";

      const likes_count = document.querySelector(`.total_${post_id}`);        

      const previous_likes = parseInt(likes_count.textContent);
     
      likes_count.textContent = previous_action == "like" ? previous_likes + 1 : previous_likes - 1;

      saveLikedposts(post_id, action);   
      
      
    };    
  })
}



function saveLikedposts(post_id, action){

  fetch (`/likepost`, {
    method: 'POST',
    body: JSON.stringify({
      post_id: post_id,
      action: action        
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    //console.log(result);     
    
  })    
  .catch(error => {
    console.log('Error:', error);
  });
}
