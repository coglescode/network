document.addEventListener('DOMContentLoaded', function() {
     

  
  document.querySelector('#allposts').style.display = 'block';
  //document.querySelector('form').style.display = 'block';

  
  document.querySelectorAll('a').forEach(a => {
    a.onclick = function() {
      
      showSection(this.dataset.section);
      
      /*
      const section = this.dataset.section;
      history.pushState({section: section}, "", `${section}`);
      */ 
    };    
  });

  
  
  const index = "allposts"
  
  //history.replaceState({section: index}, "", `/allposts`);
      
  window.onpopstate = function(event) {
        console.log(event.state.section);
        showSection(event.state.section);

  }
  
  load_posts("allposts");

});


function showSection(section) {   

  document.querySelector('#allposts').style.display = 'none';
  document.querySelector('#profile').style.display = 'none';
  document.querySelector('#following').style.display = 'none';
  
  document.querySelector(`#${section}`).style.display = 'block';

    
  load_posts(section);

  if (section !== 'allposts') {
    document.querySelector('#form_div').style.display = 'none';
  } else {
    document.querySelector('#form_div').style.display = 'block';
  }  
}


function load_posts(section) {  

  const api_section = `/getsection/${section}`;
  async function getsection() {

    const response = await fetch(api_section);    

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }


    const data =  await response.json();

    console.log(data);    


    //const posts = data.map(showposts);
   
      // Below Querying with forEach function
      
      const posts = data.forEach(posts => {
      
      const post_grid = document.createElement('div');
      const picture = document.createElement('div');  
      const user = document.createElement('a'); 
      const time = document.createElement('div');
      const body = document.createElement('div');
      const likes = document.createElement('div');
      
      post_grid.setAttribute("class", "post_grid");
      
      picture.id = "picture";
      picture.setAttribute('class', 'profile');
   
      user.id = `${posts.poster}`;
      //user.id = "user";
      user.setAttribute('class', 'user');
      user.setAttribute('data-section', 'profile');
      user.textContent = `${posts.poster}`;
      
      time.id = "time";
      time.setAttribute('class', 'timestamp');
      time.textContent = `${posts.created }`;
      
      body.id = "body";
      body.setAttribute('class', 'content');
      body.textContent = `${posts.body}`;
     
      likes.id = "likes";
      likes.className = "bi bi-star fs-4 ";
      likes.textContent = `${posts.likes}`;
      
      post_grid.append(picture, user, time, body, likes);
      document.querySelector('#allposts').appendChild(post_grid);
    
      //user.addEventListener('click', () => load_profile(posts.poster));
      user.addEventListener('click', () => {

        //load_posts('profile');
        
        document.querySelector(".container").firstChild.innerHTML = "Profile";

        /*
        const profile = "profile"
        history.replaceState({section: profile}, "", `/${posts.poster}`);
        */
      
        document.querySelector("#form_div").style.display = "none";
        document.querySelector("#allposts").style.display = "none";
        document.querySelector("#profile").style.display = "block";  

        load_profile(posts.id);       
        
      });
    });  
    
    
  }
  
  getsection();


  const newItem = document.createElement("h1");  
  const textNode =  document.createTextNode(`${section.charAt(0).toUpperCase() + section.slice(1)}`);
  newItem.appendChild(textNode);

  const container = document.querySelector(".container");
  container.replaceChild(newItem, container.childNodes[0]);
  
}



function load_profile(id) {        
    
  
  fetch(`/getuser/${id}`)
  .then(res => res.json())
  .then(data => {

     
    // Takes the user profile you clicked on out of the array
    const visitedProfile = data.splice(0, 1)
    console.log(visitedProfile);
    
    const requestUser = data.pop();
    console.log(requestUser);

    // Show the visited user following and follower count
    const currentuser = document.createElement('div');
          //currentuser.id = `${visitedProfile[0].username}`;
          currentuser.id = "uservisited";
          //user.setAttribute('class', 'user');
          currentuser.innerHTML = `${visitedProfile[0].username}`;
          document.querySelector("#profile").appendChild(currentuser);

        const following = document.createElement('div');
          following.id = "following";
          following.style.display = "block";
          following.innerHTML  =  `${visitedProfile[0].following}`;
          document.querySelector("#profile").appendChild(following);

          const followers = document.createElement('div');
          followers.id = "followers";
          //x.className = "bi bi-star fs-4 ";
          //likes.setAttribute("class", "likes");
          followers.style.display = "block";
          followers.innerHTML  =  `<i></i> ${visitedProfile[0].followers}`;
          document.querySelector("#profile").appendChild(followers);

    // Checks if the request user and the visited profile user are the same to display or not the follow button    
    if (requestUser.username !== visitedProfile[0].username) {
      document.querySelector("#btn_follow").style.display = "block";

      const visited_user = visitedProfile[0].username;
      document.querySelector("#user_followed").setAttribute("value", visited_user )
    } else {
      document.querySelector("#btn_follow").style.display = "none";     
    }

   
    // Below display the visited profile users posts    
    data.forEach(showposts);
    //profile.map(showposts);

    function showposts(profile) {
    
      const post_grid = document.createElement('div');
            post_grid.id = "post";
            post_grid.setAttribute("class", "post_grid");
            document.querySelector("#profile").appendChild(post_grid);

      const picture = document.createElement('div');
            picture.id = "picture";
            picture.setAttribute('class', 'profile');
            //profile.innerHTML = `<h1> ${posts.user} </h1>`;
            post_grid.appendChild(picture);
      
      const user = document.createElement('div');
            user.id = `${profile.poster}`;
            //user.id = "user";
            user.setAttribute('class', 'user');
            user.setAttribute('data-section', 'profile');
            user.innerHTML = `<a>${profile.poster}</a>`;
            post_grid.appendChild(user);
      
            
      const time = document.createElement('div');
            time.id = "timestamp";
            time.setAttribute('class', 'timestamp');
            time.innerHTML = `<h5> ${profile.created }</h5>`;
            post_grid.appendChild(time);
      

      const body = document.createElement('div');
            body.id = "body";
            body.setAttribute('class', 'content');
            body.innerHTML = `<h1> ${profile.body} </h1>`;
            post_grid.appendChild(body);


      const likes = document.createElement('div');
            likes.id = "likes";
            likes.className = "bi bi-star fs-4 ";
            //likes.setAttribute("class", "likes");
            likes.innerHTML  =  `<i></i> ${profile.likes}`;
            post_grid.appendChild(likes);

    }
    
    /*
    document.querySelector("#btn_follow").addEventListener('click', () => {
      var x = document.querySelector("#btn_follow"); 
      if (x.hasAttribute("value")) {
        x.setAttribute("value", "Unfollow");      
      } else {
        x.setAttribute("value", "Folow");
      }
    });
    */
    
  })
  
 
  
}

/*
function followuser() { 

  const user = document.querySelector("#uservisited").value;

  console.log(user);

  document.querySelector("#follow_form").onsubmit = () => { 
    fetch('/followuser ', {

      method:"POST",
      body: JSON.stringify({
        username: user,
      })
    
    })
    .then(res => res.json())
    .then(data => {
      console.log("Success:", data);
  
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }



}
*/