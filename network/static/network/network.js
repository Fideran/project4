document.addEventListener('DOMContentLoaded', function(){
    
    let post = 'allposts';
    let page_num = 1;
    document.querySelectorAll('.page-link').forEach(link => {
        link.onclick = function(){
            page_num = this.dataset.value;
            loadPost(post, page_num);};
    })

    post_like();
//default view
    loadPost(post, page_num);
    

//Display User Profile View
    const user_link = document.querySelector("#user_link");
    user_link.addEventListener('click', () => {userProfile()});
    
//Display All Posts and Following view
    
    document.querySelector('#all_posts_link').addEventListener('click', () => {
        let post = 'allposts';
        document.querySelector('#pages').style.display = 'block';
        document.querySelectorAll('.page-link').forEach(link => {
            link.onclick = function(){
                page_num = this.dataset.value;
                loadPost(post, page_num); return false};
            });
        loadPost(post, page_num);
    });
    document.querySelector('#following_link').addEventListener('click', () => {
        let post = 'following';
        document.querySelector('#pages').style.display = 'none';
        document.querySelectorAll('.page-link').forEach(link => {
            link.onclick = function(){
                page_num = this.dataset.value;
                loadPost(post, page_num); return false};
        });
            loadPost(post, page_num)});


//Creat a new post
    document.querySelector('#new_form').onsubmit = new_post;

//Button Pagination
});

function userProfile(){
    document.querySelector('#profile').innerHTML = '';
    document.querySelector('#profile_view').style.display = 'none';
    document.querySelector('#user-profile-view').style.display = 'block';
    document.querySelector('#all-post-view').style.display = 'none';
    document.querySelector('#edit_view').style.display = 'none';
    fetch('/user')
    .then(response => response.json())
    .then(user_profile => {
        const username = user_profile.username;
        const email = user_profile.email;
        const username_div =document.createElement('div', 'user-name');
        username_div.innerHTML = `${username}`;
        const email_div = document.createElement('div', 'user-email');
        email_div.innerHTML =`${email}`;
        document.querySelector('#profile').append(username_div, email_div);
    })
}

function profile(element, follower, follower_num){
    document.querySelector('#user-profile-view').style.display = 'none';
    document.querySelector('#all-post-view').style.display = 'none';
    document.querySelector('#profile_view').style.display = 'block';
    document.querySelector('#edit_view').style.display = 'none';
    document.querySelector('#other_profile').innerHTML = `${element.user}: ${element.email}
            <button id="follow${element.user_id}">Follow</button>
            <div id="follower${element.user_id}">Followers: ${follower_num} </div>
    `;
    fetch('/follow')
    .then(response => response.json())
    .then(result => {
        data = result.followed;
        arr = data.filter(el => el.followed_id === element.user_id );
        arr2 = arr.filter(el => el.follower_id === follower.id);
        const button = document.querySelector('#follow'+element.user_id);
        button.innerHTML = arr2[0].button_value;
        
        
    })
    document.querySelector('#follow'+ element.user_id).onclick = () =>{
        const button = document.querySelector('#follow'+element.user_id);
        if(button.innerHTML !== 'Follow'){
            //alert('Are You Sure!!!');
            unfollow(element);
            document.querySelector('#follower'+element.user_id).innerHTML = `Followers: ${follower_num}`;  
        }else{follow(element, follower_num)}
        
    }

}

function loadPost(post, page_num){
    document.querySelector('#all-post').innerHTML = '';
    document.querySelector('#all-post-view').style.display = 'block';
    document.querySelector('#user-profile-view').style.display = 'none';
    document.querySelector('#profile_view').style.display = 'none';
    document.querySelector('#edit_view').style.display = 'none';

    if(post === 'allposts'){
        document.querySelector('#new-post').style.display = 'block';
        fetch(`allposts/allposts/${page_num}`)
        .then(response => response.json())
        .then(posts => {
            posts.posts.forEach(element => {
                //const likes_number = post_like()//return: post_id and nbr of like
                post_like(element);
            });
        });
        }
    if(post === 'following'){
        document.querySelector('#new-post').style.display = 'none';
        fetch(`allposts/following/${page_num}`)
        .then(response => response.json())
        .then(posts => {
            posts.follows.forEach(element => {
                const followed = element.user;
                posts.posts.forEach(post =>{
                    if(post.user === element.user){
                        post_like(post);
                    }
                })
            
            });
        });
    }
}

function pagination(post){
    loadPost(post, page_num)
}

