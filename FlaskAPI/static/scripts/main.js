function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("myNavId").style.marginLeft = "250px";
  document.getElementById("mainHomeId").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("myNavId").style.marginLeft = "0";
  document.getElementById("mainHomeId").style.marginLeft = "0";
}

// Script for Deployment Frequency Page

function hide_seek() {
  var filter_id = document.getElementById("filter_type");
  var selected_filter = filter_id.options[filter_id.selectedIndex].value;
  
  // var project_id = document.getElementById("fetchProjectid");
  // var project_id_value = project_id.options[project_id.selectedIndex].value;
  if (
    selected_filter == "project" ||
    selected_filter == "users" ||
    selected_filter == "date_range"
  ) {
    document.getElementById("fetchProject_div").style.display = "inline";
  } else {
    // document.getElementById("fetchProject_div").style.display = "none";
    document.getElementById("date_range_div").style.display = "none";
  }

  if (selected_filter == "choose") {
    document.getElementById("fetchProject_div").style.display = "none";
  }

  if (selected_filter == "date_range") {
    document.getElementById("date_range_div").style.removeProperty("display");
  } else {
    // document.getElementById("fetchProject_div").style.display = "none";
    document.getElementById("date_range_div").style.display = "none";
  }
}



function show_workspace() {

  var project_id = document.getElementById("fetchProjectid");
  var project_filter = project_id.options[project_id.selectedIndex].value;

  
  
  if (project_filter == "choose") {
    document.getElementById("workspace_div").style.display = "none";
  } else {
    document.getElementById("workspace_div").style.removeProperty("display");
  }
    
}
