//global variable to output to console during implementation
IS_DEBUG = false; 

//function _(x) as a quick getter method
function _(x) {
/*********************
    Helper function that allows quick access
    to document.getElementById()
    ARGS:
        x: (str) element to return
    RETURNS:
        None
*********************/
    return document.getElementById(x);
}


function search(){
/*********************
    Filter table by selected input type.
    ARGS:
        None
    RETURNS:
        None
*********************/

    //variable initialization at start
    //to help with performance
    var input;
    var filter;
    var table;
    var tr;
    var td1;
    var td2;
    var td3;
    var i;
    var size;
    var value;
    var option;

    //get value of 1 <= option <= 2
    option = parseInt(_('sel').value);

    //str containing the desired search
    input  = _('search_inp');

    //ignore case-sensitivity
    filter = input.value.toLowerCase();

    //table to search
    table  = _('transactionTable');

    //rows to search
    tr = table.getElementsByTagName("tr");
    
    //length of table
    size = tr.length;

    for (i = 0; i < size; i++) {

        //Transaction Date
        td1 = tr[i].getElementsByTagName("td")[0]; 

        //Merchent
        td2 = tr[i].getElementsByTagName("td")[1]; 

        //Amount
        td3 = tr[i].getElementsByTagName("td")[2]; 

        //check if filter is in transaction date
        if (option == 1){
            if(td1) {
                value = td1.textContent || td1.innerText;
                if (value.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display="";
                }
                else {
                    tr[i].style.display="none";
                }
            }
        }

        //check if filter is in Merchant 
        if (option == 2) {
            if(td2) {
                value = td2.textContent || td2.innerText;
                if (value.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display="";
                }
                else {
                    tr[i].style.display="none";
                }
            }
        }

        //check if filter is in Amount 
        if (option == 3) {
            if(td3) {
                value = td3.textContent || td3.innerText;
                if (value.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display="";
                }
                else {
                    tr[i].style.display="none";
                }
            }
        }

    }
}



function insertHTML(id, text) {
/*********************
    Helper function that inserts html info
    into html id.
    ARGS:
        id:     (str) html tag to insert
        text:   (str) query to insert
    RETURNS:
        None
*********************/

    //caller to our helpful _() function
    _(id).innerHTML = text;
}


function displayInfo(list) {
/*********************
    Function gets called by both checkLogin() and
    loginFunction(). Used to display a transaction
    list provided by the Expensify API.
    ARGS:
        None
    RETURNS:
        None
*********************/

    var txt = "";
    var search = "";
    var option = "";
    var info = "";
    var query = ""
    var i;


    //insert data to tables
    txt += "<table border='1'>";
    for (i in list) {
        txt += "<tr>";
        txt += "<td>"+ list[i].created + "</td>"; 
        txt += "<td width='30%'>"+ list[i].merchant + "</td>"; 

        //check if the currency is USD
        //Otherwise, do not add currency sign
        //O(1) check, so doesnt slow down too much
        if (list[i].currency == "USD") {
            txt += "<td>$"+ list[i].amount + "</td>"; 

        }
        else{
            txt += "<td>"+ list[i].amount + "</td>"; 
        }
        txt += "</tr>";
    }

    //little ugly, but this keeps the main homepage clean before logging in 
    search = "<input type='text' id='search_inp' onkeyup='search()' placeholder='Search for desired query'>"; 
    option =    "<select id='sel'>" +
                    "<option value='1'>Transaction Date</option>" +
                    "<option value='2'>Merchant</option>" +
                    "<option value='3'>Amount</option>" +
                    "</select>";
    info   =  "<table id='info' border='1'>"+ 
                "<thead><tr>" +
                "<th>Transaction Date</th>" + 
                "<th>Merchant</th>"+
                "<th>Amount</th>"+ 
                "</tr>";
    
    //display what the table is
    $('#t_h1').append("Transactions:");

    //add search bar
    query = search + option;
    insertHTML('search',query);

    //add floating header to table
    insertHTML('transactionInfo',info);

    //add the data from API result to table
    insertHTML('transactionTableBody',txt);

    //display transaction form
    $('#transactionForm').removeClass('hidden').addClass("div_2");
    $('#info_div').removeClass('hidden').addClass("info_div");

}

