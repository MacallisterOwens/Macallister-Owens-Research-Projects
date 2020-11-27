// Some sort-by function stuff here. 

//Store search keywords for "sort by" function if an user input some.
//These stored information will be deleted by the browser when the user closed the tab.
function storeKeywords(){
	//Reset storage
	sessionStorage.clear();

	if(document.getElementsByName("search_simple")[0].value){
		//Store keywords for simple search 
		sessionStorage.setItem('simple_kw', document.getElementsByName("search_simple")[0].value);
		
	}
	else{
		
		//Store keywords for advanced search
		sessionStorage.setItem('school',document.getElementsByName("school")[0].value);
		sessionStorage.setItem('faculty', document.getElementsByName("faculty")[0].value);
		sessionStorage.setItem('title', document.getElementsByName("search_title")[0].value);
		sessionStorage.setItem('description', document.getElementsByName("desc_title")[0].value);
	}

	//Prevent submiting an empty form 
	var count = 0;//How many non-empty fields?
	for(var i = 0; i < sessionStorage.length; i++){
		if(sessionStorage.getItem(sessionStorage.key(i)) != "")
			count++;
	}
	// If there is any keyword,do search.
	if(count>0) return true;
	//Otherwise
	else return false; 

}

//Grab keywords and the way of sorting, and send them to start a new search
function sortBy(){

	//Initializing variables, which store keywords input by user...
	var simple_kw = sessionStorage.getItem('simple_kw');
	var school = sessionStorage.getItem('school');
	var faculty = sessionStorage.getItem('faculty');
	var title = sessionStorage.getItem('title');
	var description = sessionStorage.getItem('description');

	//Get the Sort-By selection form in search.html
	var sort_by_selector = document.getElementById('sort_by_form');
	
	//Set the keyword for simple search
	var hiddenInput = document.createElement('input');
	hiddenInput.type = 'hidden';
	hiddenInput.name = "search_simple";
	hiddenInput.value = simple_kw;
	sort_by_selector.appendChild(hiddenInput);

	//Set the keywords for advanced search
	//School
	hiddenInput = document.createElement('input');// Pls do not disable these two lines of "redundant" code, 
	hiddenInput.type = 'hidden';				  // since they are not redundant. Same below
	hiddenInput.name = "school";
	hiddenInput.value = school;
	sort_by_selector.appendChild(hiddenInput);
	//Faculty
	hiddenInput = document.createElement('input');
	hiddenInput.type = 'hidden';
	hiddenInput.name = "faculty";
	hiddenInput.value = faculty;
	sort_by_selector.appendChild(hiddenInput);
	//Title
	hiddenInput = document.createElement('input');
	hiddenInput.type = 'hidden';
	hiddenInput.name = "search_title";
	hiddenInput.value = title;
	sort_by_selector.appendChild(hiddenInput);
	//Description
	hiddenInput = document.createElement('input');
	hiddenInput.type = 'hidden';
	hiddenInput.name = "desc_title";
	hiddenInput.value = description;
	sort_by_selector.appendChild(hiddenInput);

	//Submit the form to get sorted results.
	sort_by_selector.submit();


}


//Update sort by selector to show current method
function updateSelector(current_order){
	//Get the selector in search.html
	var options = document.getElementById("sort_by_select");

	//Set the option to be selected iff it has same value with current order method which is used by the user
    for(i=0; i < options.length; i++)
    {
        if(options[i].value == current_order)
            options[i].selected = true;
    }
}

