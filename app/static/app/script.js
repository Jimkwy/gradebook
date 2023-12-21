document.addEventListener("DOMContentLoaded", function() {

  //add event listeners to each submit button after checking if they were generated
  if (document.getElementById('join_form')) {
    document.getElementById('join_form').addEventListener('submit', joinSchool);
  }
  if (document.getElementById('newSchool_form')) {
    document.getElementById('newSchool_form').addEventListener('submit', newSchool);
  }
  if (document.getElementById('addCourse_form')) {
    document.getElementById('addCourse_form').addEventListener('submit', addCourse);
  }

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

//api call for creating a new school
function newSchool() {
    fetch('/newSchool' , {
        method: 'POST',
        body: JSON.stringify({
          name: document.getElementById('school_name').value,
          address: document.getElementById('school_address').value,
          phone: document.getElementById('school_phone').value
        })
      })
      .then(response => response.json())
      .then(result => {
        console.log(result);
      });
};

//api call for joining a school with a referal code
function joinSchool() {

fetch('/joinSchool' , {
    method: 'POST',
    body: JSON.stringify({
        school_code: document.getElementById('school_code').value,
    })
    })
    .then(response => response.json())
    .then(result => {
    console.log(result);
    });
};

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