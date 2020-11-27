// Display advanced search drop-down
function dropdown(){
  
    //Prevent adv-search box drops down twice cause of some conflits 
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        return;
      }
    }
    
    //Display drop down menu
    document.getElementById("dropdown").classList.toggle("show");
    //Disable the "simple search button"
    document.getElementById("simple_btn").classList.add("disabled");
    $('#simple_btn').prop("disabled", true)
    //Change the button background color to lightgrey
    document.getElementById("simple_btn").style.background="#A9A9A9";
    //Change the icon color to darkgrey
    document.getElementById("simple_btn").style.color="#808080";

    
    //If the advanced search text is not hidden
    if(document.getElementById("adv-search-link").hidden==false){
      //Change the text color to darker blue
      document.getElementById("adv-search-link").style.color = "#003399";
    }
    //Scroll the screen to display the whole advanced search menu
    scroll("scroll-anchor","adv-search")
}

// Hide the drop-down when somewhere else on webpage is clicked 
window.onclick = function(event) {
 
  if (event.target.tagName !='OPTION' && event.target.className != 'form-control' && event.target.className != 'form-group' 
    && event.target.className != 'btn' && event.target.tagName != 'SPAN') {
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
          //Enable the simple search button
          document.getElementById("simple_btn").classList.remove("disabled");
          $('#simple_btn').prop("disabled", false)
          //Change buttons' colors
          document.getElementById("simple_btn").style.background="#DAAA00";
          document.getElementById("simple_btn").style.color="#FFFFFF"
          document.getElementById("adv-search-link").style.color = "#007BFF";
      }
    }
  }
}

// Set the width of search bar
function resizeSearchBar(){

  //width of viewport of browser
  var viewW = this.window.innerWidth;

    //Adjust width of search bar
    if(viewW>1080){
      //Display link-style advanced search button
      document.getElementById("adv-search-link").hidden = false;
      
      //Hide arrow button
      document.getElementById("mobile-adv-search-btn").hidden = true;
      
      //Set width of search bar
      document.getElementById("adv-search").style.width = "600px";
      
    }
    else if(viewW>850){
      //Display link-style advanced search button
      document.getElementById("adv-search-link").hidden = false;
      
      //Hide arrow button
      document.getElementById("mobile-adv-search-btn").hidden = true;
      
      //Set width of search bar
      document.getElementById("adv-search").style.width = "550px";
    }
    else if(viewW >=576){
      
      //Hide link-style advanced search button
      document.getElementById("adv-search-link").hidden = true;
      
      //Display arrow button
      document.getElementById("mobile-adv-search-btn").hidden = false;
        
      //Set width of search bar
      if(viewW/2 >= 289)
        document.getElementById("adv-search").style.width = viewW/2+"px";
      else 
        document.getElementById("adv-search").style.width = "289px";
  
    }
    else{
      //Hide link-style advanced search button
      document.getElementById("adv-search-link").hidden = true;
      
      //Display arrow button
      document.getElementById("mobile-adv-search-btn").hidden = false;

      //Set width of search bar
      document.getElementById("adv-search").style.width = "360px";

    }
}

//Resize width of search bar for desktops/laptops
window.onresize = function(event){
   resizeSearchBar();
}

//Display an arrow button on mobile size screen, while display "Advanced Search" on larger screen.
function advSearchBtn(){

  //Real screen width
  var screenW = this.window.screen.width;


  //If the window screen size is mobile
  if(screenW<=540){
    //Hide text/link style advanced search button
    document.getElementById("adv-search-link").hidden = true;
    //Display icon style button
    document.getElementById("mobile-adv-search-btn").hidden = false;

    //For iPhone5
    if(screenW<=320 && screenW >280) document.getElementById("dropdown").style.left="-235px";//width==320px offset==-235px
    //For Moto G4 & Galaxy S5
    if(screenW >320 && screenW <411) document.getElementById("dropdown").style.left="-252px"; //width==360px offset==-252px
    //For Galaxy fold
    if(screenW==280)  document.getElementById("dropdown").style.left="-200px"; //width==280px offset==-200px

  }
  else{//For larger screen like tablets, laptops and desktops
    
    //Set width of search bar
     resizeSearchBar();
     
  }


  //Display the search bar after all parameters set. This prevents the search bar flashing horizontally in the initial 
  document.getElementById("adv-search").hidden = false;

}

function getCurrentFilters(){

  if(sessionStorage.length > 0){

    var html = "Current Filters";

    //Initializing variables, which store keywords input by user...
    var simple_kw = sessionStorage.getItem('simple_kw');
    var school = sessionStorage.getItem('school');
    var faculty = sessionStorage.getItem('faculty');
    var title = sessionStorage.getItem('title');
    var description = sessionStorage.getItem('description');

    //For simple search
    if(simple_kw != null && simple_kw.length > 0){

      html += " > Anything containing \"" + simple_kw + "\"";
      
    }
    else{//For advanced search

       if(school != ""){
          html +=" > \""+ school +"\" ";
        }
        if(faculty != ""){
          html += " > \"" + faculty +"\" ";
        }
        if(title != ""){
          html += " > Titles containing \"" + title + "\" ";
        }
        if(description != ""){
          html += " > Descriptions containing \"" + description +"\" ";
        }
    }
    
    document.getElementById("filters_text").innerHTML= html;
  
  }
  //No filters
  else {
    document.getElementById("module-title").innerHTML ="All Projects";
    document.getElementById("filters_text").innerHTML = "Current Filters > None";
    
  }
  

}


//Auto-scroll the page to anchor's or smAnchor's position
function scroll(anchor,smAnchor){
  if(document.getElementById(anchor) !=null){
    //Get the broswer's type
  var userAgent = navigator.userAgent;
  var isOpera = userAgent.indexOf("Opera") > -1;
  var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera; 
  var isSafari = userAgent.indexOf("Safari") > -1 && userAgent.indexOf("Chrome") == -1;

  //If we need to fit smaller screen
  if(smAnchor!=null){
    //If the screen is smaller
    if(window.screen.width<=320){
        //Get the anchor
        var anchor = document.getElementById(smAnchor);
        //If the browser is safari or IE, do a naive scrolling as they don't support the advanced
        if(isSafari || isIE){ anchor.scrollIntoView(true);} 
        //For other browswers, do a advanced scrolling
        else anchor.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
        return;
    }
  }
  //If we don't need to fit smaller screens
  //Get the anchor
  var anchor = document.getElementById(anchor);
  //If the browser is safari or IE, do a naive scrolling as they don't support the advanced
  if(isSafari || isIE){anchor.scrollIntoView(true);}
  //For other browswers, do a advanced scrolling
  else anchor.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});

  }


}

