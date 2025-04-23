{/* <script> */}
const PRIMARY_COLOR = '#5A0B29'; 
const PRIMARY_LIGHTCOLOR = '#A71D46'; 
const SECONDARY_COLOR = 'white'

document.addEventListener('DOMContentLoaded', function() {
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const closeMenu = document.getElementById('closeMenu');

if(menuToggle){
    menuToggle.addEventListener('click', function() {
    mobileMenu.classList.remove('translate-x-full');
});

closeMenu.addEventListener('click', function() {
    mobileMenu.classList.add('translate-x-full');
});
}

});



const form = document.querySelector('#messageForm');
if(form){
form.addEventListener('submit', function(e) {
    e.preventDefault();
    $.ajax({
    url : `/message`,
    type: 'POST',
    data: { 
        csrfmiddlewaretoken: '{{csrf_token}}',
        name: $('#name').val(),
        message: $('#message').val(),
        phone: $('phone').val() || '',
        email : $('email').val(),
    },
    beforeSend: function(){
    },
    success: function(res) {
        
        if(res.status == 'success'){
            
            alert('Merci pour votre message, on vous contactera sous peu!');
            form.reset();
        }

    },
    complete: function(){
    },

    error: function(jqXHR,textstatus,errorThrown){
    }

})
    
});
}

// Intersection Observer for smooth animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible-element');
        }
    });
}, { threshold: 0.1 });

const hiddenElements = document.querySelectorAll('.hidden-element');
hiddenElements.forEach(el => observer.observe(el));
        
        {/* </script> */}