document.addEventListener("DOMContentLoaded", function() {

});

//primary view loading function
function load_view(view) {
    console.log(view)
    const views = document.getElementsByClassName('view');
    for (i = 0; i < views.length; i++) {
        views[i].style.display = 'none';
        };
    
    document.getElementById(view).style.display = 'block';
}