function createTransaction(){
/*********************
    Creates a new transaction from html form.
    ARGS:
        None
    RETURNS:
        None
*********************/
    var formdata;
    var result;
    var list;
    var ajax;

    console.log('create');
    _("transaction_btn").disabled = true;
    $('#transaction_form').hide();
    _("create_status").innerHTML = "Creating transaction...";

    formdata = new FormData();
    formdata.append('functionName', 'createTransaction');
    formdata.append('date',         _('date').value);
    formdata.append('merchant',     _('merchant').value);
    formdata.append('amount',       _('amount').value);
    
    ajax = new XMLHttpRequest();
    ajax.open("POST", "proxy.php",true);
    ajax.onreadystatechange = function() {
        if(ajax.readyState == 4 && ajax.status == 200){
            console.log(JSON.parse(ajax.response));
            result = JSON.parse(ajax.response);
            if (result['jsonCode'] == 200) {
                insertHTML('create_status', "Done! Refresh the page and search for your transaction.");
            }
            else{
                insertHTML("create_status","Something went wrong. Please try again<br><small>Tip: Check that all fields are complete.</br>");
                _("transaction_btn").disabled = false;
                }
            
        }
    }
    ajax.send(formdata);
}

function checkLogin(){
/*********************
    Function is ran on page load 
    Handles authorization of log in and
    handles 407 (Expired Token) error.
    ARGS:
        None
    RETURNS:
        None
*********************/
    var cookie;
    var result;
    var list;
    var formdata;
    var ajax;

    var cookie = decodeURIComponent(document.cookie);

    //console.log check to see if cookie is set
    if (IS_DEBUG) { console.log(cookie); }

    if (cookie.includes('authToken')){
        _('status').innerHTML = "Checking cookies...";

        formdata = new FormData();

        //only data to send to proxy server
        //proxy handles function calling
        formdata.append('functionName', 'loggedIn' );
        ajax = new XMLHttpRequest();

        //If the user is authenticated, this
        //is technically just a GET method
        ajax.open("POST", "proxy.php",true);
        ajax.onreadystatechange = function() {
            if(ajax.readyState == 4 && ajax.status == 200){

                //check what ajax response is
                if (IS_DEBUG) { console.log('response',ajax.response); }

                result = JSON.parse(ajax.response);

                //check to see if authentication succeeds 
                if (result['jsonCode'] == 200) {
                    $("#login_form").hide();
                    insertHTML('status',"Welcome Back!");

                    //retrieve list and send to 
                    //helper function
                    list = result['transactionList'];
                    displayInfo(list);

                    //expired token
                } else if (result['jsonCode'] == 407) {
                    insertHTML("status","Your token has Expired. <b>Please log in again.");

                    //reenable login button
                    _("login_btn").disabled = false;
                }
                else {
                    insertHTML('status',"Welcome! Please log in to continue.");
                }
            }
        }
    ajax.send(formdata);
    }
    else{
        _('login_btn').disabled = false;
    }
}

function loginFunction() {
    /*
    Handles authentication through Expensify API
    using proxy server. Function is called after
    submitting credentials on HTML form.
    Args:
        None
    Returns:
        None
    */
    var result;
    var list;
    var ajax;
    var formdata;

    //disable login button to restrict
    //multiple requests to server
    _("login_btn").disabled=true;
    _("status").innerHTML="Logging in...";

    //formdata and attributes from log in form
    formdata = new FormData();
    formdata.append("functionName",         "authenticate");
    formdata.append("partnerName",          _("partnerName").value );
    formdata.append("partnerPassword",      _("partnerPassword").value );
    formdata.append("partnerUserID",        _("partnerUserID").value );
    formdata.append("partnerUserSecret",    _("partnerUserSecret").value );

    if (IS_DEBUG){
        console.log('formdata for login');
        for (var key of formdata.keys()) {
            console.log("key:",key); 
        }
    }

    ajax = new XMLHttpRequest();
    ajax.open('POST','proxy.php',true);
    ajax.onreadystatechange = function() {
        if(ajax.readyState == 4 && ajax.status == 200){
            result = JSON.parse(ajax.response);
            if (IS_DEBUG){
                console.log('JSON result from AJAX:',result);
            }
            console.log(result['jsonCode']);

            //check to see if authentication succeeds 
            if (result['jsonCode'] == 200) {
                $("#login_form").hide();
                insertHTML('status',"");
                $("#loginContent").append("You have successfully logged in!");

                list = result['transactionList'];
                displayList(list);

            //password authentication failed
            } else if (result['jsonCode'] == 401) {
                insertHTML("status","The name or password you submitted did not match our records. <b>Please Try Again");

                //reenable login button
                _("login_btn").disabled = false;

            } else if (result['jsonCode'] == 404) {
                insertHTML("status","The user informationt you submitted did not match our records. <b>Please Try Again");

                //reenable login button
                _("login_btn").disabled = false;
            }
        }
    }
    ajax.send(formdata);

}