function post_display(element, like, user_id){
    
    if(like !== []){like_num = like[0].likes_number;
    }else{like_num = 0;}
    
    
    const post = document.createElement('div');
    post.id = `post_div_${element.id}`;
    post.className = 'post';
    post.innerHTML = `
        <div><a href="#"  data-profile_id="${element.user_id}" id="post${element.id}"><b>${element.user}</b></a> <fid id=email>${element.email} . ${element.time}</fid></div>
        <div class="content" id="content_${element.id}">${element.content}</div>
        <div id="like_comment_edit${element.id}" class ="like_comment_edit">
        <button class="like_button" id="like_${element.id}">🧡${like_num}</button>
        <button class="comment_button">💬${element.comment}</button></div>
        `;
    document.querySelector('#all-post').append(post);

    //LIKE and UNLIKE
    const love = document.querySelector('#like_'+element.id);
    love.onclick = function(){
        if(like[0].every_likes.length === 0){
            console.log('like_num ='+(like[0].every_likes.length+1));
            love.innerHTML = `🧡${like[0].every_likes.length+1}`;
            //post method to save like
            fetch('/like', {
                method: 'POST',
                body: JSON.stringify({
                    user_id: user_id,
                    post_id: element.id, 
                })
            })

        }else{
            const likers = like[0].every_likes;
            console.log(user_id);
            function filter_id(obj){
                if(obj.id === user_id){
                    return true;
                }else{return false;}
            }
            already_liker = likers.filter(filter_id);
            console.log(already_liker);
            if(already_liker.length === 0){
                love.innerHTML = `🧡${like[0].every_likes.length+1}`;
                //post method to save like
                fetch('/like', {
                    method: 'POST',
                    body: JSON.stringify({
                        user_id: user_id,
                        post_id: element.id
                    })
                })
            }else{
                //post method to unlike
                love.innerHTML =`🧡${like[0].every_likes.length-1}`
                fetch('/unlike', {
                    method: 'POST',
                    body: JSON.stringify({
                        user_id: user_id,
                        post_id: element.id
                    })
                })
            }
            

            
        };

    };

    //CREAT EDIT BUTTON
    if(element.user_id === user_id){
        const edit = document.createElement('button');
        edit.id = `edit_${element.id}`
        edit.className = 'edit';
        edit.innerHTML = 'Edit';
        document.querySelector('#like_comment_edit'+element.id).append(edit);
    }
    //EDIT POST
    const post_edit = document.querySelector('#edit_'+element.id);
    post_edit.onclick = function(){
        document.querySelector('#all-post-view').style.display = 'none';
        document.querySelector('#user-profile-view').style.display = 'none';
        document.querySelector('#profile_view').style.display = 'none';
        document.querySelector('#edit_view').style.display = 'block';
        document.querySelector('#text_edit').value = element.content;
        document.querySelector('#edit_form').onsubmit = ()=>{
            //POST METHOD HERE
            const content = document.querySelector('#text_edit').value;
            alert(content);
            console.log(content);
            fetch('/edit_post', {
                method: 'POST',
                body: JSON.stringify({
                    content: content,
                    post_id: element.id,
                })
            })
        }

    };

    //PROFILE OTHER USER
    const profiles = document.querySelector('#post'+ element.id);
    profiles.onclick = function(){
        fetch('/profile/follower')
        .then(response => response.json())
        .then(result=> {
            let data = result.Followers;
            arr = data.filter(a => a.id === element.user_id);
            follower = arr[0];
            follower_num = follower.follower
        });

        fetch('/user')
        .then(response => response.json())
        .then(user_profile => {
            const username = user_profile.username;
            const email = user_profile.email;
            const id = user_profile.id;
            alert(id + '=' + element.user_id);
            if(id === element.user_id){userProfile()}
            else{profile(element, user_profile, follower_num)}
        })
            };
}

function new_post(){
    alert('You Can Create a New Post');
    const content = document.querySelector('#content').value;
    console.log(content);
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    
    
    return false;
}

function post_like(element){
    const post = element
    fetch('/like')
    .then(response => response.json())
    .then(result => {
        let data = result.likes;
        arr = data.filter(x => x.post_id === post.id);
        fetch('/user')
        .then(response => response.json())
        .then(user_profile => {
            const username = user_profile.username;
            const id = user_profile.id;
            post_display(post,arr, id);        })
        
    })
    return false;
}
function follow(element,follower_num){
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            followed_id: element.user_id,
        })
    })
    
document.querySelector('#follow'+element.user_id).innerHTML = 'Unfollow';  
document.querySelector('#follower'+element.user_id).innerHTML = `Followers: ${follower_num+1}`;  
}

function unfollow(element){
    fetch('/unfollow', {
        method: 'POST',
        body: JSON.stringify({
            unfollowed_id: element.user_id,
        })
    })
    
document.querySelector('#follow'+element.user_id).innerHTML = 'Follow';


}