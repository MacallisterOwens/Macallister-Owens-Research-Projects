
//Handler
function paginator(currentPageNum, maxPageNum){
	highlightPageIndex(currentPageNum, maxPageNum);
	disablePrevNext(currentPageNum,maxPageNum);
}

//Active current page index. e.g. if current page is 2nd, the 2nd index of paginator will be coloured.
function highlightPageIndex(currentPageNum, maxPageNum){
	for(i=1; i<=maxPageNum;i++)
		document.getElementById("page"+currentPageNum).classList.remove("active");
	document.getElementById("page"+currentPageNum).classList.add("active");
	
}


//Enable or disable the "Previous page button" and "Next page button" for the paginator
function disablePrevNext(currentPageNum,maxPageNum){
	//If only one page, disable prev and next button
	if(maxPageNum==1){
		document.getElementById("prev").classList.add("disabled");
		document.getElementById("next").classList.add("disabled");
		return;
	}
	//If current page is the 1st, disable and dim the Previous button
	if(currentPageNum==1){
		document.getElementById("prev").classList.add("disabled");
		document.getElementById("next").classList.remove("disabled");
	}
	//If current page is the last page, disable and dim the Next button
	else if(currentPageNum==maxPageNum){
		document.getElementById("next").classList.add("disabled");
		document.getElementById("prev").classList.remove("disabled");
	}

}