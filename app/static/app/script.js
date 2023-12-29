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

//api call for adding a new course
function addCourse() {
  
  // api call to submit new class
  fetch('/addCourse' , {
    method: 'POST',
    body: JSON.stringify({
      subject: document.getElementById('course_subject').value,
      code: document.getElementById('course_code').value,
      level: document.getElementById('course_level').value,
      year: document.getElementById('course_year').value,
      description: document.getElementById('course_descrition').value,
      start: document.getElementById('course_start').value,
      end: document.getElementById('course_end').value,
      })
    })
    .then(response => response.json())
    .then(result => {
    console.log(result);
    });
};